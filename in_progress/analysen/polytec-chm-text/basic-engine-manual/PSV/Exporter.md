# PSV – Exporter

## Exporter Object

*Quelle: `PSV~Exporter.html` · Polytec PSV Type Library*

### Description

The Exporter object allows to export geometry and measurement data from a .pvd, .svd , .mvd or .set file to one of the supported file formats.

### Remarks

To create an instance of this object use the Exporter Property of the application or the Exporter Property of the document.

### Example

The example demonstrates how to export data synchronously or asynchronously to the various file formats while showing progress.

- Example (Visual Basic)

```
#Language "WWB.Net"

Option Explicit

Imports System
Imports System.Collections.Generic

Dim g_completed As Boolean

Dim WithEvents g_exporterEvents As Exporter

Public Sub g_exporterEvents_ExportCompleted(ByVal cancelled As Boolean, ByVal errorOccurred As Boolean, ByVal errorMessage As String) Handles g_exporterEvents.ExportCompleted
  Dim exportCompletedText = "Export completed: "
  If errorOccurred Then
    exportCompletedText = exportCompletedText + "Error occurred: " + errorMessage.ToString()
  ElseIf cancelled Then
    exportCompletedText = exportCompletedText + "Export cancelled."
  End If
  Debug.WriteLine(exportCompletedText)
  g_completed = True
End Sub

Public Sub g_exporterEvents_IsBusyChanged(ByVal IsBusyChanged As Boolean) Handles g_exporterEvents.IsBusyChanged
  Dim busyChangedText = "Busy changed: " + IsBusyChanged.ToString()
  Debug.WriteLine(busyChangedText)
End Sub

Public Sub g_exporterEvents_ProgressChanged(ByVal progress As Integer) Handles g_exporterEvents.ProgressChanged
  Dim progressChangedText = "Progress changed: " + progress.ToString()
  Debug.WriteLine(progressChangedText)
  If progress > 50 Then
    'g_exporterEvents.CancelAsync()
  End If
End Sub

Sub Main
  Debug.Clear
  g_completed = False

  Dim expParams As New ExportParameters

  ExportToFile("D:\Data\Settings90.set", PTCExportType.ptcExportTypeUniversalFile, expParams, True, "D:\Data\Settings90.unv")
  ExportToFileAsync("D:\Data\Settings90.set", PTCExportType.ptcExportTypeAsamOdsAtfx, expParams, False, "D:\Data\Settings90.atfx")

  ExportToFile("D:\Data\Example_new.svd", PTCExportType.ptcExportTypeUniversalFile, expParams, True, "D:\Data\ExampleTest_new.unv")
  ExportToFile("D:\Data\Example_new.svd", PTCExportType.ptcExportTypeMEScope, expParams, True, "D:\Data\ExampleTest_new.str")
  ExportToFileAsync("D:\Data\Example_new.svd", PTCExportType.ptcExportTypeAsamOdsAtfx, expParams, True, "D:\Data\ExampleTest_new.atfx")
  ExportToFileAsync("D:\Data\Example.svd", PTCExportType.ptcExportTypeUniversalFile, expParams, True, "D:\Data\ExampleTest.unv")
  ExportToFileAsync("D:\Data\Example.svd", PTCExportType.ptcExportTypeMEScope, expParams, True, "D:\Data\ExampleTest.str")
  ExportToFile("D:\Data\Example.svd", PTCExportType.ptcExportTypeAsamOdsAtfx, expParams, True, "D:\Data\ExampleTest.atfx")

  Dim signalsToExport As New List(Of String)
  signalsToExport.Add("FFT \ Vib \ Displacement")
  signalsToExport.Add("FFT \ Vib & Ref1 \ H1 Displacement / Voltage")

  expParams.BandSignals = signalsToExport.ToArray()
  expParams.PointSignals = signalsToExport.ToArray()

  Dim refIndices As New List(Of Integer)
  refIndices.Add(5)

  expParams.ReferencePointIndices = refIndices.ToArray()

  ExportToFile("D:\Data\Example_new.svd", PTCExportType.ptcExportTypeUniversalFile, expParams, False, "D:\Data\ExampleTest_new_select.unv")
  ExportToFile("D:\Data\Example_new.svd", PTCExportType.ptcExportTypeMEScope, expParams, False, "D:\Data\ExampleTest_new_select.str")
  ExportToFileAsync("D:\Data\Example_new.svd", PTCExportType.ptcExportTypeAsamOdsAtfx, expParams, False, "D:\Data\ExampleTest_new_select.atfx")
  ExportToFileAsync("D:\Data\Example.svd", PTCExportType.ptcExportTypeUniversalFile, expParams, False, "D:\Data\ExampleTest_select.unv")
  ExportToFileAsync("D:\Data\Example.svd", PTCExportType.ptcExportTypeMEScope, expParams, False, "D:\Data\ExampleTest_select.str")
  ExportToFile("D:\Data\Example.svd", PTCExportType.ptcExportTypeAsamOdsAtfx, expParams, False, "D:\Data\ExampleTest_select.atfx")

End Sub

Sub ExportToFile(inputFileName As String, exportType As PSV.PTCExportType, expParams As ExportParameters, loadParams As Boolean, outputFileName As String)

  Debug.WriteLine("Export started ...")

  Dim oExp As Exporter = Application.Exporter(inputFileName, exportType)
  g_exporterEvents = oExp

  If loadParams Then
    oExp.LoadParameters(expParams)
  End If
  expParams.FileName = outputFileName
  ShowExportParameters(expParams)
  oExp.Export(expParams)

  Debug.WriteLine("Export completed.")

End Sub

Sub ExportToFileAsync(inputFileName As String, exportType As PSV.PTCExportType, expParams As ExportParameters, loadParams As Boolean, outputFileName As String)

  Dim oExp As Exporter = Application.Exporter(inputFileName, exportType)
  g_exporterEvents = oExp

  If loadParams Then
    oExp.LoadParameters(expParams)
  End If
  expParams.FileName = outputFileName
  ShowExportParameters(expParams)
  oExp.ExportAsync(expParams)

  While Not g_completed
    Wait 1
  End While
  g_completed = False

End Sub

Sub ShowExportParameters(parameters As ExportParameters)
  Debug.WriteLine "ExportParameters: "
  Debug.Print "FileName: "; parameters.FileName.ToString
  Debug.Print "BandSignals: "
  Dim oBandSignals() As String = parameters.BandSignals
  For Each oBandSignal As String In oBandSignals
    Debug.Print oBandSignal.ToString
  Next
  Debug.Print "PointSignals: "
  Dim oPointSignals() As String = parameters.PointSignals
  For Each oPointSignal As String In oPointSignals
    Debug.Print oPointSignal.ToString
  Next
  Debug.Print "DisplayObjects: "; parameters.DisplayObjects.ToString
  Debug.Print "ExportInvalidatedPoints: "; parameters.ExportInvalidatedPoints.ToString
  Debug.Print "ExportOverrangePoints: "; parameters.ExportOverrangePoints.ToString
  Debug.Print "ReferencePointIndices: "
  Dim oReferencePointIndices() As Integer = parameters.ReferencePointIndices
  For Each oReferencePointIndice As Integer In oReferencePointIndices
    Debug.Print oReferencePointIndice.ToString
  Next
End Sub
```


---

## Exporter Object Members

*Quelle: `PSV~Exporter_members.html` · Polytec PSV Type Library*

### Public Methods

| CancelAsync | Cancels an asynchronous operation. The method returns at once. The ongoing operation might or might not be canceled. See the cancelled parameter of the corresponding ExportCompleted event to check whether the operation has been canceled. It is legal (and a no-operation) to call this function when no operation is ongoing, i.e. IsBusy is False. |
|---|---|
| Export | Exports the data. |
| ExportAsync | Exports the data. The method returns at once and starts the calculation on a worker thread. Use the ExportCompleted event to receive the result. Calling this method while IsBusy is True results in an error. |
| LoadParameters | Loads the export parameters that were used for the last export via the user interface of the software (VibSoft, PSV or MPV). |

### Public Properties

| IsBusy | Queries whether the export functionality is busy. It is not allowed to start a new operation while this property is True. |
|---|---|

### Events

| ExportCompleted | The event signaling that the export is finished. |
|---|---|
| IsBusyChanged | The event signaling that the busy status has changed. |
| ProgressChanged | The event signaling that the progress has changed. |


---

## CancelAsync Method

*Quelle: `PSV~Exporter~CancelAsync.html` · Polytec PSV Type Library · Exporter Object : CancelAsync Method*

### Description

Cancels an asynchronous operation. The method returns at once. The ongoing operation might or might not be canceled. See the cancelled parameter of the corresponding ExportCompleted event to check whether the operation has been canceled. It is legal (and a no-operation) to call this function when no operation is ongoing, i.e. IsBusy is False.

### Syntax

*Visual Basic:*
```
Public Sub CancelAsync()
```


---

## Export Method

*Quelle: `PSV~Exporter~Export.html` · Polytec PSV Type Library · Exporter Object : Export Method*

### Description

Exports the data.

### Syntax

*Visual Basic:*
```
Public Sub Export( _
   ByVal parameters As ExportParameters _
)
```

### Parameters

parameters

The export parameters.


---

## ExportAsync Method

*Quelle: `PSV~Exporter~ExportAsync.html` · Polytec PSV Type Library · Exporter Object : ExportAsync Method*

### Description

Exports the data. The method returns at once and starts the calculation on a worker thread. Use the ExportCompleted event to receive the result. Calling this method while IsBusy is True results in an error.

### Syntax

*Visual Basic:*
```
Public Sub ExportAsync( _
   ByVal parameters As ExportParameters _
)
```

### Parameters

parameters

The export parameters.


---

## LoadParameters Method

*Quelle: `PSV~Exporter~LoadParameters.html` · Polytec PSV Type Library · Exporter Object : LoadParameters Method*

### Description

Loads the export parameters that were used for the last export via the user interface of the software (VibSoft, PSV or MPV).

### Syntax

*Visual Basic:*
```
Public Sub LoadParameters( _
   ByRef parameters As ExportParameters _
)
```

### Parameters

parameters

The export parameters.


---

## IsBusy Property

*Quelle: `PSV~Exporter~IsBusy.html` · Polytec PSV Type Library · Exporter Object : IsBusy Property*

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


---

## ExportCompleted Event

*Quelle: `PSV~Exporter~ExportCompleted_EV.html` · Polytec PSV Type Library · Exporter Object : ExportCompleted Event*

### Description

The event signaling that the export is finished.

### Syntax

*Visual Basic:*
```
Public Event ExportCompleted( _
   ByVal cancelled As Boolean, _
   ByVal errorOccurred As Boolean, _
   ByVal errorMessage As String _
)
```

### Parameters

cancelled

True if the export was canceled, False otherwise.

errorOccurred

True if an error occurred during the export, False otherwise.

errorMessage

The error message if an error occurred.


---

## IsBusyChanged Event

*Quelle: `PSV~Exporter~IsBusyChanged_EV.html` · Polytec PSV Type Library · Exporter Object : IsBusyChanged Event*

### Description

The event signaling that the busy status has changed.

### Syntax

*Visual Basic:*
```
Public Event IsBusyChanged( _
   ByVal IsBusyChanged As Boolean _
)
```

### Parameters

IsBusyChanged

True if the export operation is ongoing, False otherwise.


---

## ProgressChanged Event

*Quelle: `PSV~Exporter~ProgressChanged_EV.html` · Polytec PSV Type Library · Exporter Object : ProgressChanged Event*

### Description

The event signaling that the progress has changed.

### Syntax

*Visual Basic:*
```
Public Event ProgressChanged( _
   ByVal progress As Long _
)
```

### Parameters

progress

The progress in percent.
