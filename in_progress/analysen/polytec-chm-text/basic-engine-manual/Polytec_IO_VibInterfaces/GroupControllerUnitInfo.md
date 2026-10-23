# Polytec_IO_VibInterfaces – GroupControllerUnitInfo

## GroupControllerUnitInfo Object

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo.html` · Polytec IO VibInterfaces Type Library*

### Description

Provides summary information about the group controller unit.


---

## GroupControllerUnitInfo Object Members

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| HasCap | Returns True if and only if the specified capability is available. |
|---|---|

### Public Properties

| AutoTuningStateFailedIndex | Gets the zero-based index of the automatic tuning state failed. |
|---|---|
| AutoTuningStateSucceededIndex | Gets the zero-based index of the automatic tuning state succeeded. |
| Caps | Gets the group controller unit capabilities. |
| MaxAutoTuningStateIndex | Gets the zero-based index of the maximum automatic tuning state. |
| MaxAutoTuningStateProgressIndex | Gets the zero-based index of the maximum automatic tuning state progress. |
| MaxSyncSourceIndex | Gets the zero-based index of the maximum sync source. |
| MinAutoTuningStateIndex | Gets the zero-based index of the minimum automatic tuning state. |
| MinAutoTuningStateProgressIndex | Gets the zero-based index of the minimum automatic tuning state progress. |
| MinSyncSourceIndex | Gets the zero-based index of the minimum sync source. |
| UniqueID | Gets the unique identifier string. |


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~HasCap.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : HasCap Method*

### Description

Returns True if and only if the specified capability is available.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As GroupControllerUnitCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| GroupControllerUnitCaps_AutoTuningState | The capability that the automatic tuning state can be queried. |
| GroupControllerUnitCaps_ClockSync | The capability that the clock can be synchronized. |
| GroupControllerUnitCaps_HourMeter | The capability that the hour meter seconds and the power switching on/off counter can be queried. |
| GroupControllerUnitCaps_None | None of the capabilities is available. |
| GroupControllerUnitCaps_UniqueID | The capability that the unique identifier can be queried. |
The capability to query.

### Return Type

True if the specified capability is supported.


---

## AutoTuningStateFailedIndex Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~AutoTuningStateFailedIndex.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : AutoTuningStateFailedIndex Property*

### Description

Gets the zero-based index of the automatic tuning state failed.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoTuningStateFailedIndex As Long
```

### Return Type

The automatic tuning state failed index.


---

## AutoTuningStateSucceededIndex Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~AutoTuningStateSucceededIndex.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : AutoTuningStateSucceededIndex Property*

### Description

Gets the zero-based index of the automatic tuning state succeeded.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoTuningStateSucceededIndex As Long
```

### Return Type

The automatic tuning state succeeded index.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~Caps.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : Caps Property*

### Description

Gets the group controller unit capabilities.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As GroupControllerUnitCaps
```

### Return Type

The capabilities.


---

## MaxAutoTuningStateIndex Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~MaxAutoTuningStateIndex.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : MaxAutoTuningStateIndex Property*

### Description

Gets the zero-based index of the maximum automatic tuning state.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxAutoTuningStateIndex As Long
```

### Return Type

The maximum automatic tuning state index.


---

## MaxAutoTuningStateProgressIndex Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~MaxAutoTuningStateProgressIndex.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : MaxAutoTuningStateProgressIndex Property*

### Description

Gets the zero-based index of the maximum automatic tuning state progress.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxAutoTuningStateProgressIndex As Long
```

### Return Type

The maximum automatic tuning state progress index.


---

## MaxSyncSourceIndex Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~MaxSyncSourceIndex.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : MaxSyncSourceIndex Property*

### Description

Gets the zero-based index of the maximum sync source.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxSyncSourceIndex As Long
```

### Return Type

The maximum sync source index.


---

## MinAutoTuningStateIndex Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~MinAutoTuningStateIndex.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : MinAutoTuningStateIndex Property*

### Description

Gets the zero-based index of the minimum automatic tuning state.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinAutoTuningStateIndex As Long
```

### Return Type

The minimum automatic tuning state index.


---

## MinAutoTuningStateProgressIndex Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~MinAutoTuningStateProgressIndex.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : MinAutoTuningStateProgressIndex Property*

### Description

Gets the zero-based index of the minimum automatic tuning state progress.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinAutoTuningStateProgressIndex As Long
```

### Return Type

The minimum automatic tuning state progress index.


---

## MinSyncSourceIndex Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~MinSyncSourceIndex.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : MinSyncSourceIndex Property*

### Description

Gets the zero-based index of the minimum sync source.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinSyncSourceIndex As Long
```

### Return Type

The minimum sync source index.


---

## UniqueID Property

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitInfo~UniqueID.html` · Polytec IO VibInterfaces Type Library · GroupControllerUnitInfo Object : UniqueID Property*

### Description

Gets the unique identifier string.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property UniqueID As String
```

### Return Type

The unique identifier string.
