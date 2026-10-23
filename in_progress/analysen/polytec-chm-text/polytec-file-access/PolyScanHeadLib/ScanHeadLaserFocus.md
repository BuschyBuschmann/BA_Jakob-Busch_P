# PolyScanHeadLib – ScanHeadLaserFocus

## ScanHeadLaserFocus Object

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus.html` · Polytec PolyScanHead Type Library*

### Description

Controls the focusing of the laser.

### Object Model

### Remarks

Beginning with the software releases in July 2018, a "lens" is called "objective" in the GUI of the applications.


---

## ScanHeadLaserFocus Object Members

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| GetDepthOfFocusRange | Returns the depth of focus range. |
|---|---|

### Public Properties

| DepthOfFocusFactor | The depth of focus factor of the scanning head. |
|---|---|
| FocalLength | The focal length of the objective of the scanning head. |
| FocusCommandTime | The time in second per focus command. |
| FocusInfinitePos | The infinite position of the focus in focus step. |
| FocusSharpness | The focus sharpness. |
| FocusStepWidth | The step width of the focus in meter. |
| LensToLensDistance | This property is obsolete. Do not use it anymore. |
| LensToMirrorDistance | The distance of the objective to the first mirror in meter. |
| MinFocusDistance | The minimum focus distance in meter. |
| ScanHeadDevice | The scanning head device object. |
| TimePerFocusStep | The time in second per focus step. |


---

## GetDepthOfFocusRange Method

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~GetDepthOfFocusRange.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : GetDepthOfFocusRange Method*

### Description

Returns the depth of focus range.

### Syntax

*Visual Basic:*
```
Public Sub GetDepthOfFocusRange( _
   ByVal lFocusPosition As Long, _
   ByVal dDepthOfSharpFac As Double, _
   ByRef plMinFocusPosition As Long, _
   ByRef plMaxFocusPosition As Long _
)
```

### Parameters

lFocusPosition

The focus position to get the depth of focus range for.

dDepthOfSharpFac

The depth of focus sharpness factor.

plMinFocusPosition

The minimum focus position of the depth of focus range.

plMaxFocusPosition

The maximum focus position of the depth of focus range.


---

## DepthOfFocusFactor Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~DepthOfFocusFactor.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : DepthOfFocusFactor Property*

### Description

The depth of focus factor of the scanning head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DepthOfFocusFactor As Double
```


---

## FocalLength Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~FocalLength.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : FocalLength Property*

### Description

The focal length of the objective of the scanning head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocalLength As Double
```


---

## FocusCommandTime Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~FocusCommandTime.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : FocusCommandTime Property*

### Description

The time in second per focus command.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusCommandTime As Double
```


---

## FocusInfinitePos Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~FocusInfinitePos.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : FocusInfinitePos Property*

### Description

The infinite position of the focus in focus step.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusInfinitePos As Double
```

### Return Type

The infinite position of the focus in focus step.


---

## FocusSharpness Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~FocusSharpness.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : FocusSharpness Property*

### Description

The focus sharpness.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FocusSharpness As Double
```


---

## FocusStepWidth Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~FocusStepWidth.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : FocusStepWidth Property*

### Description

The step width of the focus in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusStepWidth As Double
```


---

## LensToLensDistance Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~LensToLensDistance.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : LensToLensDistance Property*

### Description

This property is obsolete. Do not use it anymore.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LensToLensDistance As Double
```


---

## LensToMirrorDistance Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~LensToMirrorDistance.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : LensToMirrorDistance Property*

### Description

The distance of the objective to the first mirror in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LensToMirrorDistance As Double
```


---

## MinFocusDistance Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~MinFocusDistance.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : MinFocusDistance Property*

### Description

The minimum focus distance in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinFocusDistance As Double
```


---

## ScanHeadDevice Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~ScanHeadDevice.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : ScanHeadDevice Property*

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

## TimePerFocusStep Property

*Quelle: `PolyScanHeadLib~ScanHeadLaserFocus~TimePerFocusStep.html` · Polytec PolyScanHead Type Library · ScanHeadLaserFocus Object : TimePerFocusStep Property*

### Description

The time in second per focus step.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TimePerFocusStep As Double
```
