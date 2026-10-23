# PolyScanHeadLib – ScannerControl

## ScannerControl Object

*Quelle: `PolyScanHeadLib~ScannerControl.html` · Polytec PolyScanHead Type Library*

### Description

Controls the scanners of the scanning head.


---

## ScannerControl Object Members

*Quelle: `PolyScanHeadLib~ScannerControl_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| GetBeamPosition | Gets the scanning mirror positions in the quantity of the scanning head. |
|---|---|
| GetBeamPositionSecondScanner | Gets the scanning mirror positions of the second scanner in the quantity of the scanning head. |
| SetBeamPosition | Sets the given scanning mirror position in the quantity of the scanning head. |
| SetBeamPositionSecondScanner | Sets the given scanning mirror position for the second scanner in the quantity of the scanning head. |
| SetOffsetForRemeasure | Sets the offset that is applied to the scanners during re-measure. |
| SetupSpeckleTracking | Sets up the speckle tracking. |
| SpeckleTracking | Sets the index of the next speckle tracking position. |
| StartSpeckleTrackingTimer | Starts the speckle tracking. |
| StopSpeckleTrackingTimer | Stops the speckle tracking. |
| TriggerUpdateScannerPosition | method TriggerUpdateScannerPosition, updates the internal scanner values while scanning autonomously. |

### Public Properties

| AutonomousScanSupported | Returns true, if the autonomous scan mode is supported. |
|---|---|
| HasSecondScanner | Queries whether the referenced scan head device has a second scanner. |
| MovingTime | Gets the moving time of the scanners in seconds. |
| Name | The name of the scanner control. |
| QuantityResolutionX | The D/A resolution of the horizontal scanner in the quantity of the scanning head. |
| QuantityResolutionY | The D/A resolution of the vertical scanner in the quantity of the scanning head. |
| SpeckleTrackingTimerActive | True if the speckle tracking is active. |


---

## GetBeamPosition Method

*Quelle: `PolyScanHeadLib~ScannerControl~GetBeamPosition.html` · Polytec PolyScanHead Type Library · ScannerControl Object : GetBeamPosition Method*

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

## GetBeamPositionSecondScanner Method

*Quelle: `PolyScanHeadLib~ScannerControl~GetBeamPositionSecondScanner.html` · Polytec PolyScanHead Type Library · ScannerControl Object : GetBeamPositionSecondScanner Method*

### Description

Gets the scanning mirror positions of the second scanner in the quantity of the scanning head.

### Syntax

*Visual Basic:*
```
Public Sub GetBeamPositionSecondScanner( _
   ByRef posX As Double, _
   ByRef posY As Double _
)
```

### Parameters

posX

The position of the horizontal scanner.

posY

The position of the vertical scanner.


---

## SetBeamPosition Method

*Quelle: `PolyScanHeadLib~ScannerControl~SetBeamPosition.html` · Polytec PolyScanHead Type Library · ScannerControl Object : SetBeamPosition Method*

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

## SetBeamPositionSecondScanner Method

*Quelle: `PolyScanHeadLib~ScannerControl~SetBeamPositionSecondScanner.html` · Polytec PolyScanHead Type Library · ScannerControl Object : SetBeamPositionSecondScanner Method*

### Description

Sets the given scanning mirror position for the second scanner in the quantity of the scanning head.

### Syntax

*Visual Basic:*
```
Public Function SetBeamPositionSecondScanner( _
   ByVal posX As Double, _
   ByVal posY As Double _
) As Double
```

### Parameters

posX

The position of the horizontal scanner.

posY

The position of the vertical scanner.

### Return Type

The waiting time in second between the point where the adjustment of the scanning mirrors is finished and the point where the data acquisition at the new scanning position can start.


---

## SetOffsetForRemeasure Method

*Quelle: `PolyScanHeadLib~ScannerControl~SetOffsetForRemeasure.html` · Polytec PolyScanHead Type Library · ScannerControl Object : SetOffsetForRemeasure Method*

### Description

Sets the offset that is applied to the scanners during re-measure.

### Syntax

*Visual Basic:*
```
Public Sub SetOffsetForRemeasure( _
   ByVal offsetForRemeasure As Long _
)
```

### Parameters

offsetForRemeasure

The offset for the scanners in scanner DAC positions.


---

## SetupSpeckleTracking Method

*Quelle: `PolyScanHeadLib~ScannerControl~SetupSpeckleTracking.html` · Polytec PolyScanHead Type Library · ScannerControl Object : SetupSpeckleTracking Method*

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

*Quelle: `PolyScanHeadLib~ScannerControl~SpeckleTracking.html` · Polytec PolyScanHead Type Library · ScannerControl Object : SpeckleTracking Method*

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

*Quelle: `PolyScanHeadLib~ScannerControl~StartSpeckleTrackingTimer.html` · Polytec PolyScanHead Type Library · ScannerControl Object : StartSpeckleTrackingTimer Method*

### Description

Starts the speckle tracking.

### Syntax

*Visual Basic:*
```
Public Sub StartSpeckleTrackingTimer()
```


---

## StopSpeckleTrackingTimer Method

*Quelle: `PolyScanHeadLib~ScannerControl~StopSpeckleTrackingTimer.html` · Polytec PolyScanHead Type Library · ScannerControl Object : StopSpeckleTrackingTimer Method*

### Description

Stops the speckle tracking.

### Syntax

*Visual Basic:*
```
Public Sub StopSpeckleTrackingTimer()
```


---

## TriggerUpdateScannerPosition Method

*Quelle: `PolyScanHeadLib~ScannerControl~TriggerUpdateScannerPosition.html` · Polytec PolyScanHead Type Library · ScannerControl Object : TriggerUpdateScannerPosition Method*

### Description

method TriggerUpdateScannerPosition, updates the internal scanner values while scanning autonomously.

### Syntax

*Visual Basic:*
```
Public Sub TriggerUpdateScannerPosition()
```


---

## AutonomousScanSupported Property

*Quelle: `PolyScanHeadLib~ScannerControl~AutonomousScanSupported.html` · Polytec PolyScanHead Type Library · ScannerControl Object : AutonomousScanSupported Property*

### Description

Returns true, if the autonomous scan mode is supported.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutonomousScanSupported As Boolean
```

### Return Type

True, if the autonomous scan mode is supported.


---

## HasSecondScanner Property

*Quelle: `PolyScanHeadLib~ScannerControl~HasSecondScanner.html` · Polytec PolyScanHead Type Library · ScannerControl Object : HasSecondScanner Property*

### Description

Queries whether the referenced scan head device has a second scanner.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasSecondScanner As Boolean
```


---

## MovingTime Property

*Quelle: `PolyScanHeadLib~ScannerControl~MovingTime.html` · Polytec PolyScanHead Type Library · ScannerControl Object : MovingTime Property*

### Description

Gets the moving time of the scanners in seconds.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MovingTime As Double
```

### Return Type

The moving time in seconds.


---

## Name Property

*Quelle: `PolyScanHeadLib~ScannerControl~Name.html` · Polytec PolyScanHead Type Library · ScannerControl Object : Name Property*

### Description

The name of the scanner control.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## QuantityResolutionX Property

*Quelle: `PolyScanHeadLib~ScannerControl~QuantityResolutionX.html` · Polytec PolyScanHead Type Library · ScannerControl Object : QuantityResolutionX Property*

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

*Quelle: `PolyScanHeadLib~ScannerControl~QuantityResolutionY.html` · Polytec PolyScanHead Type Library · ScannerControl Object : QuantityResolutionY Property*

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

*Quelle: `PolyScanHeadLib~ScannerControl~SpeckleTrackingTimerActive.html` · Polytec PolyScanHead Type Library · ScannerControl Object : SpeckleTrackingTimerActive Property*

### Description

True if the speckle tracking is active.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SpeckleTrackingTimerActive As Boolean
```
