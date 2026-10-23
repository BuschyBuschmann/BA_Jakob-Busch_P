# POLYALIGNMENTLib – Alignment2D

## Alignment2D Object

*Quelle: `POLYALIGNMENTLib~Alignment2D.html` · Polytec PolyAlignment Type Library*

### Description

Item of the Alignments2D collection.

### Object Model


---

## Alignment2D Object Members

*Quelle: `POLYALIGNMENTLib~Alignment2D_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Calculate | Calculates a new 2D alignment. |
|---|---|
| GetCosineCorrectionFactor | Retrieves the cosine correction factor for the given scanner coordinates. |
| Invalidate | Invalidates the current 2D alignment and resets all properties. |
| ScannerToVideo | Converts the specified scanner coordinates to video coordinates. |
| TriangulationGrid | Returns the triangulation grid that is used to calculate the 2D alignment. |
| VideoToScanner | Converts the specified video coordinates to scanner coordinates. |

### Public Properties

| Align2DPoints | Returns a copy of the collection of 2D alignment points. |
|---|---|
| Align2DPointsRef | Returns a read-only reference of the collection of 2D alignment points. |
| IsShowTriangulationGridPossible | Returns whether the triangulation grid can be shown. |
| ScanHeadDistance | Returns the distance from the scanning heads front panel (for scanner angle 0/0) to the measurement object in meter. |
| ScanHeadType | Returns the type of the scanning head. |
| ScannerQuantity | Returns the physical quantity of the scanner. |
| Valid | Returns true if the 2D alignment is valid. |


---

## Calculate Method

*Quelle: `POLYALIGNMENTLib~Alignment2D~Calculate.html` · Polytec PolyAlignment Type Library · Alignment2D Object : Calculate Method*

### Description

Calculates a new 2D alignment.

### Syntax

*Visual Basic:*
```
Public Sub Calculate( _
   ByVal pIAlign2DPoints As Align2DPoints, _
   ByVal pIScanHeadScanner As IScanHeadScanner, _
   ByVal vbTrapezoidCorrection As Boolean _
)
```

### Parameters

pIAlign2DPoints

The collection of 2D points for this alignment.

pIScanHeadScanner

The scanner properties for this alignment.

vbTrapezoidCorrection

If true, the correction of the camera trapezoidal error will be calculated.


---

## GetCosineCorrectionFactor Method

*Quelle: `POLYALIGNMENTLib~Alignment2D~GetCosineCorrectionFactor.html` · Polytec PolyAlignment Type Library · Alignment2D Object : GetCosineCorrectionFactor Method*

### Description

Retrieves the cosine correction factor for the given scanner coordinates.

### Syntax

*Visual Basic:*
```
Public Function GetCosineCorrectionFactor( _
   ByVal dScannerX As Double, _
   ByVal dScannerY As Double, _
   ByVal vbCorrectX As Boolean, _
   ByVal vbCorrectY As Boolean _
) As Double
```

### Parameters

dScannerX

The horizontal scanner coordinate (angle or displacement).

dScannerY

The vertical scanner coordinate (angle or displacement).

vbCorrectX

A flag indicating whether the x-axis is to be corrected.

vbCorrectY

A flag indicating whether the y-axis is to be corrected.

### Return Type

The cosine correction factor.


---

## Invalidate Method

*Quelle: `POLYALIGNMENTLib~Alignment2D~Invalidate.html` · Polytec PolyAlignment Type Library · Alignment2D Object : Invalidate Method*

### Description

Invalidates the current 2D alignment and resets all properties.

### Syntax

*Visual Basic:*
```
Public Sub Invalidate()
```


---

## ScannerToVideo Method

*Quelle: `POLYALIGNMENTLib~Alignment2D~ScannerToVideo.html` · Polytec PolyAlignment Type Library · Alignment2D Object : ScannerToVideo Method*

### Description

Converts the specified scanner coordinates to video coordinates.

### Syntax

*Visual Basic:*
```
Public Sub ScannerToVideo( _
   ByVal dScannerX As Double, _
   ByVal dScannerY As Double, _
   ByRef pfVideoX As Single, _
   ByRef pfVideoY As Single _
)
```

### Parameters

dScannerX

The horizontal scanner coordinate (angle or displacement).

dScannerY

The vertical scanner coordinate (angle or displacement).

pfVideoX

The video x-coordinate.

pfVideoY

The video y-coordinate.

### Remarks

For PSV systems the scanner coordinates are expected to be specified as angles in degree, and for MSA systems they are expected as displacements.

### Example


---

## TriangulationGrid Method

*Quelle: `POLYALIGNMENTLib~Alignment2D~TriangulationGrid.html` · Polytec PolyAlignment Type Library · Alignment2D Object : TriangulationGrid Method*

### Description

Returns the triangulation grid that is used to calculate the 2D alignment.

### Syntax

*Visual Basic:*
```
Public Function TriangulationGrid( _
   ByRef ppsaPoints() As Single _
) As Long()
```

### Parameters

ppsaPoints

Receives the coordinates of the grid points with alternating x- and y-coordinates.

### Return Type

An array containing the triangle elements.

### Remarks

The returned elements are a 0-based, 1-dimensional array of integers with the 1-based indexes of the grid points. For every element the array contains the number of the points in the element followed by the point indexes.

### Example


---

## VideoToScanner Method

*Quelle: `POLYALIGNMENTLib~Alignment2D~VideoToScanner.html` · Polytec PolyAlignment Type Library · Alignment2D Object : VideoToScanner Method*

### Description

Converts the specified video coordinates to scanner coordinates.

### Syntax

*Visual Basic:*
```
Public Sub VideoToScanner( _
   ByVal fVideoX As Single, _
   ByVal fVideoY As Single, _
   ByRef pdScannerX As Double, _
   ByRef pdScannerY As Double _
)
```

### Parameters

fVideoX

The video x-coordinate.

fVideoY

The video y-coordinate.

pdScannerX

The horizontal scanner coordinate (angle or displacement).

pdScannerY

The vertical scanner coordinate (angle or displacement).

### Remarks

For PSV systems the scanner coordinates are returned as angles in degree, and for MSA systems they are returned as displacements.


---

## Align2DPoints Property

*Quelle: `POLYALIGNMENTLib~Alignment2D~Align2DPoints.html` · Polytec PolyAlignment Type Library · Alignment2D Object : Align2DPoints Property*

### Description

Returns a copy of the collection of 2D alignment points.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Align2DPoints As Align2DPoints
```


---

## Align2DPointsRef Property

*Quelle: `POLYALIGNMENTLib~Alignment2D~Align2DPointsRef.html` · Polytec PolyAlignment Type Library · Alignment2D Object : Align2DPointsRef Property*

### Description

Returns a read-only reference of the collection of 2D alignment points.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Align2DPointsRef As Align2DPoints
```


---

## IsShowTriangulationGridPossible Property

*Quelle: `POLYALIGNMENTLib~Alignment2D~IsShowTriangulationGridPossible.html` · Polytec PolyAlignment Type Library · Alignment2D Object : IsShowTriangulationGridPossible Property*

### Description

Returns whether the triangulation grid can be shown.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsShowTriangulationGridPossible As Boolean
```

### Return Type

True when the triangulation grid can be shown.

### Example


---

## ScanHeadDistance Property

*Quelle: `POLYALIGNMENTLib~Alignment2D~ScanHeadDistance.html` · Polytec PolyAlignment Type Library · Alignment2D Object : ScanHeadDistance Property*

### Description

Returns the distance from the scanning heads front panel (for scanner angle 0/0) to the measurement object in meter.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadDistance As Double
```


---

## ScanHeadType Property

*Quelle: `POLYALIGNMENTLib~Alignment2D~ScanHeadType.html` · Polytec PolyAlignment Type Library · Alignment2D Object : ScanHeadType Property*

### Description

Returns the type of the scanning head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadType As PTCScanHeadType
```


---

## ScannerQuantity Property

*Quelle: `POLYALIGNMENTLib~Alignment2D~ScannerQuantity.html` · Polytec PolyAlignment Type Library · Alignment2D Object : ScannerQuantity Property*

### Description

Returns the physical quantity of the scanner.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScannerQuantity As PTCPhysicalQuantity
```

### Remarks

The possible physical quantities are ptcPhysicalQuantityAngle for the default scanning head and ptcPhysicalQuantityDisplacement for the MSV and MSA scanning heads.


---

## Valid Property

*Quelle: `POLYALIGNMENTLib~Alignment2D~Valid.html` · Polytec PolyAlignment Type Library · Alignment2D Object : Valid Property*

### Description

Returns true if the 2D alignment is valid.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Valid As Boolean
```
