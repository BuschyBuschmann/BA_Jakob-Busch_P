# POLYFILELib – IMeasPoint9

## IMeasPoint9 Interface

*Quelle: `POLYFILELib~IMeasPoint9.html` · Polytec PolyFile Type Library*

### Description

IMeasPoint9 Interface

### Object Model

### Remarks

It is recommended to cast to the MeasPoint object.


---

## IMeasPoint9 Interface Members

*Quelle: `POLYFILELib~IMeasPoint9_members.html` · Polytec PolyFile Type Library*

### Public Methods

| CoordXYZ | Retrieves the 3D coordinate of the measurement point. |
|---|---|
| SetCoordXYZ | Sets the 3D coordinate of the measurement point. |
| SetVideoXY | Sets the video coordinate of the measurement point. |
| ToggleValidInvalidated | Toggles the invalidated state of the measurement point. |
| VideoXY | Retrieves the video coordinate of the measurement point. |

### Public Properties

| AverageCount | Returns the average count for the measurement point. |
|---|---|
| Component | Returns the geometry component this point belongs to. |
| ContainedFileActiveID | Returns the identifier of the contained file of the measurement point in a combined file (ptcFileIDCombinedFile). |
| ContainedFileActiveMPIndex | Returns the measurement point index of the active contained file (only valid for a combined file - ptcFileIDCombinedFile). The measurement point index can be used as an index to the active ContainedFile's measurement point collection (see ContainedFileActiveID Property ). |
| ContainedFileIndex | Returns the contained file index of the measurement point in a combined file (ptcFileIDCombinedFile). The contained file index can be used as an index to the ContainedFiles collection . |
| ContainedFileMeasPointIndex | Returns the measurement point index of the contained file (only valid for a combined file - ptcFileIDCombinedFile). The measurement point index can be used as an index to the ContainedFile's measurement point collection (see ContainedFileIndex ). |
| FocusStatus | Returns a bit-pattern of the laser focus status (OFV 5000 series only). To test for status bits use the And operator to mask the status with one or several of the bit constants of PTCFocusStatus . |
| FocusValues | Returns or sets the laser focus values of the measurement point. |
| GeometryStatus | Returns a bit-pattern of the 3D geometry status. To test for status bits use the And operator to mask the status with one or several of the bit constants of PTCGeometryStatus . |
| Index | Returns the measurement point index. Can be used as an index to the MeasPoints collection . |
| Label | Returns or sets the label of the measurement point. The label is shown in the MPV/PSV software as the measurement point index. |
| MinSigma | Returns the minimum signal enhancement sigma. |
| ScanDistances | Returns the Distances from the scanning heads front panel (for scanner angle 0/0) to the measurement point. |
| ScanQuantitiesX | Returns the scanner X values of the measurement point. |
| ScanQuantitiesY | Returns the scanner Y values of the measurement point. |
| ScanQuantity | Returns the physical quantity for the ScanQuantities of the measurement point. |
| ScanStatus | Returns a bit-pattern of the measurement status. To test for status bits use the And operator to mask the status with one or several of the bit constants of PTCScanStatus . |
| ScanStatusDisabled | Returns true if the scan status is disabled or false if the scan status is not disabled. Sets or resets the ScanStatusDisabled flag. |
| Sigma | Returns the signal enhancement sigma. |
| VibrometerRange | Returns the vibrometer range this point was measured with. |


---

## CoordXYZ Method

*Quelle: `POLYFILELib~IMeasPoint9~CoordXYZ.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : CoordXYZ Method*

### Description

Retrieves the 3D coordinate of the measurement point.

### Syntax

*Visual Basic:*
```
Public Sub CoordXYZ( _
   ByRef pdX As Double, _
   ByRef pdY As Double, _
   ByRef pdZ As Double _
)
```

### Parameters

pdX

X-value of 3D coordinate

pdY

Y-value of 3D coordinate

pdZ

Z-value of 3D coordinate


---

## SetCoordXYZ Method

*Quelle: `POLYFILELib~IMeasPoint9~SetCoordXYZ.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : SetCoordXYZ Method*

### Description

Sets the 3D coordinate of the measurement point.

### Syntax

*Visual Basic:*
```
Public Sub SetCoordXYZ( _
   ByVal dX As Double, _
   ByVal dY As Double, _
   ByVal dZ As Double _
)
```

### Parameters

dX

X-value of 3D coordinate

dY

Y-value of 3D coordinate

dZ

Z-value of 3D coordinate

### Remarks

The 3D coordinate can only be changed for a MPV/PSV settings file if the geometry was generated in the APS point mode.

### Example


---

## SetVideoXY Method

*Quelle: `POLYFILELib~IMeasPoint9~SetVideoXY.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : SetVideoXY Method*

### Description

Sets the video coordinate of the measurement point.

### Syntax

*Visual Basic:*
```
Public Sub SetVideoXY( _
   ByVal fX As Single, _
   ByVal fY As Single _
)
```

### Parameters

fX

X-value of video coordinate

fY

Y-value of video coordinate

### Remarks

The video coordinate can only be changed for a MPV/PSV settings file and if the geometry was generated in the APS point mode. The coordinates are in the coordinate system defined by the rectangle returned by the GetVideoRect Method.


---

## ToggleValidInvalidated Method

*Quelle: `POLYFILELib~IMeasPoint9~ToggleValidInvalidated.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ToggleValidInvalidated Method*

### Description

Toggles the invalidated state of the measurement point.

### Syntax

*Visual Basic:*
```
Public Sub ToggleValidInvalidated()
```


---

## VideoXY Method

*Quelle: `POLYFILELib~IMeasPoint9~VideoXY.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : VideoXY Method*

### Description

Retrieves the video coordinate of the measurement point.

### Syntax

*Visual Basic:*
```
Public Sub VideoXY( _
   ByRef pfX As Single, _
   ByRef pfY As Single _
)
```

### Parameters

pfX

X-value of video coordinate

pfY

Y-value of video coordinate

### Remarks

The returned coordinates are in the coordinate system defined by the rectangle returned by the GetVideoRect Method.


---

## AverageCount Property

*Quelle: `POLYFILELib~IMeasPoint9~AverageCount.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : AverageCount Property*

### Description

Returns the average count for the measurement point.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AverageCount As Long
```

### Remarks

This is the number of averages that contributed to the measurement result at this measurement point. For the average blocks that are stored in the data see the AverageCount property of the DataPoint object.


---

## Component Property

*Quelle: `POLYFILELib~IMeasPoint9~Component.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : Component Property*

### Description

Returns the geometry component this point belongs to.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Component As GeometryComponent
```


---

## ContainedFileActiveID Property

*Quelle: `POLYFILELib~IMeasPoint9~ContainedFileActiveID.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ContainedFileActiveID Property*

### Description

Returns the identifier of the contained file of the measurement point in a combined file (ptcFileIDCombinedFile).

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ContainedFileActiveID As Long
```

### Remarks

The contained file identifier is a one-based index of the contained file, that itself is not a combined file. The identifier is created by visiting all contained files recursively and depth-first via the ContainedFiles collection and is incremented every time a contained file does not contain files.


---

## ContainedFileActiveMPIndex Property

*Quelle: `POLYFILELib~IMeasPoint9~ContainedFileActiveMPIndex.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ContainedFileActiveMPIndex Property*

### Description

Returns the measurement point index of the active contained file (only valid for a combined file - ptcFileIDCombinedFile). The measurement point index can be used as an index to the active ContainedFile's measurement point collection (see ContainedFileActiveID Property).

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ContainedFileActiveMPIndex As Long
```


---

## ContainedFileIndex Property

*Quelle: `POLYFILELib~IMeasPoint9~ContainedFileIndex.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ContainedFileIndex Property*

### Description

Returns the contained file index of the measurement point in a combined file (ptcFileIDCombinedFile). The contained file index can be used as an index to the ContainedFiles collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ContainedFileIndex As Long
```


---

## ContainedFileMeasPointIndex Property

*Quelle: `POLYFILELib~IMeasPoint9~ContainedFileMeasPointIndex.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ContainedFileMeasPointIndex Property*

### Description

Returns the measurement point index of the contained file (only valid for a combined file - ptcFileIDCombinedFile). The measurement point index can be used as an index to the ContainedFile's measurement point collection (see ContainedFileIndex).

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ContainedFileMeasPointIndex As Long
```


---

## FocusStatus Property

*Quelle: `POLYFILELib~IMeasPoint9~FocusStatus.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : FocusStatus Property*

### Description

Returns a bit-pattern of the laser focus status (OFV 5000 series only). To test for status bits use the And operator to mask the status with one or several of the bit constants of PTCFocusStatus.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusStatus As PTCFocusStatus
```

### Example


---

## FocusValues Property

*Quelle: `POLYFILELib~IMeasPoint9~FocusValues.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : FocusValues Property*

### Description

Returns or sets the laser focus values of the measurement point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FocusValues As Long()
```

### Return Type

0-based, one dimensional array of integer values for all scanning heads.

### Remarks

Setting the values is supported only for settings files (.set) not for measurement files (.svd, .pvd, .mpd),


---

## GeometryStatus Property

*Quelle: `POLYFILELib~IMeasPoint9~GeometryStatus.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : GeometryStatus Property*

### Description

Returns a bit-pattern of the 3D geometry status. To test for status bits use the And operator to mask the status with one or several of the bit constants of PTCGeometryStatus.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GeometryStatus As PTCGeometryStatus
```


---

## Index Property

*Quelle: `POLYFILELib~IMeasPoint9~Index.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : Index Property*

### Description

Returns the measurement point index. Can be used as an index to the MeasPoints collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Index As Long
```


---

## Label Property

*Quelle: `POLYFILELib~IMeasPoint9~Label.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : Label Property*

### Description

Returns or sets the label of the measurement point. The label is shown in the MPV/PSV software as the measurement point index.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Label As Long
```


---

## MinSigma Property

*Quelle: `POLYFILELib~IMeasPoint9~MinSigma.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : MinSigma Property*

### Description

Returns the minimum signal enhancement sigma.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinSigma As Single
```

### Remarks

Sigma is an indicator for the noise level that depends logarithmically on the amplitude of the frequency lines of the spectrum. Only the frequency lines with the lowest amplitudes are taken into account. You can use the sigma indicator only for a relative analysis. The absolute value of this indicator does not have a meaning.

### Example


---

## ScanDistances Property

*Quelle: `POLYFILELib~IMeasPoint9~ScanDistances.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ScanDistances Property*

### Description

Returns the Distances from the scanning heads front panel (for scanner angle 0/0) to the measurement point.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanDistances As Double()
```

### Return Type

0-based, one dimensional array of double values for all scanning heads.


---

## ScanQuantitiesX Property

*Quelle: `POLYFILELib~IMeasPoint9~ScanQuantitiesX.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ScanQuantitiesX Property*

### Description

Returns the scanner X values of the measurement point.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanQuantitiesX As Double()
```

### Return Type

0-based, one dimensional array of double values for all scanning heads.


---

## ScanQuantitiesY Property

*Quelle: `POLYFILELib~IMeasPoint9~ScanQuantitiesY.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ScanQuantitiesY Property*

### Description

Returns the scanner Y values of the measurement point.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanQuantitiesY As Double()
```

### Return Type

0-based, one dimensional array of double values for all scanning heads.


---

## ScanQuantity Property

*Quelle: `POLYFILELib~IMeasPoint9~ScanQuantity.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ScanQuantity Property*

### Description

Returns the physical quantity for the ScanQuantities of the measurement point.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanQuantity As PTCPhysicalQuantity
```

### Return Type

The physical quantity can be one of the following PTCPhysicalQuantity constants:

| ptcPhysicalQuantityAngle | Scanner from default scanning head |
|---|---|
| ptcPhysicalQuantityDisplacement | Scanner from MSV or MSA scanning head |


---

## ScanStatus Property

*Quelle: `POLYFILELib~IMeasPoint9~ScanStatus.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ScanStatus Property*

### Description

Returns a bit-pattern of the measurement status. To test for status bits use the And operator to mask the status with one or several of the bit constants of PTCScanStatus.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanStatus As PTCScanStatus
```


---

## ScanStatusDisabled Property

*Quelle: `POLYFILELib~IMeasPoint9~ScanStatusDisabled.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : ScanStatusDisabled Property*

### Description

Returns true if the scan status is disabled or false if the scan status is not disabled. Sets or resets the ScanStatusDisabled flag.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScanStatusDisabled As Boolean
```


---

## Sigma Property

*Quelle: `POLYFILELib~IMeasPoint9~Sigma.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : Sigma Property*

### Description

Returns the signal enhancement sigma.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Sigma As Single
```

### Remarks

Sigma is an indicator for the noise level that depends logarithmically on the amplitude of the frequency lines of the spectrum. Only the frequency lines with the lowest amplitudes are taken into account. You can use the sigma indicator only for a relative analysis. The absolute value of this indicator does not have a meaning.

### Example


---

## VibrometerRange Property

*Quelle: `POLYFILELib~IMeasPoint9~VibrometerRange.html` · Polytec PolyFile Type Library · IMeasPoint9 Interface : VibrometerRange Property*

### Description

Returns the vibrometer range this point was measured with.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property VibrometerRange As String
```

### Remarks

The vibrometer range can vary from point to point when the AutoRemeasureAutoRange Property was set to True. In other cases, this property might return an empty string.
