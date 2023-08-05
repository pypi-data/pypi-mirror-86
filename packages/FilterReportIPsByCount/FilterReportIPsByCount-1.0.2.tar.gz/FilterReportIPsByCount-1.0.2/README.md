# FilterReportIPsByCount
Script to read through a report containing IP addresses that are potentially malicious and require blacklisting, check if those IPs appear in the report a number of times (count), and check if those IPs have been blacklisted. Outputs list of IPs and the IPs' analysis to standard out or in a chosen file.

## How to Use
1.  [Make sure that you have Python installed on your computer, and that it is updated to at least version 3.6 ](https://www.python.org/downloads/)
    *  [Make sure that you set up Python environment variables](https://docs.python.org/3/using/windows.html#excursus-setting-environment-variables)
2.  Download the zip file or clone the repository
3.  In the command line, navigate to the repository and enter the below command (Only required with first use)
    * `pip install -r requirements.txt`
4.  Enter the below command with the following arguments
    * `FilterReportIPsByCount\FilterReportIPsByCount.py -i <input filename> -o <output filename> -c <count>`
    > **-i [input filename]** : REQUIRED, the filename (with path, if not on the same directory) of the excel file you want to analyze
    >
    > **-o [output filename]** : Optional, the filename of the text file to which you would like to print the IP analysis information; if not specified, will output to stdout
    >
    > **-c [count]** : Optional, number of times an IP should appear in the report to be added to the list of IPs to analyze; if not specified, will default to 5
    >
    > **-h** : Shows the arguments and options required 
