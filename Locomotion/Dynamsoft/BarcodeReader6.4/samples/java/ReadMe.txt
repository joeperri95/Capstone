----------------------------------------
Dynamsoft Barcode Reader Java Demo ReadMe
----------------------------------------

Introduction
This Java sample is developed by using Java Native Interface to call the C API of Dynamsoft Barcode Reader. The sample demonstrates how to read barcodes from the Command Line.

ENVIRONMENT
- Linux x64

INSTALL
1. Extract the zip and enter the "BarcodeReaderDemo" folder.
2. Open Eclipse and import the project. 
3. Run as java application and follow the instruction step by step.

Note:
If you need to support reading PDF files on Linux:
A. To run the demo from eclipse
   1) Click Menu "Run" then "Run Configurations"
   2) Select the target configuration, then click on the "Environment" Tab
   3) Add "LD_LIBRARY_PATH" and set its value to "/tmp"
B. To run the demo from terminal, 
   a) You can execute the following command: 
       export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp
   b) Or append the above text "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp" at the end of file "~/.bashrc", then execute the command "source ~/.bashrc" to take effect immediately.

How to extend your trial license:
1. Open the "Get Your Trial License Now" to retrieve a trial license.
2. Find string "new BarcodeReader" in the file "src\com\dynamsoft\demo\BarcodeReaderDemo.java" and replace with the new key.

If you run into any issues, please feel free to contact us at support@dynamsoft.com.

Copyright (C) Dynamsoft Corporation 2018.  All rights reserved.