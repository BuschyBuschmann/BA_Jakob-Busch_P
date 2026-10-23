# POLYFILELib – MeasPoint

## MeasPoint Object

*Quelle: `POLYFILELib~MeasPoint.html` · Polytec PolyFile Type Library*

### Description

Item of the MeasPoints collection. The MeasPoint object contains properties of a measurement point (scan point) of a MPV/PSV measurement file or settings file.

### Object Model


---

## MeasPoint Object Members

*Quelle: `POLYFILELib~MeasPoint_members.html` · Polytec PolyFile Type Library*

### Public Methods

| CoordXYZ | Retrieves the 3D coordinate of the measurement point. |
|---|---|
| SetCoordXYZ | Sets the 3D coordinate of the measurement point. |
| SetTextureXYIndex | Sets the texture coordinates and the texture index for the point. |
| SetVideoXY | Sets the video coordinate of the measurement point. |
| TextureXYIndex | Gets the texture coordinates and the texture index of the point. |
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
| PathLengthStatus | Returns a bit-pattern of the optical path length status. To test for status bits use the And operator to mask the status with one or several of the bit constants of the PTCPathLengthStatus Enumeration . |
| PathLengthValue | Returns or sets the optical path length value. |
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

*Quelle: `POLYFILELib~MeasPoint~CoordXYZ.html` · Polytec PolyFile Type Library · MeasPoint Object : CoordXYZ Method*

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

*Quelle: `POLYFILELib~MeasPoint~SetCoordXYZ.html` · Polytec PolyFile Type Library · MeasPoint Object : SetCoordXYZ Method*

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

## SetTextureXYIndex Method

*Quelle: `POLYFILELib~MeasPoint~SetTextureXYIndex.html` · Polytec PolyFile Type Library · MeasPoint Object : SetTextureXYIndex Method*

### Description

Sets the texture coordinates and the texture index for the point.

### Syntax

*Visual Basic:*
```
Public Sub SetTextureXYIndex( _
   ByVal xValue As Single, _
   ByVal yValue As Single, _
   ByVal Index As Long _
)
```

### Parameters

xValue

The horizontal texture coordinate in the range 0 - 1.

yValue

The vertical texture coordinate in the range 0 - 1.

Index

The zero-based index of the texture.

### Remarks

The texture index 0 references the video image. Texture indices larger than 0 reference textures from imported geometries.


---

## SetVideoXY Method

*Quelle: `POLYFILELib~MeasPoint~SetVideoXY.html` · Polytec PolyFile Type Library · MeasPoint Object : SetVideoXY Method*

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

## TextureXYIndex Method

*Quelle: `POLYFILELib~MeasPoint~TextureXYIndex.html` · Polytec PolyFile Type Library · MeasPoint Object : TextureXYIndex Method*

### Description

Gets the texture coordinates and the texture index of the point.

### Syntax

*Visual Basic:*
```
Public Sub TextureXYIndex( _
   ByRef xValue As Single, _
   ByRef yValue As Single, _
   ByRef Index As Long _
)
```

### Parameters

xValue

The horizontal texture coordinate in the range 0 - 1.

yValue

The vertical texture coordinate in the range 0 - 1.

Index

The zero-based index of the texture.

### Remarks

The texture index 0 references the video image. Texture indices larger than 0 reference textures from imported geometries.


---

## ToggleValidInvalidated Method

*Quelle: `POLYFILELib~MeasPoint~ToggleValidInvalidated.html` · Polytec PolyFile Type Library · MeasPoint Object : ToggleValidInvalidated Method*

### Description

Toggles the invalidated state of the measurement point.

### Syntax

*Visual Basic:*
```
Public Sub ToggleValidInvalidated()
```


---

## VideoXY Method

*Quelle: `POLYFILELib~MeasPoint~VideoXY.html` · Polytec PolyFile Type Library · MeasPoint Object : VideoXY Method*

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

*Quelle: `POLYFILELib~MeasPoint~AverageCount.html` · Polytec PolyFile Type Library · MeasPoint Object : AverageCount Property*

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

*Quelle: `POLYFILELib~MeasPoint~Component.html` · Polytec PolyFile Type Library · MeasPoint Object : Component Property*

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

*Quelle: `POLYFILELib~MeasPoint~ContainedFileActiveID.html` · Polytec PolyFile Type Library · MeasPoint Object : ContainedFileActiveID Property*

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

*Quelle: `POLYFILELib~MeasPoint~ContainedFileActiveMPIndex.html` · Polytec PolyFile Type Library · MeasPoint Object : ContainedFileActiveMPIndex Property*

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

*Quelle: `POLYFILELib~MeasPoint~ContainedFileIndex.html` · Polytec PolyFile Type Library · MeasPoint Object : ContainedFileIndex Property*

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

*Quelle: `POLYFILELib~MeasPoint~ContainedFileMeasPointIndex.html` · Polytec PolyFile Type Library · MeasPoint Object : ContainedFileMeasPointIndex Property*

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

*Quelle: `POLYFILELib~MeasPoint~FocusStatus.html` · Polytec PolyFile Type Library · MeasPoint Object : FocusStatus Property*

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

*Quelle: `POLYFILELib~MeasPoint~FocusValues.html` · Polytec PolyFile Type Library · MeasPoint Object : FocusValues Property*

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

*Quelle: `POLYFILELib~MeasPoint~GeometryStatus.html` · Polytec PolyFile Type Library · MeasPoint Object : GeometryStatus Property*

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

*Quelle: `POLYFILELib~MeasPoint~Index.html` · Polytec PolyFile Type Library · MeasPoint Object : Index Property*

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

*Quelle: `POLYFILELib~MeasPoint~Label.html` · Polytec PolyFile Type Library · MeasPoint Object : Label Property*

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

*Quelle: `POLYFILELib~MeasPoint~MinSigma.html` · Polytec PolyFile Type Library · MeasPoint Object : MinSigma Property*

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

## PathLengthStatus Property

*Quelle: `POLYFILELib~MeasPoint~PathLengthStatus.html` · Polytec PolyFile Type Library · MeasPoint Object : PathLengthStatus Property*

### Description

Returns a bit-pattern of the optical path length status. To test for status bits use the And operator to mask the status with one or several of the bit constants of the PTCPathLengthStatus Enumeration.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PathLengthStatus As PTCPathLengthStatus
```

### Remarks

The optical path length is only relevant on MSA-650 systems.


---

## PathLengthValue Property

*Quelle: `POLYFILELib~MeasPoint~PathLengthValue.html` · Polytec PolyFile Type Library · MeasPoint Object : PathLengthValue Property*

### Description

Returns or sets the optical path length value.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PathLengthValue As Single
```

### Return Type

The path length value.

### Remarks

The optical path length value is only relevant on MSA-650 systems.


---

## ScanDistances Property

*Quelle: `POLYFILELib~MeasPoint~ScanDistances.html` · Polytec PolyFile Type Library · MeasPoint Object : ScanDistances Property*

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

*Quelle: `POLYFILELib~MeasPoint~ScanQuantitiesX.html` · Polytec PolyFile Type Library · MeasPoint Object : ScanQuantitiesX Property*

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

*Quelle: `POLYFILELib~MeasPoint~ScanQuantitiesY.html` · Polytec PolyFile Type Library · MeasPoint Object : ScanQuantitiesY Property*

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

*Quelle: `POLYFILELib~MeasPoint~ScanQuantity.html` · Polytec PolyFile Type Library · MeasPoint Object : ScanQuantity Property*

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

*Quelle: `POLYFILELib~MeasPoint~ScanStatus.html` · Polytec PolyFile Type Library · MeasPoint Object : ScanStatus Property*

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

*Quelle: `POLYFILELib~MeasPoint~ScanStatusDisabled.html` · Polytec PolyFile Type Library · MeasPoint Object : ScanStatusDisabled Property*

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

*Quelle: `POLYFILELib~MeasPoint~Sigma.html` · Polytec PolyFile Type Library · MeasPoint Object : Sigma Property*

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

*Quelle: `POLYFILELib~MeasPoint~VibrometerRange.html` · Polytec PolyFile Type Library · MeasPoint Object : VibrometerRange Property*

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
