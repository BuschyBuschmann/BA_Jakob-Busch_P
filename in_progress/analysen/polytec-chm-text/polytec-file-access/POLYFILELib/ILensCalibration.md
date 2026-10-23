# POLYFILELib – ILensCalibration

## ILensCalibration Interface

*Quelle: `POLYFILELib~ILensCalibration.html` · Polytec PolyFile Type Library*

### Description

ILensCalibration Interface

### Remarks

It is recommended to cast to the LensCalibration Object.


---

## ILensCalibration Interface Members

*Quelle: `POLYFILELib~ILensCalibration_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Caps | Returns or specifies the capabilities of this objective. This can be a combination of the following PTCLensCalibrationCapsType constants. |
|---|---|
| DistanceX | Returns or specifies the horizontal calibration distance in meter. |
| DistanceY | Returns or specifies the vertical calibration distance in meter. |
| MagnificationFactorX | Returns or specifies the horizontal objective calibration factor. |
| MagnificationFactorY | Returns or specifies the vertical objective calibration factor. |
| Name | Returns or specifies the name of the objective calibration. |
| PixelsX | Returns or specifies the horizontal calibration distance in pixels. |
| PixelsY | Returns or specifies the vertical calibration distance in pixels. |


---

## Caps Property

*Quelle: `POLYFILELib~ILensCalibration~Caps.html` · Polytec PolyFile Type Library · ILensCalibration Interface : Caps Property*

### Description

Returns or specifies the capabilities of this objective. This can be a combination of the following PTCLensCalibrationCapsType constants.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCLensCalibrationCapsType
```

### Remarks

Beginning with the software releases in July 2018, a "lens" is called "objective" in the GUI of the applications.


---

## DistanceX Property

*Quelle: `POLYFILELib~ILensCalibration~DistanceX.html` · Polytec PolyFile Type Library · ILensCalibration Interface : DistanceX Property*

### Description

Returns or specifies the horizontal calibration distance in meter.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DistanceX As Double
```


---

## DistanceY Property

*Quelle: `POLYFILELib~ILensCalibration~DistanceY.html` · Polytec PolyFile Type Library · ILensCalibration Interface : DistanceY Property*

### Description

Returns or specifies the vertical calibration distance in meter.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DistanceY As Double
```


---

## MagnificationFactorX Property

*Quelle: `POLYFILELib~ILensCalibration~MagnificationFactorX.html` · Polytec PolyFile Type Library · ILensCalibration Interface : MagnificationFactorX Property*

### Description

Returns or specifies the horizontal objective calibration factor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MagnificationFactorX As Double
```


---

## MagnificationFactorY Property

*Quelle: `POLYFILELib~ILensCalibration~MagnificationFactorY.html` · Polytec PolyFile Type Library · ILensCalibration Interface : MagnificationFactorY Property*

### Description

Returns or specifies the vertical objective calibration factor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MagnificationFactorY As Double
```


---

## Name Property

*Quelle: `POLYFILELib~ILensCalibration~Name.html` · Polytec PolyFile Type Library · ILensCalibration Interface : Name Property*

### Description

Returns or specifies the name of the objective calibration.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## PixelsX Property

*Quelle: `POLYFILELib~ILensCalibration~PixelsX.html` · Polytec PolyFile Type Library · ILensCalibration Interface : PixelsX Property*

### Description

Returns or specifies the horizontal calibration distance in pixels.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PixelsX As Long
```


---

## PixelsY Property

*Quelle: `POLYFILELib~ILensCalibration~PixelsY.html` · Polytec PolyFile Type Library · ILensCalibration Interface : PixelsY Property*

### Description

Returns or specifies the vertical calibration distance in pixels.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PixelsY As Long
```
