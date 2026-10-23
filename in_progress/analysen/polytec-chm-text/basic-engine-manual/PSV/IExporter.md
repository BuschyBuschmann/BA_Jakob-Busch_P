# PSV – IExporter

## IExporter Interface

*Quelle: `PSV~IExporter.html` · Polytec PSV Type Library*

### Description

The exporter.

### Remarks

It is recommended to cast to the Exporter Object.


---

## IExporter Interface Members

*Quelle: `PSV~IExporter_members.html` · Polytec PSV Type Library*

### Public Methods

| CancelAsync | Cancels an asynchronous operation. The method returns at once. The ongoing operation might or might not be canceled. See the cancelled parameter of the corresponding ExportCompleted event to check whether the operation has been canceled. It is legal (and a no-operation) to call this function when no operation is ongoing, i.e. IsBusy is False. |
|---|---|
| Export | Exports the data. |
| ExportAsync | Exports the data. The method returns at once and starts the calculation on a worker thread. Use the ExportCompleted event to receive the result. Calling this method while IsBusy is True results in an error. |
| LoadParameters | Loads the export parameters that were used for the last export via the user interface of the software (VibSoft, PSV or MPV). |

### Public Properties

| IsBusy | Queries whether the export functionality is busy. It is not allowed to start a new operation while this property is True. |
|---|---|


---

## CancelAsync Method

*Quelle: `PSV~IExporter~CancelAsync.html` · Polytec PSV Type Library · IExporter Interface : CancelAsync Method*

### Description

Cancels an asynchronous operation. The method returns at once. The ongoing operation might or might not be canceled. See the cancelled parameter of the corresponding ExportCompleted event to check whether the operation has been canceled. It is legal (and a no-operation) to call this function when no operation is ongoing, i.e. IsBusy is False.

### Syntax

*Visual Basic:*
```
Public Sub CancelAsync()
```


---

## Export Method

*Quelle: `PSV~IExporter~Export.html` · Polytec PSV Type Library · IExporter Interface : Export Method*

### Description

Exports the data.

### Syntax

*Visual Basic:*
```
Public Sub Export( _
   ByVal parameters As IExportParameters _
)
```

### Parameters

parameters

The export parameters.


---

## ExportAsync Method

*Quelle: `PSV~IExporter~ExportAsync.html` · Polytec PSV Type Library · IExporter Interface : ExportAsync Method*

### Description

Exports the data. The method returns at once and starts the calculation on a worker thread. Use the ExportCompleted event to receive the result. Calling this method while IsBusy is True results in an error.

### Syntax

*Visual Basic:*
```
Public Sub ExportAsync( _
   ByVal parameters As IExportParameters _
)
```

### Parameters

parameters

The export parameters.


---

## LoadParameters Method

*Quelle: `PSV~IExporter~LoadParameters.html` · Polytec PSV Type Library · IExporter Interface : LoadParameters Method*

### Description

Loads the export parameters that were used for the last export via the user interface of the software (VibSoft, PSV or MPV).

### Syntax

*Visual Basic:*
```
Public Sub LoadParameters( _
   ByRef parameters As IExportParameters _
)
```

### Parameters

parameters

The export parameters.


---

## IsBusy Property

*Quelle: `PSV~IExporter~IsBusy.html` · Polytec PSV Type Library · IExporter Interface : IsBusy Property*

### Description

Queries whether the export functionality is busy. It is not allowed to start a new operation while this property is True.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsBusy As Boolean
```

### Return Type

True if the export functionality is busy, False otherwise.
