# Polytec_IO_VibInterfaces – IGroupControllerUnit

## IGroupControllerUnit Interface

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit.html` · Polytec IO VibInterfaces Type Library*

### Description

This interface is provided for the MPV system , e.g. for the case where one hardware controller unit is used for all sensor heads/sondes of the controller group. Thus, some commands are only available for such unit and are not supported for the individual controller units.

In particular, please note that this interface is not used to group individual controller units.

### Object Model


---

## IGroupControllerUnit Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| ReadHourMeterData | Reads the hour meter seconds and the power switching on/off counter from the hardware. |
|---|---|
| StartAutoTuning | Starts the automatic tuning of the LiNbO3 shifter. |

### Public Properties

| AutoTuningFailed | Gets a value indicating whether the automatic tuning failed. |
|---|---|
| AutoTuningInProgress | Gets a value indicating whether the automatic tuning is in progress. |
| AutoTuningState | Gets the state of the automatic tuning. |
| AutoTuningSucceeded | Gets a value indicating whether the automatic tuning succeeded. |
| ClockIsSynchronized | Gets a value indicating whether the clock is synchronized. |
| GroupControllerUnitInfo | Gets information describing the group controller unit. |
| NeedAutoTuning | Gets a value indicating whether an automatic tuning is needed. |


---

## ReadHourMeterData Method

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit~ReadHourMeterData.html` · Polytec IO VibInterfaces Type Library · IGroupControllerUnit Interface : ReadHourMeterData Method*

### Description

Reads the hour meter seconds and the power switching on/off counter from the hardware.

### Syntax

*Visual Basic:*
```
Public Function ReadHourMeterData() As Long()
```

### Return Type

The array of hour meter seconds and the power switching on/off counter.


---

## StartAutoTuning Method

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit~StartAutoTuning.html` · Polytec IO VibInterfaces Type Library · IGroupControllerUnit Interface : StartAutoTuning Method*

### Description

Starts the automatic tuning of the LiNbO3 shifter.

### Syntax

*Visual Basic:*
```
Public Sub StartAutoTuning()
```


---

## AutoTuningFailed Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit~AutoTuningFailed.html` · Polytec IO VibInterfaces Type Library · IGroupControllerUnit Interface : AutoTuningFailed Property*

### Description

Gets a value indicating whether the automatic tuning failed.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoTuningFailed As Boolean
```

### Return Type

True if and only if the automatic tuning failed.


---

## AutoTuningInProgress Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit~AutoTuningInProgress.html` · Polytec IO VibInterfaces Type Library · IGroupControllerUnit Interface : AutoTuningInProgress Property*

### Description

Gets a value indicating whether the automatic tuning is in progress.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoTuningInProgress As Boolean
```

### Return Type

True if and only if the automatic tuning is in progress.


---

## AutoTuningState Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit~AutoTuningState.html` · Polytec IO VibInterfaces Type Library · IGroupControllerUnit Interface : AutoTuningState Property*

### Description

Gets the state of the automatic tuning.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoTuningState As Long
```

### Return Type

The automatic tuning state.


---

## AutoTuningSucceeded Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit~AutoTuningSucceeded.html` · Polytec IO VibInterfaces Type Library · IGroupControllerUnit Interface : AutoTuningSucceeded Property*

### Description

Gets a value indicating whether the automatic tuning succeeded.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoTuningSucceeded As Boolean
```

### Return Type

True if and only if the automatic tuning succeeded.


---

## ClockIsSynchronized Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit~ClockIsSynchronized.html` · Polytec IO VibInterfaces Type Library · IGroupControllerUnit Interface : ClockIsSynchronized Property*

### Description

Gets a value indicating whether the clock is synchronized.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ClockIsSynchronized As Boolean
```

### Return Type

True if and only if the clock is synchronized.


---

## GroupControllerUnitInfo Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit~GroupControllerUnitInfo.html` · Polytec IO VibInterfaces Type Library · IGroupControllerUnit Interface : GroupControllerUnitInfo Property*

### Description

Gets information describing the group controller unit.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GroupControllerUnitInfo As GroupControllerUnitInfo
```

### Return Type

The object holding the information about the group controller unit.


---

## NeedAutoTuning Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupControllerUnit~NeedAutoTuning.html` · Polytec IO VibInterfaces Type Library · IGroupControllerUnit Interface : NeedAutoTuning Property*

### Description

Gets a value indicating whether an automatic tuning is needed.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property NeedAutoTuning As Boolean
```

### Return Type

True if and only if an automatic tuning is needed.
