# POLYALIGNMENTLib – IAlignment2D

## IAlignment2D Interface

*Quelle: `POLYALIGNMENTLib~IAlignment2D.html` · Polytec PolyAlignment Type Library*

### Description

Item of Alignments2D collection.

### Object Model

### Remarks

It is recommended to cast to the Alignment2D Object.

### Example


---

## IAlignment2D Interface Members

*Quelle: `POLYALIGNMENTLib~IAlignment2D_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Calculate | Calculates a new 2D alignment. |
|---|---|
| GetCosineCorrectionFactor | Retrieves the cosine correction factor for the given scanner coordinates. |
| Invalidate | Invalidates the current 2D alignment and resets all properties. |
| ScannerToVideo | Converts the specified scanner coordinates to video coordinates. |
| VideoToScanner | Converts the specified video coordinates to scanner coordinates. |

### Public Properties

| Align2DPoints | Returns a copy of the collection of 2D alignment points. |
|---|---|
| ScanHeadDistance | Returns the distance from the scanning heads front panel (for scanner angle 0/0) to the measurement object in meter. |
| ScanHeadType | Returns the type of the scanning head. |
| ScannerQuantity | Returns the physical quantity of the scanner. |
| Valid | Returns true if the 2D alignment is valid. |


---

## Calculate Method

*Quelle: `POLYALIGNMENTLib~IAlignment2D~Calculate.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : Calculate Method*

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

*Quelle: `POLYALIGNMENTLib~IAlignment2D~GetCosineCorrectionFactor.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : GetCosineCorrectionFactor Method*

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

*Quelle: `POLYALIGNMENTLib~IAlignment2D~Invalidate.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : Invalidate Method*

### Description

Invalidates the current 2D alignment and resets all properties.

### Syntax

*Visual Basic:*
```
Public Sub Invalidate()
```


---

## ScannerToVideo Method

*Quelle: `POLYALIGNMENTLib~IAlignment2D~ScannerToVideo.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : ScannerToVideo Method*

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

## VideoToScanner Method

*Quelle: `POLYALIGNMENTLib~IAlignment2D~VideoToScanner.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : VideoToScanner Method*

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

*Quelle: `POLYALIGNMENTLib~IAlignment2D~Align2DPoints.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : Align2DPoints Property*

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

## ScanHeadDistance Property

*Quelle: `POLYALIGNMENTLib~IAlignment2D~ScanHeadDistance.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : ScanHeadDistance Property*

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

*Quelle: `POLYALIGNMENTLib~IAlignment2D~ScanHeadType.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : ScanHeadType Property*

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

*Quelle: `POLYALIGNMENTLib~IAlignment2D~ScannerQuantity.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : ScannerQuantity Property*

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

*Quelle: `POLYALIGNMENTLib~IAlignment2D~Valid.html` · Polytec PolyAlignment Type Library · IAlignment2D Interface : Valid Property*

### Description

Returns true if the 2D alignment is valid.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Valid As Boolean
```
