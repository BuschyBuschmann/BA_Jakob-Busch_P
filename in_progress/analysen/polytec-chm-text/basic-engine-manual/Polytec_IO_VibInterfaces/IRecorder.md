# Polytec_IO_VibInterfaces – IRecorder

## IRecorder Interface

*Quelle: `Polytec_IO_VibInterfaces~IRecorder.html` · Polytec IO VibInterfaces Type Library*

### Description

The recorder mode, e.g. of a VGO-200.


---

## IRecorder Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IRecorder_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| DeleteRecordings | Deletes the recordings with the specified file IDs. |
|---|---|
| GetRecorderProjectNames | Gets the recorder project names from the device. |
| SetRecorderProjectNames | Sets the list of recorder project names to the device. |

### Public Properties

| Name | The name of the recorder. |
|---|---|


---

## DeleteRecordings Method

*Quelle: `Polytec_IO_VibInterfaces~IRecorder~DeleteRecordings.html` · Polytec IO VibInterfaces Type Library · IRecorder Interface : DeleteRecordings Method*

### Description

Deletes the recordings with the specified file IDs.

### Syntax

*Visual Basic:*
```
Public Sub DeleteRecordings( _
   ByVal fileIDs() As Long _
)
```

### Parameters

fileIDs

The file IDs.


---

## GetRecorderProjectNames Method

*Quelle: `Polytec_IO_VibInterfaces~IRecorder~GetRecorderProjectNames.html` · Polytec IO VibInterfaces Type Library · IRecorder Interface : GetRecorderProjectNames Method*

### Description

Gets the recorder project names from the device.

### Syntax

*Visual Basic:*
```
Public Function GetRecorderProjectNames() As String()
```

### Return Type

The list of project names or an empty list.


---

## SetRecorderProjectNames Method

*Quelle: `Polytec_IO_VibInterfaces~IRecorder~SetRecorderProjectNames.html` · Polytec IO VibInterfaces Type Library · IRecorder Interface : SetRecorderProjectNames Method*

### Description

Sets the list of recorder project names to the device.

### Syntax

*Visual Basic:*
```
Public Sub SetRecorderProjectNames( _
   ByVal projectNames() As String _
)
```

### Parameters

projectNames

The list of project names or an empty list.


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~IRecorder~Name.html` · Polytec IO VibInterfaces Type Library · IRecorder Interface : Name Property*

### Description

The name of the recorder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```
