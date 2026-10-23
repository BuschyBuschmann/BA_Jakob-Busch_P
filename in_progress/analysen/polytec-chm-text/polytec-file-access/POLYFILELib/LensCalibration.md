# POLYFILELib – LensCalibration

## LensCalibration Object

*Quelle: `POLYFILELib~LensCalibration.html` · Polytec PolyFile Type Library*

### Description

Calibration of the objective of an MSV or MSA system. Item of the LensCalibrations collection.

### Remarks

Beginning with the software releases in July 2018, a "lens" is called "objective" in the GUI of the applications.


---

## LensCalibration Object Members

*Quelle: `POLYFILELib~LensCalibration_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Caps | Returns or specifies the capabilities of this objective. This can be a combination of the following PTCLensCalibrationCapsType constants. |
|---|---|
| DistanceX | Returns or specifies the horizontal calibration distance in meter. |
| DistanceY | Returns or specifies the vertical calibration distance in meter. |
| GouyCorrectionFactor | Returns or specifies the Gouy correction factor. |
| MagnificationFactorX | Returns or specifies the horizontal objective calibration factor. |
| MagnificationFactorY | Returns or specifies the vertical objective calibration factor. |
| Name | Returns or specifies the name of the objective calibration. |
| OpticalPathLength | The optical path for this objective. |
| PixelsX | Returns or specifies the horizontal calibration distance in pixels. |
| PixelsY | Returns or specifies the vertical calibration distance in pixels. |


---

## Caps Property

*Quelle: `POLYFILELib~LensCalibration~Caps.html` · Polytec PolyFile Type Library · LensCalibration Object : Caps Property*

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

*Quelle: `POLYFILELib~LensCalibration~DistanceX.html` · Polytec PolyFile Type Library · LensCalibration Object : DistanceX Property*

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

*Quelle: `POLYFILELib~LensCalibration~DistanceY.html` · Polytec PolyFile Type Library · LensCalibration Object : DistanceY Property*

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

## GouyCorrectionFactor Property

*Quelle: `POLYFILELib~LensCalibration~GouyCorrectionFactor.html` · Polytec PolyFile Type Library · LensCalibration Object : GouyCorrectionFactor Property*

### Description

Returns or specifies the Gouy correction factor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property GouyCorrectionFactor As Double
```

### Remarks

This is a factor for the correction of the Gouy phase of the laser beam. Some starting information on the Gouy phase can be found in the English Wikipedia at Gaussian_beam#Gouy_phase. For a clean explanation of the physics background, please consult a reference book.

Relevant for our application is the effect that by the Gouy phase of the laser beam the measured amplitude of the vibrometer signal is smaller than the true one. The strength of this effect depends on the used objective. The Gouy correction factor is multiplied with the measured vibrometer signal in order to compensate for this effect.

The Gouy correction factor should stay in the interval (1, 1.2).


---

## MagnificationFactorX Property

*Quelle: `POLYFILELib~LensCalibration~MagnificationFactorX.html` · Polytec PolyFile Type Library · LensCalibration Object : MagnificationFactorX Property*

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

*Quelle: `POLYFILELib~LensCalibration~MagnificationFactorY.html` · Polytec PolyFile Type Library · LensCalibration Object : MagnificationFactorY Property*

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

*Quelle: `POLYFILELib~LensCalibration~Name.html` · Polytec PolyFile Type Library · LensCalibration Object : Name Property*

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

## OpticalPathLength Property

*Quelle: `POLYFILELib~LensCalibration~OpticalPathLength.html` · Polytec PolyFile Type Library · LensCalibration Object : OpticalPathLength Property*

### Description

The optical path for this objective.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property OpticalPathLength As Double
```

### Return Type

The optical path length.

### Remarks

The optical path length is only relevant on MSA-650 systems.


---

## PixelsX Property

*Quelle: `POLYFILELib~LensCalibration~PixelsX.html` · Polytec PolyFile Type Library · LensCalibration Object : PixelsX Property*

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

*Quelle: `POLYFILELib~LensCalibration~PixelsY.html` · Polytec PolyFile Type Library · LensCalibration Object : PixelsY Property*

### Description

Returns or specifies the vertical calibration distance in pixels.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PixelsY As Long
```
