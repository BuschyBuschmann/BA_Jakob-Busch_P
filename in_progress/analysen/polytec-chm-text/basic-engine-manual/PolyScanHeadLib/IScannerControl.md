# PolyScanHeadLib – IScannerControl

## IScannerControl Interface

*Quelle: `PolyScanHeadLib~IScannerControl.html` · Polytec PolyScanHead Type Library*

### Description

Controls the scanners of the scanning head.

### Remarks

It is recommended to cast to the ScannerControl object.


---

## IScannerControl Interface Members

*Quelle: `PolyScanHeadLib~IScannerControl_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| GetBeamPosition | Gets the scanning mirror positions in the quantity of the scanning head. |
|---|---|
| SetBeamPosition | Sets the given scanning mirror position in the quantity of the scanning head. |
| SetupSpeckleTracking | Sets up the speckle tracking. |
| SpeckleTracking | Sets the index of the next speckle tracking position. |
| StartSpeckleTrackingTimer | Starts the speckle tracking. |
| StopSpeckleTrackingTimer | Stops the speckle tracking. |

### Public Properties

| QuantityResolutionX | The D/A resolution of the horizontal scanner in the quantity of the scanning head. |
|---|---|
| QuantityResolutionY | The D/A resolution of the vertical scanner in the quantity of the scanning head. |
| SpeckleTrackingTimerActive | True if the speckle tracking is active. |


---

## GetBeamPosition Method

*Quelle: `PolyScanHeadLib~IScannerControl~GetBeamPosition.html` · Polytec PolyScanHead Type Library · IScannerControl Interface : GetBeamPosition Method*

### Description

Gets the scanning mirror positions in the quantity of the scanning head.

### Syntax

*Visual Basic:*
```
Public Sub GetBeamPosition( _
   ByRef pdPosX As Double, _
   ByRef pdPosY As Double _
)
```

### Parameters

pdPosX

The position of the horizontal scanner.

pdPosY

The position of the vertical scanner.


---

## SetBeamPosition Method

*Quelle: `PolyScanHeadLib~IScannerControl~SetBeamPosition.html` · Polytec PolyScanHead Type Library · IScannerControl Interface : SetBeamPosition Method*

### Description

Sets the given scanning mirror position in the quantity of the scanning head.

### Syntax

*Visual Basic:*
```
Public Function SetBeamPosition( _
   ByVal dPosX As Double, _
   ByVal dPosY As Double _
) As Double
```

### Parameters

dPosX

The position of the horizontal scanner.

dPosY

The position of the vertical scanner.

### Return Type

The waiting time in second between the point where the adjustment of the scanning mirrors is finished and the point where the data acquisition at the new scanning position can start.


---

## SetupSpeckleTracking Method

*Quelle: `PolyScanHeadLib~IScannerControl~SetupSpeckleTracking.html` · Polytec PolyScanHead Type Library · IScannerControl Interface : SetupSpeckleTracking Method*

### Description

Sets up the speckle tracking.

### Syntax

*Visual Basic:*
```
Public Sub SetupSpeckleTracking( _
   ByVal dPeriodInSec As Double, _
   ByVal dRadius As Double, _
   ByVal psaMinorEllipseAxis() As Double, _
   ByVal psaOffsetsForStartIndex() As Double, _
   ByVal psaEllipseRotationAngles() As Double, _
   ByVal psaDistanceCorrectionFactors() As Double _
)
```

### Parameters

dPeriodInSec

The speckle tracking period in second.

dRadius

The speckle tracking radius in the quantity of the scanning head.

psaMinorEllipseAxis

0-based array of the minor ellipse axes for all active scanning heads.

psaOffsetsForStartIndex

0-based array of the start indices for all active scanning heads. The offset for scanning head top is always 0.

psaEllipseRotationAngles

0-based array of the ellipse rotation angles (relative to the up-vector of the corresponding scanning head) for all active scanning heads.

psaDistanceCorrectionFactors

0-based array of distance correction factors for all active scanning heads.


---

## SpeckleTracking Method

*Quelle: `PolyScanHeadLib~IScannerControl~SpeckleTracking.html` · Polytec PolyScanHead Type Library · IScannerControl Interface : SpeckleTracking Method*

### Description

Sets the index of the next speckle tracking position.

### Syntax

*Visual Basic:*
```
Public Sub SpeckleTracking( _
   ByVal lSpeckleTrackingIndex As Long _
)
```

### Parameters

lSpeckleTrackingIndex

The index of the position.


---

## StartSpeckleTrackingTimer Method

*Quelle: `PolyScanHeadLib~IScannerControl~StartSpeckleTrackingTimer.html` · Polytec PolyScanHead Type Library · IScannerControl Interface : StartSpeckleTrackingTimer Method*

### Description

Starts the speckle tracking.

### Syntax

*Visual Basic:*
```
Public Sub StartSpeckleTrackingTimer()
```


---

## StopSpeckleTrackingTimer Method

*Quelle: `PolyScanHeadLib~IScannerControl~StopSpeckleTrackingTimer.html` · Polytec PolyScanHead Type Library · IScannerControl Interface : StopSpeckleTrackingTimer Method*

### Description

Stops the speckle tracking.

### Syntax

*Visual Basic:*
```
Public Sub StopSpeckleTrackingTimer()
```


---

## QuantityResolutionX Property

*Quelle: `PolyScanHeadLib~IScannerControl~QuantityResolutionX.html` · Polytec PolyScanHead Type Library · IScannerControl Interface : QuantityResolutionX Property*

### Description

The D/A resolution of the horizontal scanner in the quantity of the scanning head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property QuantityResolutionX As Double
```


---

## QuantityResolutionY Property

*Quelle: `PolyScanHeadLib~IScannerControl~QuantityResolutionY.html` · Polytec PolyScanHead Type Library · IScannerControl Interface : QuantityResolutionY Property*

### Description

The D/A resolution of the vertical scanner in the quantity of the scanning head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property QuantityResolutionY As Double
```


---

## SpeckleTrackingTimerActive Property

*Quelle: `PolyScanHeadLib~IScannerControl~SpeckleTrackingTimerActive.html` · Polytec PolyScanHead Type Library · IScannerControl Interface : SpeckleTrackingTimerActive Property*

### Description

True if the speckle tracking is active.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SpeckleTrackingTimerActive As Boolean
```
