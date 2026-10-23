# POLYFILELib – IMeasPoint11

## IMeasPoint11 Interface

*Quelle: `POLYFILELib~IMeasPoint11.html` · Polytec PolyFile Type Library*

### Description

IMeasPoint11 Interface

### Object Model

### Remarks

It is recommended to cast to the MeasPoint Object.


---

## IMeasPoint11 Interface Members

*Quelle: `POLYFILELib~IMeasPoint11_members.html` · Polytec PolyFile Type Library*

### Public Methods

| CoordXYZ | CoordXYZ |
|---|---|
| SetCoordXYZ | SetCoordXYZ |
| SetTextureXYIndex | method SetTextureXYIndex |
| SetVideoXY | SetVideoXY |
| TextureXYIndex | method TextureXYIndex |
| ToggleValidInvalidated | Switch MeasPointStatus between Invalidated and Valid |
| VideoXY | VideoXY |

### Public Properties

| AverageCount | Get property AverageCount |
|---|---|
| Component | Returns the root component of the geometry components hierarchy. |
| ContainedFileActiveID | Get property contained file active ID |
| ContainedFileActiveMPIndex | Get property contained file active measpoint index |
| ContainedFileIndex | Get property ContainedFileIndex |
| ContainedFileMeasPointIndex | Get property ContainedFileMPIndex |
| FocusStatus | Get property FocusStatus |
| FocusValues | Get property FocusValues |
| GeometryStatus | Get property GeometryStatus |
| Index | Get property Index |
| Label | Get property Label |
| MinSigma | Get property MinSigma |
| PathLengthStatus | Get property PathLengthStatus |
| PathLengthValue | Get property PathLengthValue |
| ScanDistances | Get property ScanDistances |
| ScanQuantitiesX | Get property ScanQuantitiesX |
| ScanQuantitiesY | Get property ScanQuantitiesY |
| ScanQuantity | Get property ScanQuantity |
| ScanStatus | Get property ScanStatus |
| ScanStatusDisabled | Get property ScanStatusDisabled |
| Sigma | Get property Sigma |
| VibrometerRange | Get property vibrometer range |


---

## CoordXYZ Method

*Quelle: `POLYFILELib~IMeasPoint11~CoordXYZ.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : CoordXYZ Method*

### Description

CoordXYZ

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

pdY

pdZ


---

## SetCoordXYZ Method

*Quelle: `POLYFILELib~IMeasPoint11~SetCoordXYZ.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : SetCoordXYZ Method*

### Description

SetCoordXYZ

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

dY

dZ


---

## SetTextureXYIndex Method

*Quelle: `POLYFILELib~IMeasPoint11~SetTextureXYIndex.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : SetTextureXYIndex Method*

### Description

method SetTextureXYIndex

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

yValue

Index


---

## SetVideoXY Method

*Quelle: `POLYFILELib~IMeasPoint11~SetVideoXY.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : SetVideoXY Method*

### Description

SetVideoXY

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

fY


---

## TextureXYIndex Method

*Quelle: `POLYFILELib~IMeasPoint11~TextureXYIndex.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : TextureXYIndex Method*

### Description

method TextureXYIndex

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

yValue

Index


---

## ToggleValidInvalidated Method

*Quelle: `POLYFILELib~IMeasPoint11~ToggleValidInvalidated.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ToggleValidInvalidated Method*

### Description

Switch MeasPointStatus between Invalidated and Valid

### Syntax

*Visual Basic:*
```
Public Sub ToggleValidInvalidated()
```


---

## VideoXY Method

*Quelle: `POLYFILELib~IMeasPoint11~VideoXY.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : VideoXY Method*

### Description

VideoXY

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

pfY


---

## AverageCount Property

*Quelle: `POLYFILELib~IMeasPoint11~AverageCount.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : AverageCount Property*

### Description

Get property AverageCount

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AverageCount As Long
```


---

## Component Property

*Quelle: `POLYFILELib~IMeasPoint11~Component.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : Component Property*

### Description

Returns the root component of the geometry components hierarchy.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Component As GeometryComponent
```


---

## ContainedFileActiveID Property

*Quelle: `POLYFILELib~IMeasPoint11~ContainedFileActiveID.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ContainedFileActiveID Property*

### Description

Get property contained file active ID

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ContainedFileActiveID As Long
```


---

## ContainedFileActiveMPIndex Property

*Quelle: `POLYFILELib~IMeasPoint11~ContainedFileActiveMPIndex.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ContainedFileActiveMPIndex Property*

### Description

Get property contained file active measpoint index

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ContainedFileActiveMPIndex As Long
```


---

## ContainedFileIndex Property

*Quelle: `POLYFILELib~IMeasPoint11~ContainedFileIndex.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ContainedFileIndex Property*

### Description

Get property ContainedFileIndex

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ContainedFileIndex As Long
```


---

## ContainedFileMeasPointIndex Property

*Quelle: `POLYFILELib~IMeasPoint11~ContainedFileMeasPointIndex.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ContainedFileMeasPointIndex Property*

### Description

Get property ContainedFileMPIndex

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ContainedFileMeasPointIndex As Long
```


---

## FocusStatus Property

*Quelle: `POLYFILELib~IMeasPoint11~FocusStatus.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : FocusStatus Property*

### Description

Get property FocusStatus

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusStatus As PTCFocusStatus
```


---

## FocusValues Property

*Quelle: `POLYFILELib~IMeasPoint11~FocusValues.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : FocusValues Property*

### Description

Get property FocusValues

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FocusValues As Long()
```


---

## GeometryStatus Property

*Quelle: `POLYFILELib~IMeasPoint11~GeometryStatus.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : GeometryStatus Property*

### Description

Get property GeometryStatus

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GeometryStatus As PTCGeometryStatus
```


---

## Index Property

*Quelle: `POLYFILELib~IMeasPoint11~Index.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : Index Property*

### Description

Get property Index

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Index As Long
```


---

## Label Property

*Quelle: `POLYFILELib~IMeasPoint11~Label.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : Label Property*

### Description

Get property Label

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Label As Long
```


---

## MinSigma Property

*Quelle: `POLYFILELib~IMeasPoint11~MinSigma.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : MinSigma Property*

### Description

Get property MinSigma

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinSigma As Single
```


---

## PathLengthStatus Property

*Quelle: `POLYFILELib~IMeasPoint11~PathLengthStatus.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : PathLengthStatus Property*

### Description

Get property PathLengthStatus

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PathLengthStatus As PTCPathLengthStatus
```


---

## PathLengthValue Property

*Quelle: `POLYFILELib~IMeasPoint11~PathLengthValue.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : PathLengthValue Property*

### Description

Get property PathLengthValue

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PathLengthValue As Single
```


---

## ScanDistances Property

*Quelle: `POLYFILELib~IMeasPoint11~ScanDistances.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ScanDistances Property*

### Description

Get property ScanDistances

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanDistances As Double()
```


---

## ScanQuantitiesX Property

*Quelle: `POLYFILELib~IMeasPoint11~ScanQuantitiesX.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ScanQuantitiesX Property*

### Description

Get property ScanQuantitiesX

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanQuantitiesX As Double()
```


---

## ScanQuantitiesY Property

*Quelle: `POLYFILELib~IMeasPoint11~ScanQuantitiesY.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ScanQuantitiesY Property*

### Description

Get property ScanQuantitiesY

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanQuantitiesY As Double()
```


---

## ScanQuantity Property

*Quelle: `POLYFILELib~IMeasPoint11~ScanQuantity.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ScanQuantity Property*

### Description

Get property ScanQuantity

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanQuantity As PTCPhysicalQuantity
```


---

## ScanStatus Property

*Quelle: `POLYFILELib~IMeasPoint11~ScanStatus.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ScanStatus Property*

### Description

Get property ScanStatus

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanStatus As PTCScanStatus
```


---

## ScanStatusDisabled Property

*Quelle: `POLYFILELib~IMeasPoint11~ScanStatusDisabled.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : ScanStatusDisabled Property*

### Description

Get property ScanStatusDisabled

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScanStatusDisabled As Boolean
```


---

## Sigma Property

*Quelle: `POLYFILELib~IMeasPoint11~Sigma.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : Sigma Property*

### Description

Get property Sigma

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Sigma As Single
```


---

## VibrometerRange Property

*Quelle: `POLYFILELib~IMeasPoint11~VibrometerRange.html` · Polytec PolyFile Type Library · IMeasPoint11 Interface : VibrometerRange Property*

### Description

Get property vibrometer range

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property VibrometerRange As String
```
