# PolyScanHeadLib – IComTask

## IComTask Interface

*Quelle: `PolyScanHeadLib~IComTask.html` · Polytec PolyScanHead Type Library*

### Description

The base interface for a task representing an asynchronous operation.

### Object Model


---

## IComTask Interface Members

*Quelle: `PolyScanHeadLib~IComTask_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| Cancel | Cancels the task. |
|---|---|
| ContinueWith | Adds a continuation to the task. |
| ThrowException | Throws the exception of a faulted task. |
| TryWait | Tries to wait for the task to complete. |
| TryWaitWithTimeout | Tries to wait for the task to complete within the specified timeout. |
| Wait | Waits for the task to complete. |
| WaitWithTimeout | Waits for the task to complete within the specified timeout. |

### Public Properties

| IsCanceled | Returns a flag value indicating whether the task has been canceled. |
|---|---|
| IsCompleted | Returns a flag value indicating whether the task has completed. |
| IsFaulted | Returns a flag value indicating whether the task has faulted. |
| Result | Waits for the task to complete and returns the result of the task. |
| Status | Returns the current status of the task. |


---

## Cancel Method

*Quelle: `PolyScanHeadLib~IComTask~Cancel.html` · Polytec PolyScanHead Type Library · IComTask Interface : Cancel Method*

### Description

Cancels the task.

### Syntax

*Visual Basic:*
```
Public Sub Cancel()
```


---

## ContinueWith Method

*Quelle: `PolyScanHeadLib~IComTask~ContinueWith.html` · Polytec PolyScanHead Type Library · IComTask Interface : ContinueWith Method*

### Description

Adds a continuation to the task.

### Syntax

*Visual Basic:*
```
Public Function ContinueWith( _
   ByVal pIContinuation As IComContinuation, _
   ByVal pIComScheduler As IComScheduler _
) As IComTask
```

### Parameters

pIContinuation

The continuation.

pIComScheduler

An optional scheduler to be used for the scheduling of the continuation, can be nullptr.

### Return Type

The task representing the continuation.


---

## ThrowException Method

*Quelle: `PolyScanHeadLib~IComTask~ThrowException.html` · Polytec PolyScanHead Type Library · IComTask Interface : ThrowException Method*

### Description

Throws the exception of a faulted task.

### Syntax

*Visual Basic:*
```
Public Sub ThrowException()
```


---

## TryWait Method

*Quelle: `PolyScanHeadLib~IComTask~TryWait.html` · Polytec PolyScanHead Type Library · IComTask Interface : TryWait Method*

### Description

Tries to wait for the task to complete.

### Syntax

*Visual Basic:*
```
Public Function TryWait() As PTCComTaskStatus
```

### Return Type

The status of the completed task. This is expected to be one of the statuses ptcComTaskCanceled, ptcComTaskFaulted, or ptcComTaskRanToCompletion.


---

## TryWaitWithTimeout Method

*Quelle: `PolyScanHeadLib~IComTask~TryWaitWithTimeout.html` · Polytec PolyScanHead Type Library · IComTask Interface : TryWaitWithTimeout Method*

### Description

Tries to wait for the task to complete within the specified timeout.

### Syntax

*Visual Basic:*
```
Public Function TryWaitWithTimeout( _
   ByVal lMillisecondsTimeout As Long _
) As PTCComTaskStatus
```

### Parameters

lMillisecondsTimeout

The timeout in millisecond.

### Return Type

The status of the completed task. This is expected to be one of the statuses ptcComTaskCanceled, ptcComTaskFaulted, ptcComTaskRanToCompletion, or ptcComTaskRunning.


---

## Wait Method

*Quelle: `PolyScanHeadLib~IComTask~Wait.html` · Polytec PolyScanHead Type Library · IComTask Interface : Wait Method*

### Description

Waits for the task to complete.

### Syntax

*Visual Basic:*
```
Public Sub Wait()
```

### Remarks

This method is expected to fail when the task has been canceled or has faulted.


---

## WaitWithTimeout Method

*Quelle: `PolyScanHeadLib~IComTask~WaitWithTimeout.html` · Polytec PolyScanHead Type Library · IComTask Interface : WaitWithTimeout Method*

### Description

Waits for the task to complete within the specified timeout.

### Syntax

*Visual Basic:*
```
Public Function WaitWithTimeout( _
   ByVal lMillisecondsTimeout As Long _
) As Boolean
```

### Parameters

lMillisecondsTimeout

The timeout in millisecond.

### Return Type

True when the task completed within the specified timeout.


---

## IsCanceled Property

*Quelle: `PolyScanHeadLib~IComTask~IsCanceled.html` · Polytec PolyScanHead Type Library · IComTask Interface : IsCanceled Property*

### Description

Returns a flag value indicating whether the task has been canceled.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsCanceled As Boolean
```


---

## IsCompleted Property

*Quelle: `PolyScanHeadLib~IComTask~IsCompleted.html` · Polytec PolyScanHead Type Library · IComTask Interface : IsCompleted Property*

### Description

Returns a flag value indicating whether the task has completed.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsCompleted As Boolean
```


---

## IsFaulted Property

*Quelle: `PolyScanHeadLib~IComTask~IsFaulted.html` · Polytec PolyScanHead Type Library · IComTask Interface : IsFaulted Property*

### Description

Returns a flag value indicating whether the task has faulted.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsFaulted As Boolean
```


---

## Result Property

*Quelle: `PolyScanHeadLib~IComTask~Result.html` · Polytec PolyScanHead Type Library · IComTask Interface : Result Property*

### Description

Waits for the task to complete and returns the result of the task.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Result As Variant
```

### Return Type

The result of the task.

### Remarks

Calling this property is expected to fail when the task has been canceled or has faulted.


---

## Status Property

*Quelle: `PolyScanHeadLib~IComTask~Status.html` · Polytec PolyScanHead Type Library · IComTask Interface : Status Property*

### Description

Returns the current status of the task.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Status As PTCComTaskStatus
```

### Return Type

The task status.
