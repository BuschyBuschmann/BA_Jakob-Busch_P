# PolyScanHeadLib – IComScheduler

## IComScheduler Interface

*Quelle: `PolyScanHeadLib~IComScheduler.html` · Polytec PolyScanHead Type Library*

### Description

The base interface of a scheduler that executes functions implementing the IComFunction interface.


---

## IComScheduler Interface Members

*Quelle: `PolyScanHeadLib~IComScheduler_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| Schedule | Schedules the specified function for execution. |
|---|---|


---

## Schedule Method

*Quelle: `PolyScanHeadLib~IComScheduler~Schedule.html` · Polytec PolyScanHead Type Library · IComScheduler Interface : Schedule Method*

### Description

Schedules the specified function for execution.

### Syntax

*Visual Basic:*
```
Public Sub Schedule( _
   ByVal pIComFunction As IComFunction _
)
```

### Parameters

pIComFunction

The function to schedule.
