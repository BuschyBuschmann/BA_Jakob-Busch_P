# PolyScanHeadLib – IComContinuation

## IComContinuation Interface

*Quelle: `PolyScanHeadLib~IComContinuation.html` · Polytec PolyScanHead Type Library*

### Description

The base interface for a continuation of a task implementing the interface IComTask.


---

## IComContinuation Interface Members

*Quelle: `PolyScanHeadLib~IComContinuation_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| Continue | The continuation function called when the passed IComTask -implementing task has finished. |
|---|---|


---

## Continue Method

*Quelle: `PolyScanHeadLib~IComContinuation~Continue.html` · Polytec PolyScanHead Type Library · IComContinuation Interface : Continue Method*

### Description

The continuation function called when the passed IComTask-implementing task has finished.

### Syntax

*Visual Basic:*
```
Public Function Continue( _
   ByVal pIComTask As IComTask _
) As Variant
```

### Parameters

pIComTask

The task to be continued.

### Return Type

The result of the continuation.
