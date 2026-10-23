# _Konzept – Examples

## Examples

*Quelle: `Examples.html` · Object Model Reference*

#### PolyFile.xls

You will find the example PolyFile.xls in the folder Examples\Excel. PolyFile.xls is an Excel 2003 file containing VBA code to access and display data stored in PSV and VibSoft measurement files. To run the macro do the following:

- Start Excel 2003 or higher

- Open the file PolyFile.xls

- If there appears a message box that asks you whether to activate the macros in the files, answer this message box by activating the macros.

- On the appearing excel spreadsheet press the Select File button

- Select a PSV or VibSoft measurement file

- The file path appears in cell B1 of the spreadsheet

- Select Read Only or Read Write radio button to specify read/write access to the data. Read Only will show 3D user signals under UsrX, UsrY and UsrZ channels, otherwise, they will be listed under the Usr 3D channel.

- Press the Select Data button

- On the appearing dialog you can browse through the modes, domains, channels, signals, displays and points of the measurement file

- The data will be displayed as graph on the spreadsheet any time you change the selection

- To save user-defined data into the measurement file press the Save button on the dialog

- Close the dialog and close the spreadsheet. Do not save the changes

To view the VBA code of this sample click on the menu Extras/Macro/Visual Basic Editor while having PolyFile.xls opened. The code for selecting the file and displaying the data is in module SelectData. The code for the dialog is in the form UFSelectData.

This sample shows how to browse a measurement file for all available data and how to let the user select data he or she wants to display.

#### ComplexPointAverage.bas

You will find the example ComplexPointAverage.bas in the folder Examples\Macros.

To run this sample do the following:

- Start PSV or VibSoft

- Open the Basic Editor by clicking the menu Macro/Basic Editor

- Open the file ComplexPointAverage.bas

- Run the macro

- Select a PSV scan file taken in FFT mode

- Select a text file to store the complex average data

This sample shows how to access the point data of all valid measurement points of a PSV scan file and calculate the complex average of these points. This functionality is not built into PSV. PSV calculates an amplitude average of the points only. The macro saves the result as user-defined dataset in the average domain of the given scan file.

#### CplxPointAvg

You will find the example CplxPointAvg in the folder Examples\VC\CplxPointAvg.
 To run this sample do the following:

- Start Microsoft® Visual Studio® C++ Version 2013 or higher

- Open the solution CplxPointAvg.sln

- Open the project settings dialog by clicking the menu Project/Properties

- Select All configurations and in Configuration Properties / C/C++ select General

- Check the paths for Additional include directories  this should be the path of the installed Polytec File Access components. We have defined three paths there  C:\Program Files\Common Files\Polytec\COM, C:\Program Files\Common Files\Polytec\PDx, and C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Polytec.IO.Vibrometer\v4.0_2.4.0.0__e9bf5e9b998cc19f. If you have installed a not English version of Windows and/or your system drive is not C: you have to change these path values. To get the correct first two paths check the value of your environment variable %CommonProgramFiles% and append \Polytec\COM and \Polytec\PDx, respectively. For the third path check the value of %SystemRoot% and adjust the path accordingly.

- Build the project

- Run the application

- On the appearing dialog based application press the Select PSV Scan File button and select a PSV file taken in FFT mode

- Select a text file to store the complex average data

This sample shows how to access the point data of all valid measurement points of a PSV scan file and calculate the complex average of these points. This functionality is not built into PSV. PSV calculates an amplitude average of the points only. This dialog-based application exports the data to an ASCII-File. You can save the ASCII-File with the extension .xls and easily import it to Excel.

The method CCplxPointAvgDlg::OnSelectFile() is called when the Select PSV Scan File button is pressed. It calls several other methods to collect the data and export it to an ASCII-File. Have a look at stdafx.h how to import the Polytec File Access type libraries via #import statements. A call to CoInitialize() has been added to CCplxPointAvgApp::InitInstance() and a call to CoUninitialize() has been added to CCplxPointAvgApp::ExitInstance().

#### CplxPointAvgSharp

You will find the example CplxPointAvgSharp in the folder Examples\DotNet\CplxPointAvgSharp.
 To run this sample do the following:

- Start Microsoft® Visual Studio® .NET 2013 or higher

- Open the workspace CplxPointAvgSharp.sln

- Build the project

- Run the application

- On the appearing dialog based application press the Select PSV Scan File button and select a PSV file taken in FFT mode

- Select a text file to store the complex average data

This sample shows how to access the point data of all valid measurement points of a PSV scan file and calculate the complex average of these points. This functionality is not built into PSV. PSV calculates an amplitude average of the points only. This dialog-based application exports the data to an ASCII-File. You can save the ASCII-File with the extension .xls and easily import it to Excel.

The method SelectFile_Click() is called when the Select PSV Scan File button is pressed. It calls several other methods to collect the data and export it to an ASCII-File.

The Polytec PolyFile Type Library has been added as a COM reference to the project. This will automatically include all necessary references and build the COM interop .dll's.

#### Matlab®

The folder Examples\Matlab contains Matlab .m files demonstrating retrieving data from Polytec files using Matlab®. Moreover the .m files allow to save Matlab® data in Polytec files as user-defined datasets.

To run this sample do the following:

- Start Matlab® R2006b or higher.

- In Matlab®, set the current directory to the Examples\Matlab folder.

- Choose a Polytec scan (.svd) or single point file (.pvd) containing time domain data and create a backup copy of this file.

- On the Matlab® command prompt type "help CalculateFFT" to get help on the CalculateFFT.m file.

- Type "CalculateFFT('Filename')" where 'Filename' is the fully qualified pathname to the Polytec file containing time domain data.

- To have a look at the data, open PSV or VibSoft, open the Polytec file that you have just processed, switch to domain 'FFT', channel 'Usr' and signal 'Matlab FFT'. The spectra you see have been calculated by Matlab® from the original time signals in the file and saved as user-defined datasets in this file.

#### Python

The folder Examples\Python contains the band_avearge.py file demonstrating to calculate the minimum, maximum, average, and geometric average of all frequency bands defined in a scan file. The calculated values are stored as user defined average signals over the scan point number in the Point Average domain.

To run this sample, do the following:

- Install a Python environment e.g., from https://www.python.org. Make sure to add python.exe to the PATH environment variable.

- Open a command prompt or PowerShell prompt with administrative rights.

- Install the necessary dependencies by executing the following commands:
 > pip install -U numpy pywin32 pillow matplotlib

- Navigate to the folder Examples\Python in the installation directory of Polytec File Access.
 > python.exe .\band_average.py

- The program asks for the name of a scanning file, warns about the modification of the file and calculates the data.

To view the calculated data, do the following:

- Open the modified scan file in the PSV Software.

- In the area view select View / Average Spectrum

- In the analyzer view select Channel / Usr

- The analyzer will display the user defined signal created by the Python script.

- Select frames 1, 2, 3, 4 to display the minimum, geometric average, average and maximum of the frequency bands versus the scan point index.

Moreover the folder Examples\Python contains Python files demonstrating retrieving data from Polytec files. To use these examples, do the following:

- Install python and the necessary dependencies as described above.

- Open a command prompt or PowerShell prompt.

- Navigate to the folder `Examples\Python` in the installation directory of Polytec File Access.

- Run a python console inside the PowerShell/CMD:
 > python.exe

- Import all functions in the python console:
 > from examples import *

- Type `help(calculate_fft)` into the python console or look into the code of `calculate_fft.py` to find documentation

- You can run these function to get and/or modify data, which can be opened in PSV or VibSoft afterward.

The `Enums.py` file shows how to use COM Enums in the python code. It does not provide a function like other examples.
