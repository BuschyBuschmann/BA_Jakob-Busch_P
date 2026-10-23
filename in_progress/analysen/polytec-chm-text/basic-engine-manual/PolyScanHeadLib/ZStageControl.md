# PolyScanHeadLib – ZStageControl

## ZStageControl Object

*Quelle: `PolyScanHeadLib~ZStageControl.html` · Polytec PolyScanHead Type Library*

### Description

This object controls the z-stage of the MSA-500 system used for focusing the laser beam and measuring distances.


---

## ZStageControl Object Members

*Quelle: `PolyScanHeadLib~ZStageControl_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| ConnectByType | Connects to the controller of the z-stage of the given type. |
|---|---|
| DisableTrigger | Disables the trigger. |
| Disconnect | Disconnects the z-stage controller. |
| EvaluateAccDistance | Finds the acceleration distance. |
| EvaluateLinearMove | Evaluates the parameters of linear z-stage movement with simultaneous generation of trigger pulses. |
| EvaluateLinearMove2 | Finds the trigger distance and the number of trigger pulses. |
| FocusScanReinit | Reinitializes the focus scan. |
| GetEvalFocus | Returns the focus position of the maximum signal level in the given time trace. |
| GetMoveTime | Returns the estimated time to move the z-stage from position1 to position2 in second. |
| NotchTuning | Performs the tuning of the notch filter of the z-stage. |
| Park | Moves the stage to a pre-defined parking position. |
| StartFocus | Runs a focus measurement. After acquisition is completed, call GetEvalFocus() with the time trace of the signal level to get the focus position. |
| StartLinearMove | Starts a linear move of the z-stage with simultaneous generation of trigger pulses. |
| StartLinearMove2 | Starts a linear move. |
| StartMoveTo | Starts a single movement to the target position with the given velocity. The movement can be stopped by calling Stop() . |
| Stop | Stops focusing. |
| Unpark | Retracts the stage from the pre-defined parking position. |
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

*Quelle: `PolyScanHeadLib~ZStageControl~ConnectByType.html` · Polytec PolyScanHead Type Library · ZStageControl Object : ConnectByType Method*

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

## DisableTrigger Method

*Quelle: `PolyScanHeadLib~ZStageControl~DisableTrigger.html` · Polytec PolyScanHead Type Library · ZStageControl Object : DisableTrigger Method*

### Description

Disables the trigger.

### Syntax

*Visual Basic:*
```
Public Sub DisableTrigger()
```


---

## Disconnect Method

*Quelle: `PolyScanHeadLib~ZStageControl~Disconnect.html` · Polytec PolyScanHead Type Library · ZStageControl Object : Disconnect Method*

### Description

Disconnects the z-stage controller.

### Syntax

*Visual Basic:*
```
Public Sub Disconnect()
```


---

## EvaluateAccDistance Method

*Quelle: `PolyScanHeadLib~ZStageControl~EvaluateAccDistance.html` · Polytec PolyScanHead Type Library · ZStageControl Object : EvaluateAccDistance Method*

### Description

Finds the acceleration distance.

### Syntax

*Visual Basic:*
```
Public Sub EvaluateAccDistance( _
   ByVal Velocity As Double, _
   ByVal Acceleration As Double, _
   ByVal length As Double, _
   ByRef accDistance As Double _
)
```

### Parameters

Velocity

The velocity.

Acceleration

The acceleration.

length

The length.

accDistance

The acceleration distance.


---

## EvaluateLinearMove Method

*Quelle: `PolyScanHeadLib~ZStageControl~EvaluateLinearMove.html` · Polytec PolyScanHead Type Library · ZStageControl Object : EvaluateLinearMove Method*

### Description

Evaluates the parameters of linear z-stage movement with simultaneous generation of trigger pulses.

### Syntax

*Visual Basic:*
```
Public Sub EvaluateLinearMove( _
   ByVal dVelocity As Double, _
   ByVal dAcceleration As Double, _
   ByVal dLength As Double, _
   ByRef pdTriggerInterval As Double, _
   ByRef pdAccDistance As Double _
)
```

### Parameters

dVelocity

The requested movement velocity in meter/second.

dAcceleration

The requested movement acceleration in meter/second^2.

dLength

The requested movement length.

pdTriggerInterval

On input the requested trigger pulse distance in meter. On output the resulting distance.

pdAccDistance

The distance necessary for accelerating / breaking in meter.


---

## EvaluateLinearMove2 Method

*Quelle: `PolyScanHeadLib~ZStageControl~EvaluateLinearMove2.html` · Polytec PolyScanHead Type Library · ZStageControl Object : EvaluateLinearMove2 Method*

### Description

Finds the trigger distance and the number of trigger pulses.

### Syntax

*Visual Basic:*
```
Public Sub EvaluateLinearMove2( _
   ByRef zStageLinearMoveSettings As IZStageMoveLinearSettings2, _
   ByRef triggerCount As Long _
)
```

### Parameters

zStageLinearMoveSettings

The linear move settings.

triggerCount

The trigger count.


---

## FocusScanReinit Method

*Quelle: `PolyScanHeadLib~ZStageControl~FocusScanReinit.html` · Polytec PolyScanHead Type Library · ZStageControl Object : FocusScanReinit Method*

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

*Quelle: `PolyScanHeadLib~ZStageControl~GetEvalFocus.html` · Polytec PolyScanHead Type Library · ZStageControl Object : GetEvalFocus Method*

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

*Quelle: `PolyScanHeadLib~ZStageControl~GetMoveTime.html` · Polytec PolyScanHead Type Library · ZStageControl Object : GetMoveTime Method*

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

*Quelle: `PolyScanHeadLib~ZStageControl~NotchTuning.html` · Polytec PolyScanHead Type Library · ZStageControl Object : NotchTuning Method*

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

## Park Method

*Quelle: `PolyScanHeadLib~ZStageControl~Park.html` · Polytec PolyScanHead Type Library · ZStageControl Object : Park Method*

### Description

Moves the stage to a pre-defined parking position.

### Syntax

*Visual Basic:*
```
Public Sub Park()
```


---

## StartFocus Method

*Quelle: `PolyScanHeadLib~ZStageControl~StartFocus.html` · Polytec PolyScanHead Type Library · ZStageControl Object : StartFocus Method*

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

## StartLinearMove Method

*Quelle: `PolyScanHeadLib~ZStageControl~StartLinearMove.html` · Polytec PolyScanHead Type Library · ZStageControl Object : StartLinearMove Method*

### Description

Starts a linear move of the z-stage with simultaneous generation of trigger pulses.

### Syntax

*Visual Basic:*
```
Public Sub StartLinearMove( _
   ByVal pIZStageLinearMoveSettings As IZStageMoveLinearSettings, _
   ByRef pdFirstTriggerPosition As Double, _
   ByRef pdActualTriggerInterval As Double, _
   ByRef plTriggerCount As Long _
)
```

### Parameters

pIZStageLinearMoveSettings

The settings for the movement.

pdFirstTriggerPosition

The position of the first trigger pulse in meter.

pdActualTriggerInterval

The distance between two trigger pulses in meter.

plTriggerCount

The total number of trigger pulses.


---

## StartLinearMove2 Method

*Quelle: `PolyScanHeadLib~ZStageControl~StartLinearMove2.html` · Polytec PolyScanHead Type Library · ZStageControl Object : StartLinearMove2 Method*

### Description

Starts a linear move.

### Syntax

*Visual Basic:*
```
Public Sub StartLinearMove2( _
   ByRef zStageLinearMoveSettings As IZStageMoveLinearSettings2, _
   ByRef firstTriggerPosition As Double, _
   ByRef triggerCount As Long _
)
```

### Parameters

zStageLinearMoveSettings

The linear move settings.

firstTriggerPosition

The first trigger position.

triggerCount

The trigger count.


---

## StartMoveTo Method

*Quelle: `PolyScanHeadLib~ZStageControl~StartMoveTo.html` · Polytec PolyScanHead Type Library · ZStageControl Object : StartMoveTo Method*

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

*Quelle: `PolyScanHeadLib~ZStageControl~Stop.html` · Polytec PolyScanHead Type Library · ZStageControl Object : Stop Method*

### Description

Stops focusing.

### Syntax

*Visual Basic:*
```
Public Sub Stop()
```


---

## Unpark Method

*Quelle: `PolyScanHeadLib~ZStageControl~Unpark.html` · Polytec PolyScanHead Type Library · ZStageControl Object : Unpark Method*

### Description

Retracts the stage from the pre-defined parking position.

### Syntax

*Visual Basic:*
```
Public Sub Unpark()
```


---

## WaitForPositionReached Method

*Quelle: `PolyScanHeadLib~ZStageControl~WaitForPositionReached.html` · Polytec PolyScanHead Type Library · ZStageControl Object : WaitForPositionReached Method*

### Description

Waits until the target position is reached.

### Syntax

*Visual Basic:*
```
Public Sub WaitForPositionReached()
```


---

## Connected Property

*Quelle: `PolyScanHeadLib~ZStageControl~Connected.html` · Polytec PolyScanHead Type Library · ZStageControl Object : Connected Property*

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

*Quelle: `PolyScanHeadLib~ZStageControl~MovementInProgress.html` · Polytec PolyScanHead Type Library · ZStageControl Object : MovementInProgress Property*

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

*Quelle: `PolyScanHeadLib~ZStageControl~Position.html` · Polytec PolyScanHead Type Library · ZStageControl Object : Position Property*

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

*Quelle: `PolyScanHeadLib~ZStageControl~PositionMax.html` · Polytec PolyScanHead Type Library · ZStageControl Object : PositionMax Property*

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

*Quelle: `PolyScanHeadLib~ZStageControl~PositionMin.html` · Polytec PolyScanHead Type Library · ZStageControl Object : PositionMin Property*

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

*Quelle: `PolyScanHeadLib~ZStageControl~PositionReached.html` · Polytec PolyScanHead Type Library · ZStageControl Object : PositionReached Property*

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

*Quelle: `PolyScanHeadLib~ZStageControl~PTerm.html` · Polytec PolyScanHead Type Library · ZStageControl Object : PTerm Property*

### Description

Specifies the P-term of the z-stage.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PTerm As Double
```
