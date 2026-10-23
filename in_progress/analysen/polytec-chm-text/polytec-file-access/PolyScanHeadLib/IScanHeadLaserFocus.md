# PolyScanHeadLib – IScanHeadLaserFocus

## IScanHeadLaserFocus Interface

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus.html` · Polytec PolyScanHead Type Library*

### Description

Controls the focusing of the laser.

### Object Model

### Remarks

It is recommended to cast to the ScanHeadLaserFocus object.


---

## IScanHeadLaserFocus Interface Members

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| GetDepthOfFocusRange | Returns the depth of focus range. |
|---|---|

### Public Properties

| DepthOfFocusFactor | The depth of focus factor of the scanning head. |
|---|---|
| FocalLength | The focal length of the objective of the scanning head. |
| FocusCommandTime | The time in second per focus command. |
| FocusSharpness | The focus sharpness. |
| FocusStepWidth | The step width of the focus in meter. |
| LensToMirrorDistance | The distance of the objective to the first mirror in meter. |
| MinFocusDistance | The minimum focus distance in meter. |
| ScanHeadDevice | The scanning head device object. |
| TimePerFocusStep | The time in second per focus step. |


---

## GetDepthOfFocusRange Method

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~GetDepthOfFocusRange.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : GetDepthOfFocusRange Method*

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

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~DepthOfFocusFactor.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : DepthOfFocusFactor Property*

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

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~FocalLength.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : FocalLength Property*

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

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~FocusCommandTime.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : FocusCommandTime Property*

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

## FocusSharpness Property

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~FocusSharpness.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : FocusSharpness Property*

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

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~FocusStepWidth.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : FocusStepWidth Property*

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

## LensToMirrorDistance Property

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~LensToMirrorDistance.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : LensToMirrorDistance Property*

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

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~MinFocusDistance.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : MinFocusDistance Property*

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

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~ScanHeadDevice.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : ScanHeadDevice Property*

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

*Quelle: `PolyScanHeadLib~IScanHeadLaserFocus~TimePerFocusStep.html` · Polytec PolyScanHead Type Library · IScanHeadLaserFocus Interface : TimePerFocusStep Property*

### Description

The time in second per focus step.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TimePerFocusStep As Double
```
