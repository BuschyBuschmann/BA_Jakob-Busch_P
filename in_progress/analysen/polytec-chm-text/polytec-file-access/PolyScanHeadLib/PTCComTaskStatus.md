# PolyScanHeadLib – PTCComTaskStatus

## PTCComTaskStatus Enumeration

*Quelle: `PolyScanHeadLib~PTCComTaskStatus.html` · Polytec PolyScanHead Type Library*

### Description

Represents the status of a task implementing the interface IComTask.

### Members

| Member | Value | Description |
|---|---|---|
| ptcComTaskCanceled | 3 | The task has been canceled. |
| ptcComTaskCreated | 0 | The task has been created, but is not started yet. |
| ptcComTaskFaulted | 4 | The task function has thrown an exception. |
| ptcComTaskRanToCompletion | 2 | The task has completed normally, i.e. without any canceling or exception. |
| ptcComTaskRunning | 1 | The task is running. |
