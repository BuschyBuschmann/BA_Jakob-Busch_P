# POLYFILELib – PolyFile

## PolyFile Object

*Quelle: `POLYFILELib~PolyFile.html` · Polytec PolyFile Type Library*

### Description

The PolyFile object represents a Polytec file.

### Object Model

### Remarks

This class can be instantiated using the string "PolyFile.PolyFile".

### Example


---

## PolyFile Object Members

*Quelle: `POLYFILELib~PolyFile_members.html` · Polytec PolyFile Type Library*

### Public Methods

| CalcBands | Calculates bands for data of original signals. |
|---|---|
| CalcBandsFromSignal | Calculates bands for the given signal. |
| Close | Closes a file. Files are closed automatically when the PolyFile object is deleted. You have to close the file prior to opening another file with the same PolyFile object. |
| CorrectAverageSpectrum | Calculates the corrected average spectrum for a given set of measurement points whose states have changed from valid to invalidated or vice versa. |
| Create | The create method allows you to create new Polytec files. |
| GetBandDomains | Returns the BandDomains collection. |
| GetPointAverageDomains | Returns the PointAverageDomains collection. |
| GetPointDomains | Returns the PointDomains collection. |
| IsDataPossible | Returns true, if data for the given data type is possible. |
| Open | Opens a file. The file is not allowed to be opened by another PolyFile object or by MPV/PSV/VibSoft applications. |
| Save | Commits all changes to all objects of this file to the file. |
| SaveAs | Copies contents of an existing file to a new file. What contents are copied depends on the value of the PTCSaveAs enumerator. |
| SaveAsEx | Same as SaveAs , only currently opened file will be used as source file. |
| TestWriteAccess | Test if a file with the given file path can be written. |

### Public Properties

| CombinedFile | Returns the parent combined file, if its a contained file in a combined file. |
|---|---|
| ContainedFiles | Returns the ContainedFiles collection for a combined file. |
| CurrentFileVersionNumber | Returns the current file version that is used for files, that are created with this version of PolyFile. |
| FileName | Specifies the file path you have specified in the Open method . |
| Infos | Returns the Infos collection. |
| IsAverageSpectrumCorrected | Returns whether the file contains an average spectrum corrected for invalidated measurement points. If so, the GetData and GetDataSection methods of the PointAverageDomain object automatically return the corrected average spectrum. |
| IsOpen | Returns whether the file is currently open. |
| Preferences | Returns the Preferences collection. |
| ReadOnly | Returns or specifies whether the file allows read access only. |
| SummaryInfo | Returns the SummaryInfo object. |
| UseGlobalDbReferences | Returns or specifies whether to use the global dB references from the Preferences collection or the local dB references from the Infos collection . |
| Version | Returns the Version object. |

### Events

| Finished | The finished event is raised, when the band calculation has finished. |
|---|---|
| FinishedHint | The finished hint event is raised, when the creation of a combined file has finished. |
| Start | The start event is raised, when the band calculation has started. |
| StartHint | The start hint event is raised, when the creation of a combined file has started. |
| Step | The step event is raised during the band calculation. |
| StepHint | The step hint event is fired during the creation of a combined file. |


---

## CalcBands Method

*Quelle: `POLYFILELib~PolyFile~CalcBands.html` · Polytec PolyFile Type Library · PolyFile Object : CalcBands Method*

### Description

Calculates bands for data of original signals.

### Syntax

*Visual Basic:*
```
Public Sub CalcBands( _
   ByVal pIBandDefs As IBandDefs3, _
   Optional ByVal ptcBandType As PTCBandType = ptcBandTypeAll _
)
```

### Parameters

pIBandDefs

A BandDefs collection.

ptcBandType

| Value | Description |
|---|---|
| ptcBandType3rdOctave | 3rd octave band. |
| ptcBandTypeAll | All band types. |
| ptcBandTypeEntire | The "Entire Bandwidth" band. |
| ptcBandTypeNone | No band type specified. |
| ptcBandTypeRms | RMS band. |
| ptcBandTypeSpectrum | FFT band. |
| ptcBandTypeTime | Time domain band. |
Desired Band Types.

### Remarks

To calculate bands for user-defined signals please use the CalcBandsFromSignal Method.


---

## CalcBandsFromSignal Method

*Quelle: `POLYFILELib~PolyFile~CalcBandsFromSignal.html` · Polytec PolyFile Type Library · PolyFile Object : CalcBandsFromSignal Method*

### Description

Calculates bands for the given signal.

### Syntax

*Visual Basic:*
```
Public Sub CalcBandsFromSignal( _
   ByVal pISignal As ISignal5, _
   ByVal pIBandDefs As IBandDefs3, _
   Optional ByVal ptcBandType As PTCBandType = ptcBandTypeAll _
)
```

### Parameters

pISignal

The user-defined signal to calculate the bands for. To get a suitable signal navigate through the PointDomains Collection returned by the GetPointDomains Method. The parameter can be Nothing. Then the bands for all original signals will be calculated.

pIBandDefs

A BandDefs collection.

ptcBandType

| Value | Description |
|---|---|
| ptcBandType3rdOctave | 3rd octave band. |
| ptcBandTypeAll | All band types. |
| ptcBandTypeEntire | The "Entire Bandwidth" band. |
| ptcBandTypeNone | No band type specified. |
| ptcBandTypeRms | RMS band. |
| ptcBandTypeSpectrum | FFT band. |
| ptcBandTypeTime | Time domain band. |
Desired Band Types.

### Remarks

You can calculate bands for original as well as user-defined signals with this method. You can only calculate bands for point data.


---

## Close Method

*Quelle: `POLYFILELib~PolyFile~Close.html` · Polytec PolyFile Type Library · PolyFile Object : Close Method*

### Description

Closes a file. Files are closed automatically when the PolyFile object is deleted. You have to close the file prior to opening another file with the same PolyFile object.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## CorrectAverageSpectrum Method

*Quelle: `POLYFILELib~PolyFile~CorrectAverageSpectrum.html` · Polytec PolyFile Type Library · PolyFile Object : CorrectAverageSpectrum Method*

### Description

Calculates the corrected average spectrum for a given set of measurement points whose states have changed from valid to invalidated or vice versa.

### Syntax

*Visual Basic:*
```
Public Sub CorrectAverageSpectrum( _
   ByVal pVal() As Long _
)
```

### Parameters

pVal

0-based, one dimensional array of 1-based measurement point indices.


---

## Create Method

*Quelle: `POLYFILELib~PolyFile~Create.html` · Polytec PolyFile Type Library · PolyFile Object : Create Method*

### Description

The create method allows you to create new Polytec files.

### Syntax

*Visual Basic:*
```
Public Sub Create( _
   ByVal bstrFilePath As String, _
   Optional ByVal ptcCreateFlag As PTCCreateFlags = ptcCreateAlways _
)
```

### Parameters

bstrFilePath

The path to the new file.

ptcCreateFlag

| Value | Description |
|---|---|
| ptcCreateAlways | The file will be always created. An existing file will be overwritten. |
| ptcCreateNone | No create flags. |
The create flags.

### Remarks

After creation the file is empty. To open and display the file e.g. in the PSV software you have to add user-defined signals and a geometry. The easiest way to add a geometry is copying the geometry from an existing file.

### Example

The following example shows how to create a new scan file, copy a geometry from an existing file, add a user-defined signal. The file created by this macro can then be opened using the MPV/PSV software.

This macro creates a new PSV scan file.

- Create a New PSV Scan File (Visual Basic)

```
Dim oFile As New PolyFile
oFile.Readonly = False
oFile.Create("D:\Temp\NewFile.svd")
Dim oVersion As Version
Set oVersion = oFile.Version
oVersion.FileID = ptcFileIDPSVFile
oFile.Save()
```

This macro copies the scan points and the coordinates of the scan points of an existing file to the new file

- Copy Scan Points (Visual Basic)

```
Dim oSrcFile As New PolyFile
oSrcFile.Open("D:\Temp\Ex CarDoor 3D.svd")

Dim oSrcMeasPoints As MeasPoints
Set oSrcMeasPoints = oSrcFile.Infos.MeasPoints
Dim oMeasPoints As MeasPoints
Set oMeasPoints = oFile.Infos.Add(ptcInfoMeasPoints)

Dim oSrcMeasPoint As MeasPoint
Dim oMeasPoint As MeasPoint
For Each oSrcMeasPoint In oSrcMeasPoints
    Set oMeasPoint = oMeasPoints.Add()
    Dim x As Double
    Dim y As Double
    Dim z As Double
    oSrcMeasPoint.CoordXYZ(x, y, z)
    oMeasPoint.SetCoordXYZ(x, y, z)
Next
```

This macro copies the elements of an existing file to the new file

- Copy Elements (Visual Basic)

```
Dim oSrcElements As Elements
Set oSrcElements = oSrcFile.Infos.Elements
Dim oElements As Elements
Set oElements = oFile.Infos.Add(ptcInfoElements)

oElements.AddRange(oSrcElements.ToArray(False), False)
```

This macro adds a user signal to the file and closes the source and destination files

- Add User Signal (Visual Basic)

```
Dim Data(0 To 99) As Single
Dim i As Integer
For i = 0 To 99
    Data(i) = Sin(2.0 * 3.141578 * i / 100.0)
Next i

Dim oUSD As New SignalDescription
oUSD.Name = "Sine"
oUSD.DataType = ptcDataPoint
oUSD.DomainType = ptcDomainTime
oUSD.FunctionType = ptcFunctionTimeResponseType
oUSD.XAxis.MaxCount = 100
oUSD.XAxis.Min = 0
oUSD.XAxis.Max = 100.0
oUSD.XAxis.Unit = "s"
oUSD.XAxis.Name = "Time"
oUSD.YAxis.Min = -1.0
oUSD.YAxis.Max = 1.0
oUSD.YAxis.Name = "Voltage"
oUSD.YAxis.Unit = "V"

oUSD.ResponseDOFs.Assign(0, ptcPlusZTranslation, "Usr", "Voltage", "V")

Dim oPointDomains As PointDomains
Set oPointDomains = oFile.GetPointDomains(ptcBuildPointData3d)

Dim oSignal As Signal
Set oSignal = oPointDomains.AddSignal(oUSD)

Dim oDataPoint As DataPoint
For Each oDataPoint In oPointDomains.type(ptcDomainTime).DataPoints
    oDataPoint.SetData(oSignal, 1, Data)
Next

oSrcFile.Close()
oFile.Save()
oFile.Close()
```


---

## GetBandDomains Method

*Quelle: `POLYFILELib~PolyFile~GetBandDomains.html` · Polytec PolyFile Type Library · PolyFile Object : GetBandDomains Method*

### Description

Returns the BandDomains collection.

### Syntax

*Visual Basic:*
```
Public Function GetBandDomains( _
   Optional ByVal ptcBuildFlags As PTCSignalBuildFlags = ptcBuildBandData3d _
) As BandDomains
```

### Parameters

ptcBuildFlags

| Value | Description |
|---|---|
| ptcBuildBandData3d | Combination of build flags for band data and 3d channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannel3d Or ptcBuildDisplayComplex Or ptcBuildDisplayPhase |
| ptcBuildBandDataXYZ | Combination of build flags for band data and x,y,z channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannelXYZ Or ptcBuildDisplayComplex Or ptcBuildDisplayPhase |
| ptcBuildChannel3d | Build the 3d channels (Usr 3D and/or Vib 3D). |
| ptcBuildChannelOriginal | Build the channels with the original signals. |
| ptcBuildChannelUser | Build the channel Usr. |
| ptcBuildChannelXYZ | Build the x,y,z channels (Usr X, Usr Y, Usr Z and/or Vib X, Vib Y, Vib Z). |
| ptcBuildDisplayComplex | Build complex displays (e.g. Real & Imag., Mag. & Phase). |
| ptcBuildDisplayInstVal | Build display Inst. Val. |
| ptcBuildDisplayNyquist | Build display Nyquist. |
| ptcBuildDisplayPhase | Build display phase. |
| ptcBuildDomain3rdOctave | Build domain 3rd Octave. |
| ptcBuildDomainAll | Build all domains. |
| ptcBuildDomainAngleSync | Build domain Angle Sync. |
| ptcBuildDomainOrderSpectrum | Build domain Order Spectrum. |
| ptcBuildDomainRms | Build domain RMS. |
| ptcBuildDomainSpectrum | Build domain Spectrum. |
| ptcBuildDomainTime | Build domain Time. |
| ptcBuildNothing | No build flags set. |
| ptcBuildPointData3d | Combination of build flags for point data or point average data and 3d channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannel3d Or ptcBuildDisplayComplex Or ptcBuildDisplayNyquist Or ptcBuildDisplayPhase |
| ptcBuildPointDataXYZ | Combination of build flags for point data or point average data and x,y,z channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannelXYZ Or ptcBuildDisplayComplex Or ptcBuildDisplayNyquist Or ptcBuildDisplayPhase |
Build flags for various signals.

### Remarks

When you want to add user-defined 3d bands you should specify the default ptcBuildBandData3d flag. When you want to access data in the x,y,z channels (Vib X, Vib Y, Vib Z and/or Usr X, Usr, Y, Usr Z) you should use the ptcBuildBandDataXYZ flag, instead.


---

## GetPointAverageDomains Method

*Quelle: `POLYFILELib~PolyFile~GetPointAverageDomains.html` · Polytec PolyFile Type Library · PolyFile Object : GetPointAverageDomains Method*

### Description

Returns the PointAverageDomains collection.

### Syntax

*Visual Basic:*
```
Public Function GetPointAverageDomains( _
   Optional ByVal ptcBuildFlags As PTCSignalBuildFlags = ptcBuildPointDataXYZ _
) As PointAverageDomains
```

### Parameters

ptcBuildFlags

| Value | Description |
|---|---|
| ptcBuildBandData3d | Combination of build flags for band data and 3d channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannel3d Or ptcBuildDisplayComplex Or ptcBuildDisplayPhase |
| ptcBuildBandDataXYZ | Combination of build flags for band data and x,y,z channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannelXYZ Or ptcBuildDisplayComplex Or ptcBuildDisplayPhase |
| ptcBuildChannel3d | Build the 3d channels (Usr 3D and/or Vib 3D). |
| ptcBuildChannelOriginal | Build the channels with the original signals. |
| ptcBuildChannelUser | Build the channel Usr. |
| ptcBuildChannelXYZ | Build the x,y,z channels (Usr X, Usr Y, Usr Z and/or Vib X, Vib Y, Vib Z). |
| ptcBuildDisplayComplex | Build complex displays (e.g. Real & Imag., Mag. & Phase). |
| ptcBuildDisplayInstVal | Build display Inst. Val. |
| ptcBuildDisplayNyquist | Build display Nyquist. |
| ptcBuildDisplayPhase | Build display phase. |
| ptcBuildDomain3rdOctave | Build domain 3rd Octave. |
| ptcBuildDomainAll | Build all domains. |
| ptcBuildDomainAngleSync | Build domain Angle Sync. |
| ptcBuildDomainOrderSpectrum | Build domain Order Spectrum. |
| ptcBuildDomainRms | Build domain RMS. |
| ptcBuildDomainSpectrum | Build domain Spectrum. |
| ptcBuildDomainTime | Build domain Time. |
| ptcBuildNothing | No build flags set. |
| ptcBuildPointData3d | Combination of build flags for point data or point average data and 3d channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannel3d Or ptcBuildDisplayComplex Or ptcBuildDisplayNyquist Or ptcBuildDisplayPhase |
| ptcBuildPointDataXYZ | Combination of build flags for point data or point average data and x,y,z channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannelXYZ Or ptcBuildDisplayComplex Or ptcBuildDisplayNyquist Or ptcBuildDisplayPhase |
Build flags for various signals.

### Remarks

When you want to add user-defined 3d signals you should specify the ptcBuildPointData3d flag. When you want to access data in the x,y,z channels (Vib X, Vib Y, Vib Z and/or Usr X, Usr, Y, Usr Z) you should use the default ptcBuildPointDataXYZ flag, instead.


---

## GetPointDomains Method

*Quelle: `POLYFILELib~PolyFile~GetPointDomains.html` · Polytec PolyFile Type Library · PolyFile Object : GetPointDomains Method*

### Description

Returns the PointDomains collection.

### Syntax

*Visual Basic:*
```
Public Function GetPointDomains( _
   Optional ByVal ptcBuildFlags As PTCSignalBuildFlags = ptcBuildPointDataXYZ _
) As PointDomains
```

### Parameters

ptcBuildFlags

| Value | Description |
|---|---|
| ptcBuildBandData3d | Combination of build flags for band data and 3d channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannel3d Or ptcBuildDisplayComplex Or ptcBuildDisplayPhase |
| ptcBuildBandDataXYZ | Combination of build flags for band data and x,y,z channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannelXYZ Or ptcBuildDisplayComplex Or ptcBuildDisplayPhase |
| ptcBuildChannel3d | Build the 3d channels (Usr 3D and/or Vib 3D). |
| ptcBuildChannelOriginal | Build the channels with the original signals. |
| ptcBuildChannelUser | Build the channel Usr. |
| ptcBuildChannelXYZ | Build the x,y,z channels (Usr X, Usr Y, Usr Z and/or Vib X, Vib Y, Vib Z). |
| ptcBuildDisplayComplex | Build complex displays (e.g. Real & Imag., Mag. & Phase). |
| ptcBuildDisplayInstVal | Build display Inst. Val. |
| ptcBuildDisplayNyquist | Build display Nyquist. |
| ptcBuildDisplayPhase | Build display phase. |
| ptcBuildDomain3rdOctave | Build domain 3rd Octave. |
| ptcBuildDomainAll | Build all domains. |
| ptcBuildDomainAngleSync | Build domain Angle Sync. |
| ptcBuildDomainOrderSpectrum | Build domain Order Spectrum. |
| ptcBuildDomainRms | Build domain RMS. |
| ptcBuildDomainSpectrum | Build domain Spectrum. |
| ptcBuildDomainTime | Build domain Time. |
| ptcBuildNothing | No build flags set. |
| ptcBuildPointData3d | Combination of build flags for point data or point average data and 3d channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannel3d Or ptcBuildDisplayComplex Or ptcBuildDisplayNyquist Or ptcBuildDisplayPhase |
| ptcBuildPointDataXYZ | Combination of build flags for point data or point average data and x,y,z channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannelXYZ Or ptcBuildDisplayComplex Or ptcBuildDisplayNyquist Or ptcBuildDisplayPhase |
Build flags for various signals.

### Remarks

When you want to add user-defined 3d signals you should specify the ptcBuildPointData3d flag. When you want to access data in the x,y,z channels (Vib X, Vib Y, Vib Z and/or Usr X, Usr, Y, Usr Z) you should use the default ptcBuildPointDataXYZ flag, instead.


---

## IsDataPossible Method

*Quelle: `POLYFILELib~PolyFile~IsDataPossible.html` · Polytec PolyFile Type Library · PolyFile Object : IsDataPossible Method*

### Description

Returns true, if data for the given data type is possible.

### Syntax

*Visual Basic:*
```
Public Function IsDataPossible( _
   ByVal ptcDataType As PTCDataType _
) As Boolean
```

### Parameters

ptcDataType

| Value | Description |
|---|---|
| ptcDataAverage | Point average data. |
| ptcDataBand | Band data. |
| ptcDataPoint | Point domain data. |
| ptcDataUnknown | The data type is unknown. |
The type of the data.


---

## Open Method

*Quelle: `POLYFILELib~PolyFile~Open.html` · Polytec PolyFile Type Library · PolyFile Object : Open Method*

### Description

Opens a file. The file is not allowed to be opened by another PolyFile object or by MPV/PSV/VibSoft applications.

### Syntax

*Visual Basic:*
```
Public Sub Open( _
   ByVal bstrFilePath As String _
)
```

### Parameters

bstrFilePath

Name and path of the file.

### Remarks

You can pass an empty string as name and path of the file, when you have set the FileName Property before.


---

## Save Method

*Quelle: `POLYFILELib~PolyFile~Save.html` · Polytec PolyFile Type Library · PolyFile Object : Save Method*

### Description

Commits all changes to all objects of this file to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```

### Remarks

The save method will generate a combined file if contained files are added to a non opened PolyFile object.


---

## SaveAs Method

*Quelle: `POLYFILELib~PolyFile~SaveAs.html` · Polytec PolyFile Type Library · PolyFile Object : SaveAs Method*

### Description

Copies contents of an existing file to a new file. What contents are copied depends on the value of the PTCSaveAs enumerator.

### Syntax

*Visual Basic:*
```
Public Sub SaveAs( _
   ByVal PTCSaveAs As PTCSaveAs, _
   ByVal bstrFileNameSrc As String, _
   ByVal bstrFileNameDest As String, _
   Optional ByVal lIndex As Long = -1 _
)
```

### Parameters

PTCSaveAs

| Value | Description |
|---|---|
| ptcSaveAsAll | Save the complete file. Deprecated, see remarks. |
| ptcSaveAsAverageSpectrum | Save the average spectrum of a PSV scan file. Note that GetData or GetDataSection of such a file return the uncorrected average spectrum only. |
| ptcSaveAsBands | Save bands of a PSV scan file. Deprecated, see remarks. |
| ptcSaveAsSinglePoint | Save single measurement point data of a PSV scan file - specify the point index. Deprecated, see remarks. |
| ptcSaveAsTypeAll | Save the complete file. |
| ptcSaveAsTypeAllNoOriginal | Save the complete file with the user-defined data excluding the original single point and average spectrum data. |
| ptcSaveAsTypeAllNoSinglePoint | Save the complete file with the user-defined data excluding the original single point but including the average spectrum data. |
| ptcSaveAsTypeAllNoUser | Save the complete file excluding the user-defined data. |
| ptcSaveAsTypeAverageSpectrum | Save the average spectrum of a PSV scan file. |
| ptcSaveAsTypeAverageSpectrumUser | Save user data for the average spectrum of a PSV scan file. |
| ptcSaveAsTypeBands | Save bands only. |
| ptcSaveAsTypeBandsUser | Save user-defined bands. |
| ptcSaveAsTypeInfos | Save Infos only (as a Settings file if no other option is selected). |
| ptcSaveAsTypeSinglePoint | Save single measurement point data of a MPV/PSV measurement file  specify a valid point index. |
| ptcSaveAsTypeSinglePointUser | Save user data for a single measurement point of a MPV/PSV measurement file  specify a valid point index. |
Specifies what to save.

bstrFileNameSrc

Path to the source file, see remarks.

bstrFileNameDest

Path to the new file.

lIndex

1-based measurement point index, see remarks.

### Remarks

The parameter PointIndex is only valid for creating single point files from PSV scan files and will be ignored in all other cases.

If a blank source filename is supplied the currently open file will be copied.

See also the remarks of the PTCSaveAs enumeration.


---

## SaveAsEx Method

*Quelle: `POLYFILELib~PolyFile~SaveAsEx.html` · Polytec PolyFile Type Library · PolyFile Object : SaveAsEx Method*

### Description

Same as SaveAs, only currently opened file will be used as source file.

### Syntax

*Visual Basic:*
```
Public Sub SaveAsEx( _
   ByVal PTCSaveAs As PTCSaveAs, _
   ByVal bstrFileNameDest As String, _
   Optional ByVal lIndex As Long = -1 _
)
```

### Parameters

PTCSaveAs

| Value | Description |
|---|---|
| ptcSaveAsAll | Save the complete file. Deprecated, see remarks. |
| ptcSaveAsAverageSpectrum | Save the average spectrum of a PSV scan file. Note that GetData or GetDataSection of such a file return the uncorrected average spectrum only. |
| ptcSaveAsBands | Save bands of a PSV scan file. Deprecated, see remarks. |
| ptcSaveAsSinglePoint | Save single measurement point data of a PSV scan file - specify the point index. Deprecated, see remarks. |
| ptcSaveAsTypeAll | Save the complete file. |
| ptcSaveAsTypeAllNoOriginal | Save the complete file with the user-defined data excluding the original single point and average spectrum data. |
| ptcSaveAsTypeAllNoSinglePoint | Save the complete file with the user-defined data excluding the original single point but including the average spectrum data. |
| ptcSaveAsTypeAllNoUser | Save the complete file excluding the user-defined data. |
| ptcSaveAsTypeAverageSpectrum | Save the average spectrum of a PSV scan file. |
| ptcSaveAsTypeAverageSpectrumUser | Save user data for the average spectrum of a PSV scan file. |
| ptcSaveAsTypeBands | Save bands only. |
| ptcSaveAsTypeBandsUser | Save user-defined bands. |
| ptcSaveAsTypeInfos | Save Infos only (as a Settings file if no other option is selected). |
| ptcSaveAsTypeSinglePoint | Save single measurement point data of a MPV/PSV measurement file  specify a valid point index. |
| ptcSaveAsTypeSinglePointUser | Save user data for a single measurement point of a MPV/PSV measurement file  specify a valid point index. |
Specifies what to save.

bstrFileNameDest

Path to the new file.

lIndex

1-based measurement point index, see remarks.

### Remarks

The parameter PointIndex is only valid for creating single point files from PSV scan files and will be ignored in all other cases.

If a blank source filename is supplied the currently open file will be copied.

See also the remarks of the PTCSaveAs enumeration.


---

## TestWriteAccess Method

*Quelle: `POLYFILELib~PolyFile~TestWriteAccess.html` · Polytec PolyFile Type Library · PolyFile Object : TestWriteAccess Method*

### Description

Test if a file with the given file path can be written.

### Syntax

*Visual Basic:*
```
Public Function TestWriteAccess( _
   ByVal bstrFileName As String _
) As Boolean
```

### Parameters

bstrFileName

Name and path of the file.


---

## CombinedFile Property

*Quelle: `POLYFILELib~PolyFile~CombinedFile.html` · Polytec PolyFile Type Library · PolyFile Object : CombinedFile Property*

### Description

Returns the parent combined file, if its a contained file in a combined file.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CombinedFile As PolyFile
```


---

## ContainedFiles Property

*Quelle: `POLYFILELib~PolyFile~ContainedFiles.html` · Polytec PolyFile Type Library · PolyFile Object : ContainedFiles Property*

### Description

Returns the ContainedFiles collection for a combined file.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ContainedFiles As ContainedFiles
```

### Remarks

Returns an empty collection for a single file.


---

## CurrentFileVersionNumber Property

*Quelle: `POLYFILELib~PolyFile~CurrentFileVersionNumber.html` · Polytec PolyFile Type Library · PolyFile Object : CurrentFileVersionNumber Property*

### Description

Returns the current file version that is used for files, that are created with this version of PolyFile.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CurrentFileVersionNumber As Long
```

### Return Type

The file version is returned in hexadecimal format. E.g. means a value of 0x860 that the file version is 8.6.


---

## FileName Property

*Quelle: `POLYFILELib~PolyFile~FileName.html` · Polytec PolyFile Type Library · PolyFile Object : FileName Property*

### Description

Specifies the file path you have specified in the Open method.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FileName As String
```

### Remarks

If the file has not been opened and the property has not been set, reading this property will fail. You can set the file path before calling Open. Then you can pass an empty string to Open.


---

## Infos Property

*Quelle: `POLYFILELib~PolyFile~Infos.html` · Polytec PolyFile Type Library · PolyFile Object : Infos Property*

### Description

Returns the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Infos As Infos
```


---

## IsAverageSpectrumCorrected Property

*Quelle: `POLYFILELib~PolyFile~IsAverageSpectrumCorrected.html` · Polytec PolyFile Type Library · PolyFile Object : IsAverageSpectrumCorrected Property*

### Description

Returns whether the file contains an average spectrum corrected for invalidated measurement points. If so, the GetData and GetDataSection methods of the PointAverageDomain object automatically return the corrected average spectrum.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsAverageSpectrumCorrected As Boolean
```


---

## IsOpen Property

*Quelle: `POLYFILELib~PolyFile~IsOpen.html` · Polytec PolyFile Type Library · PolyFile Object : IsOpen Property*

### Description

Returns whether the file is currently open.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsOpen As Boolean
```


---

## Preferences Property

*Quelle: `POLYFILELib~PolyFile~Preferences.html` · Polytec PolyFile Type Library · PolyFile Object : Preferences Property*

### Description

Returns the Preferences collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Preferences As Preferences
```


---

## ReadOnly Property

*Quelle: `POLYFILELib~PolyFile~ReadOnly.html` · Polytec PolyFile Type Library · PolyFile Object : ReadOnly Property*

### Description

Returns or specifies whether the file allows read access only.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ReadOnly As Boolean
```

### Remarks

If you change the value of this property all current references to any other objects of Polytec File Access are not valid anymore.


---

## SummaryInfo Property

*Quelle: `POLYFILELib~PolyFile~SummaryInfo.html` · Polytec PolyFile Type Library · PolyFile Object : SummaryInfo Property*

### Description

Returns the SummaryInfo object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SummaryInfo As SummaryInfo
```


---

## UseGlobalDbReferences Property

*Quelle: `POLYFILELib~PolyFile~UseGlobalDbReferences.html` · Polytec PolyFile Type Library · PolyFile Object : UseGlobalDbReferences Property*

### Description

Returns or specifies whether to use the global dB references from the Preferences collection or the local dB references from the Infos collection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property UseGlobalDbReferences As Boolean
```


---

## Version Property

*Quelle: `POLYFILELib~PolyFile~Version.html` · Polytec PolyFile Type Library · PolyFile Object : Version Property*

### Description

Returns the Version object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Version As Version
```


---

## Finished Event

*Quelle: `POLYFILELib~PolyFile~Finished_EV.html` · Polytec PolyFile Type Library · PolyFile Object : Finished Event*

### Description

The finished event is raised, when the band calculation has finished.

### Syntax

*Visual Basic:*
```
Public Event Finished()
```


---

## FinishedHint Event

*Quelle: `POLYFILELib~PolyFile~FinishedHint_EV.html` · Polytec PolyFile Type Library · PolyFile Object : FinishedHint Event*

### Description

The finished hint event is raised, when the creation of a combined file has finished.

### Syntax

*Visual Basic:*
```
Public Event FinishedHint()
```


---

## Start Event

*Quelle: `POLYFILELib~PolyFile~Start_EV.html` · Polytec PolyFile Type Library · PolyFile Object : Start Event*

### Description

The start event is raised, when the band calculation has started.

### Syntax

*Visual Basic:*
```
Public Event Start( _
   ByVal Steps As Long _
)
```

### Parameters

Steps

The number of steps for the band calculation.


---

## StartHint Event

*Quelle: `POLYFILELib~PolyFile~StartHint_EV.html` · Polytec PolyFile Type Library · PolyFile Object : StartHint Event*

### Description

The start hint event is raised, when the creation of a combined file has started.

### Syntax

*Visual Basic:*
```
Public Event StartHint( _
   ByVal Steps As Long _
)
```

### Parameters

Steps

The expected number of steps for the creation of the combined file.


---

## Step Event

*Quelle: `POLYFILELib~PolyFile~Step_EV.html` · Polytec PolyFile Type Library · PolyFile Object : Step Event*

### Description

The step event is raised during the band calculation.

### Syntax

*Visual Basic:*
```
Public Event Step( _
   ByVal StepNumber As Long, _
   ByRef vbCancel As Boolean _
)
```

### Parameters

StepNumber

The current step number of the band calculation.

vbCancel

Set this property to true to cancel the band calculation.


---

## StepHint Event

*Quelle: `POLYFILELib~PolyFile~StepHint_EV.html` · Polytec PolyFile Type Library · PolyFile Object : StepHint Event*

### Description

The step hint event is fired during the creation of a combined file.

### Syntax

*Visual Basic:*
```
Public Event StepHint( _
   ByVal StepNumber As Long, _
   ByVal Hint As String, _
   ByRef vbCancel As Boolean _
)
```

### Parameters

StepNumber

The current step number of the creation of a combined file.

Hint

The hint that informs which part of the creation of the combined file is in progress.

vbCancel

Set this parameter to true to cancel the creation of a combined file.
