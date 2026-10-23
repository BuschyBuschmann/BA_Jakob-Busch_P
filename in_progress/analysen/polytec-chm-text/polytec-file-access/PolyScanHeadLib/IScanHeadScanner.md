# PolyScanHeadLib – IScanHeadScanner

## IScanHeadScanner Interface

*Quelle: `PolyScanHeadLib~IScanHeadScanner.html` · Polytec PolyScanHead Type Library*

### Description

Controls the scanner of the scanning head.

### Object Model

### Remarks

It is recommended to cast to the ScanHeadScanner object.


---

## IScanHeadScanner Interface Members

*Quelle: `PolyScanHeadLib~IScanHeadScanner_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| GetLaserOrigin | Returns the coordinate where the laser hits the front plate of the scanning head when the beam direction is 0° / 0°. |
|---|---|
| GetMirrorTimesX | Returns the moving and waiting time for a given step of the horizontal scanner. |
| GetMirrorTimesY | Returns the moving and waiting time for a given step of the vertical scanner. |

### Public Properties

| CosCorrectionActiveX | True if angle correction is active for horizontal direction. |
|---|---|
| CosCorrectionActiveY | True if angle correction is active for vertical direction. |
| CosCorrectionPossibleX | True if angle correction is possible for the horizontal direction. |
| CosCorrectionPossibleY | True if angle correction is possible for the vertical direction. |
| InvertedX | True if the polarity of the horizontal scanner is inverted. |
| InvertedY | True if the polarity of the vertical scanner is inverted. |
| MirrorDistance | The distance in meter between the two scanner mirrors. |
| PreferredScanDirection | The preferred scan direction. |
| Quantity | The physical quantity of the scanning head. |
| QuantityMaxX | The maximum value for the horizontal scanner in the quantity of the scanning head. |
| QuantityMaxY | The maximum value for the vertical scanner in the quantity of the scanning head. |
| ScanHeadDevice | The scanning head device object. |
| SwappedXY | True if the horizontal and vertical scanners are swapped. |


---

## GetLaserOrigin Method

*Quelle: `PolyScanHeadLib~IScanHeadScanner~GetLaserOrigin.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : GetLaserOrigin Method*

### Description

Returns the coordinate where the laser hits the front plate of the scanning head when the beam direction is 0° / 0°.

### Syntax

*Visual Basic:*
```
Public Sub GetLaserOrigin( _
   ByRef pdCoordX As Double, _
   ByRef pdCoordY As Double, _
   ByRef pdCoordZ As Double _
)
```

### Parameters

pdCoordX

The x-coordinate of the laser beam origin in meter.

pdCoordY

The y-coordinate of the laser beam origin in meter.

pdCoordZ

The z-coordinate of the laser beam origin in meter.

### Remarks

The coordinate returned is in the coordinate system of the scanning head. The origin of this coordinate system is at the center of the first mirror (vertical scanner). When looking from behind the scanning head, the positive x-axis points right, the positive y-axis points up and the positive z-axis points back.


---

## GetMirrorTimesX Method

*Quelle: `PolyScanHeadLib~IScanHeadScanner~GetMirrorTimesX.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : GetMirrorTimesX Method*

### Description

Returns the moving and waiting time for a given step of the horizontal scanner.

### Syntax

*Visual Basic:*
```
Public Sub GetMirrorTimesX( _
   ByVal dDiffX As Double, _
   ByRef pdMoveTimeX As Double, _
   ByRef pdWaitTimeX As Double _
)
```

### Parameters

dDiffX

The step size in the quantity of the scanning head.

pdMoveTimeX

The moving time in second.

pdWaitTimeX

The waiting time in second.


---

## GetMirrorTimesY Method

*Quelle: `PolyScanHeadLib~IScanHeadScanner~GetMirrorTimesY.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : GetMirrorTimesY Method*

### Description

Returns the moving and waiting time for a given step of the vertical scanner.

### Syntax

*Visual Basic:*
```
Public Sub GetMirrorTimesY( _
   ByVal dDiffY As Double, _
   ByRef pdMoveTimeY As Double, _
   ByRef pdWaitTimeY As Double _
)
```

### Parameters

dDiffY

The step size in the quantity of the scanning head.

pdMoveTimeY

The moving time in second.

pdWaitTimeY

The waiting time in second.


---

## CosCorrectionActiveX Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~CosCorrectionActiveX.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : CosCorrectionActiveX Property*

### Description

True if angle correction is active for horizontal direction.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CosCorrectionActiveX As Boolean
```


---

## CosCorrectionActiveY Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~CosCorrectionActiveY.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : CosCorrectionActiveY Property*

### Description

True if angle correction is active for vertical direction.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CosCorrectionActiveY As Boolean
```


---

## CosCorrectionPossibleX Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~CosCorrectionPossibleX.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : CosCorrectionPossibleX Property*

### Description

True if angle correction is possible for the horizontal direction.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CosCorrectionPossibleX As Boolean
```


---

## CosCorrectionPossibleY Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~CosCorrectionPossibleY.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : CosCorrectionPossibleY Property*

### Description

True if angle correction is possible for the vertical direction.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CosCorrectionPossibleY As Boolean
```


---

## InvertedX Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~InvertedX.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : InvertedX Property*

### Description

True if the polarity of the horizontal scanner is inverted.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property InvertedX As Boolean
```


---

## InvertedY Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~InvertedY.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : InvertedY Property*

### Description

True if the polarity of the vertical scanner is inverted.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property InvertedY As Boolean
```


---

## MirrorDistance Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~MirrorDistance.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : MirrorDistance Property*

### Description

The distance in meter between the two scanner mirrors.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MirrorDistance As Double
```


---

## PreferredScanDirection Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~PreferredScanDirection.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : PreferredScanDirection Property*

### Description

The preferred scan direction.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PreferredScanDirection As PTCPreferredScanDirection
```


---

## Quantity Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~Quantity.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : Quantity Property*

### Description

The physical quantity of the scanning head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Quantity As PTCPhysicalQuantity
```

### Remarks

Possible values are voltage, angle or displacement.


---

## QuantityMaxX Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~QuantityMaxX.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : QuantityMaxX Property*

### Description

The maximum value for the horizontal scanner in the quantity of the scanning head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property QuantityMaxX As Double
```


---

## QuantityMaxY Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~QuantityMaxY.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : QuantityMaxY Property*

### Description

The maximum value for the vertical scanner in the quantity of the scanning head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property QuantityMaxY As Double
```


---

## ScanHeadDevice Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~ScanHeadDevice.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : ScanHeadDevice Property*

### Description

The scanning head device object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadDevice As IScanHeadDevice
```


---

## SwappedXY Property

*Quelle: `PolyScanHeadLib~IScanHeadScanner~SwappedXY.html` · Polytec PolyScanHead Type Library · IScanHeadScanner Interface : SwappedXY Property*

### Description

True if the horizontal and vertical scanners are swapped.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SwappedXY As Boolean
```
