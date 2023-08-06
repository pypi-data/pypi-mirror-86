#!/usr/bin/python
# FilterReportIPsByCount
# Divyaa Kamalanathan 2020 divyaaveerama96@gmail.com
# Script to read through a report on an excel file, grab IPs if it is greater than or equal
# to a set count and check if malicious
# GNU Public License v3


import sys
import requests
import xlrd
import re
import getopt
import config


# Function to check the Excel file for IP addresses and add those to a list

def getIPsFromExcelFile(filename):
    IPs = []
    IPCheck = re.compile(r'^([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)$')
    excelFile = (filename)

    try:
        wb = xlrd.open_workbook(excelFile)
    except:
        print("Input File not Found")
        sys.exit(2)

    sheet = wb.sheet_by_index(0)
    for x in range(sheet.ncols - 1):
        for y in range(sheet.nrows - 1):
            value = sheet.cell_value(y, x)
            if IPCheck.match(value):
                IPs.append(value)
    return IPs


# Check list of IPs to see if each IP appears <set count> or more times 
def getIPsToBan(IPs, count):
    IPsWithCount = {}
    IPsToBan = []

    for IP in IPs:
        if IP in IPsWithCount:
            IPsWithCount[IP] += 1

        if IP not in IPsWithCount:
            IPsWithCount[IP] = 1

    for IP in IPsWithCount:
        if IPsWithCount[IP] >= count:
            IPsToBan.append(IP)

    return IPsToBan


# Use IPVoid API to check if IP has been blacklisted, returns IPs and IP Information
def checkIfMalicious(IPsToCheck):
    apikey = config.api_key()
    MalIPs = {}
    for IP in IPsToCheck:
        response = requests.get('https://endpoint.apivoid.com/iprep/v1/pay-as-you-go/?key=' + apikey + '&ip=' + IP)
        if response.status_code == 200:
            response_json = response.json()
            try:
                if response_json['data']['report']['blacklists']['detections'] >= 1:
                    blacklistStatus = "Blacklisted " + str(
                        response_json['data']['report']['blacklists']['detections']) + "/" + str(
                        response_json['data']['report']['blacklists']['engines_count'])
                    reverseDNS = str(response_json['data']['report']['information']['reverse_dns'])
                    ISP = str(response_json['data']['report']['information']['isp'])
                    Continent = str(response_json['data']['report']['information']['continent_name'])
                    Country = str(response_json['data']['report']['information']['country_name'])
                    analysis = "IP Address : " + IP + "\nBlacklist Status: " + blacklistStatus + "\nReverse DNS: " + reverseDNS + "\nISP: " + ISP + "\nContinent: " + Continent + "\nCountry: " + Country + "\n\n"
                    MalIPs[IP] = analysis
            except:
                pass

    return MalIPs


# Print IPs to ban in a list and IP info to file
def PrintIPInformationIntoFile(maliciousIPs, filename):
    fo = open(filename, "w+")
    for keys in maliciousIPs.keys():
        fo.write(keys)
        fo.write("\n")
    fo.write("\n")

    for values in maliciousIPs.values():
        fo.write(values)


# Print IPs to ban in a list and IP info to stdout, if no output file is specified
def PrintIPInformation(maliciousIPs):
    for keys in maliciousIPs.keys():
        print(keys)
        print("\n")

    print("\n")

    for values in maliciousIPs.values():
        print(values)
        print("\n")


# Main Function    
def main(argv):
    excelFileName = ''
    outputFileName = ''
    count = 0

    try:
        opts, args = getopt.getopt(argv, "hi:o:c:")

    except getopt.GetoptError:
        print("FilterReportIPsByCount.py -i <input filename> -o <output filename> -c <count of IPs to check for>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("FilterReportIPsByCount.py -i <input filename> -o <output filename> -c <count of IPs to check for>")
            sys.exit()

        elif opt in ("-i"):
            excelFileName = arg

        elif opt in ("-o"):
            outputFileName = arg

        elif opt in ("-c"):
            count = int(arg)

    if count <= 0:
        print("Invalid count, using default count of 5")
        count = 5

    IPs = getIPsFromExcelFile(excelFileName)
    IPsToBan = getIPsToBan(IPs, count)
    MaliciousIPs = checkIfMalicious(IPsToBan)
    if outputFileName != '':
        PrintIPInformationIntoFile(MaliciousIPs, outputFileName)
    else:
        PrintIPInformation(MaliciousIPs)


if __name__ == "__main__":
    main(sys.argv[1:])
