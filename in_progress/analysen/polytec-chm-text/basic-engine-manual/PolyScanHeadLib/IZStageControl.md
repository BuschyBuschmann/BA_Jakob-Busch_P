# PolyScanHeadLib – IZStageControl

## IZStageControl Interface

*Quelle: `PolyScanHeadLib~IZStageControl.html` · Polytec PolyScanHead Type Library*

### Description

This object controls the z-stage of the MSA-500 system used for focusing the laser beam and measuring distances.

### Remarks

It is recommended to cast to the ZStageControl object.


---

## IZStageControl Interface Members

*Quelle: `PolyScanHeadLib~IZStageControl_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| ConnectByType | Connects to the controller of the z-stage of the given type. |
|---|---|
| Disconnect | Disconnects the z-stage controller. |
| FocusScanReinit | Reinitializes the focus scan. |
| GetEvalFocus | Returns the focus position of the maximum signal level in the given time trace. |
| GetMoveTime | Returns the estimated time to move the z-stage from position1 to position2 in second. |
| NotchTuning | Performs the tuning of the notch filter of the z-stage. |
| StartFocus | Runs a focus measurement. After acquisition is completed, call GetEvalFocus() with the time trace of the signal level to get the focus position. |
| StartMoveTo | Starts a single movement to the target position with the given velocity. The movement can be stopped by calling Stop() . |
| Stop | Stops focusing. |
| WaitForPositionReached | Waits until the target position is reached. |

### Public Properties

| Connected | True, if there is a connection to the controller of the z-stage. |
|---|---|
| MovementInProgress | True, if the movement of the z-stage is in progress, e.g. StartFocus or StartMoveTo are in progress and Stop was not called yet. |
| Position | Specifies the current position of the z-stage in meter. |
| PositionMax | The maximum value for the position in meter. |
| PositionMin | The minimum value for the position in meter. |
| PositionReached | True if the target position has been reached. |
| PTerm | Specifies the P-term of the z-stage. |


---

## ConnectByType Method

*Quelle: `PolyScanHeadLib~IZStageControl~ConnectByType.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : ConnectByType Method*

### Description

Connects to the controller of the z-stage of the given type.

### Syntax

*Visual Basic:*
```
Public Function ConnectByType( _
   ByVal ptcType As PTCZStageType _
) As String
```

### Parameters

ptcType

| Value | Description |
|---|---|
| ptcZStageE7XX | E7XX z-stage |
| ptcZStageGCS2 | GCS2 z-stage |
| ptcZStageGCS2_E709 | GCS2 E709 z-stage |
| ptcZStageNone | No z-stage |
| ptcZStageSimulation | Simulated z-stage |
The type of the z-stage.


---

## Disconnect Method

*Quelle: `PolyScanHeadLib~IZStageControl~Disconnect.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : Disconnect Method*

### Description

Disconnects the z-stage controller.

### Syntax

*Visual Basic:*
```
Public Sub Disconnect()
```


---

## FocusScanReinit Method

*Quelle: `PolyScanHeadLib~IZStageControl~FocusScanReinit.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : FocusScanReinit Method*

### Description

Reinitializes the focus scan.

### Syntax

*Visual Basic:*
```
Public Sub FocusScanReinit( _
   ByVal pIZStageSettings As ZStageSettings _
)
```

### Parameters

pIZStageSettings

The settings of the z-stage.

### Remarks

After approximately every 50 periods it is necessary to reinitialize the z-stage.


---

## GetEvalFocus Method

*Quelle: `PolyScanHeadLib~IZStageControl~GetEvalFocus.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : GetEvalFocus Method*

### Description

Returns the focus position of the maximum signal level in the given time trace.

### Syntax

*Visual Basic:*
```
Public Function GetEvalFocus( _
   ByVal ptcVal As PTCZStageFocusType, _
   ByVal pIZStageSettings As ZStageSettings, _
   ByVal psaData() As Single, _
   ByVal dSampleFreq As Double, _
   ByVal dFitWidth As Double _
) As Double
```

### Parameters

ptcVal

| Value | Description |
|---|---|
| ptcZStageAutoFocus | The focus type is AutoFocus. |
| ptcZStageScanFocus | The focus type is focus scan. |
The type of the focus.

pIZStageSettings

The settings of the z-stage.

psaData

The array of signal values of the time trace.

dSampleFreq

The sample frequency of the time trace.

dFitWidth

The width of the time range for the fit of one peak in second.

### Return Type

The focus position in meter.


---

## GetMoveTime Method

*Quelle: `PolyScanHeadLib~IZStageControl~GetMoveTime.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : GetMoveTime Method*

### Description

Returns the estimated time to move the z-stage from position1 to position2 in second.

### Syntax

*Visual Basic:*
```
Public Function GetMoveTime( _
   ByVal dPosition1 As Double, _
   ByVal dPosition2 As Double _
) As Double
```

### Parameters

dPosition1

The start position in meter.

dPosition2

The end position in meter.

### Return Type

The estimated time in second.


---

## NotchTuning Method

*Quelle: `PolyScanHeadLib~IZStageControl~NotchTuning.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : NotchTuning Method*

### Description

Performs the tuning of the notch filter of the z-stage.

### Syntax

*Visual Basic:*
```
Public Sub NotchTuning()
```

### Remarks

This should be done when objectives are attached to or removed from the MSA scan head.

Beginning with the software releases in July 2018, a "lens" is called "objective" in the GUI of the applications.


---

## StartFocus Method

*Quelle: `PolyScanHeadLib~IZStageControl~StartFocus.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : StartFocus Method*

### Description

Runs a focus measurement. After acquisition is completed, call GetEvalFocus() with the time trace of the signal level to get the focus position.

### Syntax

*Visual Basic:*
```
Public Sub StartFocus( _
   ByVal ptcVal As PTCZStageFocusType, _
   ByVal pIZStageSettings As ZStageSettings _
)
```

### Parameters

ptcVal

| Value | Description |
|---|---|
| ptcZStageAutoFocus | The focus type is AutoFocus. |
| ptcZStageScanFocus | The focus type is focus scan. |
The type of focus.

pIZStageSettings

The z-stage settings.


---

## StartMoveTo Method

*Quelle: `PolyScanHeadLib~IZStageControl~StartMoveTo.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : StartMoveTo Method*

### Description

Starts a single movement to the target position with the given velocity. The movement can be stopped by calling Stop().

### Syntax

*Visual Basic:*
```
Public Sub StartMoveTo( _
   ByVal dTargetPosition As Double, _
   ByVal dVelocity As Double _
)
```

### Parameters

dTargetPosition

The target position in meter.

dVelocity

The velocity in meter/second.


---

## Stop Method

*Quelle: `PolyScanHeadLib~IZStageControl~Stop.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : Stop Method*

### Description

Stops focusing.

### Syntax

*Visual Basic:*
```
Public Sub Stop()
```


---

## WaitForPositionReached Method

*Quelle: `PolyScanHeadLib~IZStageControl~WaitForPositionReached.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : WaitForPositionReached Method*

### Description

Waits until the target position is reached.

### Syntax

*Visual Basic:*
```
Public Sub WaitForPositionReached()
```


---

## Connected Property

*Quelle: `PolyScanHeadLib~IZStageControl~Connected.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : Connected Property*

### Description

True, if there is a connection to the controller of the z-stage.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Connected As Boolean
```


---

## MovementInProgress Property

*Quelle: `PolyScanHeadLib~IZStageControl~MovementInProgress.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : MovementInProgress Property*

### Description

True, if the movement of the z-stage is in progress, e.g. StartFocus or StartMoveTo are in progress and Stop was not called yet.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MovementInProgress As Boolean
```


---

## Position Property

*Quelle: `PolyScanHeadLib~IZStageControl~Position.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : Position Property*

### Description

Specifies the current position of the z-stage in meter.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Position As Double
```


---

## PositionMax Property

*Quelle: `PolyScanHeadLib~IZStageControl~PositionMax.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : PositionMax Property*

### Description

The maximum value for the position in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionMax As Double
```


---

## PositionMin Property

*Quelle: `PolyScanHeadLib~IZStageControl~PositionMin.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : PositionMin Property*

### Description

The minimum value for the position in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionMin As Double
```


---

## PositionReached Property

*Quelle: `PolyScanHeadLib~IZStageControl~PositionReached.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : PositionReached Property*

### Description

True if the target position has been reached.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionReached As Boolean
```


---

## PTerm Property

*Quelle: `PolyScanHeadLib~IZStageControl~PTerm.html` · Polytec PolyScanHead Type Library · IZStageControl Interface : PTerm Property*

### Description

Specifies the P-term of the z-stage.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PTerm As Double
```
