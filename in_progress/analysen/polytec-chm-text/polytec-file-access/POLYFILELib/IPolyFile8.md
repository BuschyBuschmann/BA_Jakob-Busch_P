# POLYFILELib – IPolyFile8

## IPolyFile8 Interface

*Quelle: `POLYFILELib~IPolyFile8.html` · Polytec PolyFile Type Library*

### Description

The PolyFile object represents a Polytec file.

### Object Model

### Remarks

It is recommended to cast to the PolyFile object.


---

## IPolyFile8 Interface Members

*Quelle: `POLYFILELib~IPolyFile8_members.html` · Polytec PolyFile Type Library*

### Public Methods

| CalcBands | Calculates bands for data of original signals. |
|---|---|
| Close | Closes a file. Files are closed automatically when the PolyFile object is deleted. You have to close the file prior to opening another file with the same PolyFile object. |
| CorrectAverageSpectrum | Calculates the corrected average spectrum for a given set of measurement points whose states have changed from valid to invalidated or vice versa. |
| Open | Opens a file. The file is not allowed to be opened by another PolyFile object or by MPV/PSV/VibSoft applications. |
| Save | Commits all changes to all objects of this file to the file. |
| SaveAs | Copies contents of an existing file to a new file. What contents are copied depends on the value of the PTCSaveAs enumerator. |
| SaveAsEx | Same as SaveAs , only currently opened file will be used as source file. |
| TestWriteAccess | Test if a file with the given file path can be written. |

### Public Properties

| CombinedFile | Returns the parent combined file, if its a contained file in a combined file. |
|---|---|
| ContainedFiles | Returns the ContainedFiles collection for a combined file. |
| FileName | Specifies the file path you have specified in the Open method . |
| Infos | Returns the Infos collection. |
| IsAverageSpectrumCorrected | Returns whether the file contains an average spectrum corrected for invalidated measurement points. If so, the GetData and GetDataSection methods of the PointAverageDomain object automatically return the corrected average spectrum. |
| IsOpen | Returns whether the file is currently open. |
| Preferences | Returns the Preferences collection. |
| ReadOnly | Returns or specifies whether the file allows read access only. |
| SummaryInfo | Returns the SummaryInfo object. |
| UseGlobalDbReferences | Returns or specifies whether to use the global dB references from the Preferences collection or the local dB references from the Infos collection . |
| Version | Returns the Version object. |


---

## CalcBands Method

*Quelle: `POLYFILELib~IPolyFile8~CalcBands.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : CalcBands Method*

### Description

Calculates bands for data of original signals.

### Syntax

*Visual Basic:*
```
Public Sub CalcBands( _
   ByVal pIBandDefs As IBandDefs, _
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

## Close Method

*Quelle: `POLYFILELib~IPolyFile8~Close.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : Close Method*

### Description

Closes a file. Files are closed automatically when the PolyFile object is deleted. You have to close the file prior to opening another file with the same PolyFile object.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## CorrectAverageSpectrum Method

*Quelle: `POLYFILELib~IPolyFile8~CorrectAverageSpectrum.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : CorrectAverageSpectrum Method*

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

## Open Method

*Quelle: `POLYFILELib~IPolyFile8~Open.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : Open Method*

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

*Quelle: `POLYFILELib~IPolyFile8~Save.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : Save Method*

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

*Quelle: `POLYFILELib~IPolyFile8~SaveAs.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : SaveAs Method*

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

*Quelle: `POLYFILELib~IPolyFile8~SaveAsEx.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : SaveAsEx Method*

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

*Quelle: `POLYFILELib~IPolyFile8~TestWriteAccess.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : TestWriteAccess Method*

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

*Quelle: `POLYFILELib~IPolyFile8~CombinedFile.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : CombinedFile Property*

### Description

Returns the parent combined file, if its a contained file in a combined file.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CombinedFile As IPolyFile8
```


---

## ContainedFiles Property

*Quelle: `POLYFILELib~IPolyFile8~ContainedFiles.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : ContainedFiles Property*

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

## FileName Property

*Quelle: `POLYFILELib~IPolyFile8~FileName.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : FileName Property*

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

*Quelle: `POLYFILELib~IPolyFile8~Infos.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : Infos Property*

### Description

Returns the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Infos As IInfos2
```


---

## IsAverageSpectrumCorrected Property

*Quelle: `POLYFILELib~IPolyFile8~IsAverageSpectrumCorrected.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : IsAverageSpectrumCorrected Property*

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

*Quelle: `POLYFILELib~IPolyFile8~IsOpen.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : IsOpen Property*

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

*Quelle: `POLYFILELib~IPolyFile8~Preferences.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : Preferences Property*

### Description

Returns the Preferences collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Preferences As IPreferences
```


---

## ReadOnly Property

*Quelle: `POLYFILELib~IPolyFile8~ReadOnly.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : ReadOnly Property*

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

*Quelle: `POLYFILELib~IPolyFile8~SummaryInfo.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : SummaryInfo Property*

### Description

Returns the SummaryInfo object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SummaryInfo As ISummaryInfo2
```


---

## UseGlobalDbReferences Property

*Quelle: `POLYFILELib~IPolyFile8~UseGlobalDbReferences.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : UseGlobalDbReferences Property*

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

*Quelle: `POLYFILELib~IPolyFile8~Version.html` · Polytec PolyFile Type Library · IPolyFile8 Interface : Version Property*

### Description

Returns the Version object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Version As IVersion2
```
