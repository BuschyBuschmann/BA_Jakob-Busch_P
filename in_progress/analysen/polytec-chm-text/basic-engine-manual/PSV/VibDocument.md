# PSV – VibDocument

## VibDocument Object

*Quelle: `PSV~VibDocument.html` · Polytec PSV Type Library*

### Description

The document object for files containing vibration data. Derived from the Document object.

### Object Model


---

## VibDocument Object Members

*Quelle: `PSV~VibDocument_members.html` · Polytec PSV Type Library*

### Public Methods

| Close | Closes the document and all related windows. |
|---|---|
| NewWindow | Opens a new window for this document and returns the new window. |
| Save | Saves the changes to the document. |
| SaveAs | Saves the document to a new file with the given file name. |

### Public Properties

| AcquisitionMode | The acquisition mode for this document. |
|---|---|
| AcquisitionProperties | The acquisition properties for this document. |
| Exporter | Gets the exporter object. |
| Name | Specifies the name of the document. |
| Type | The type of the document. |
| Windows | The collection of Window objects belonging to this document. |

### Events

| Close | The document has been closed. |
|---|---|


---

## Close Method

*Quelle: `PSV~VibDocument~Close.html` · Polytec PSV Type Library · VibDocument Object : Close Method*

### Description

Closes the document and all related windows.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## NewWindow Method

*Quelle: `PSV~VibDocument~NewWindow.html` · Polytec PSV Type Library · VibDocument Object : NewWindow Method*

### Description

Opens a new window for this document and returns the new window.

### Syntax

*Visual Basic:*
```
Public Function NewWindow() As Window
```


---

## Save Method

*Quelle: `PSV~VibDocument~Save.html` · Polytec PSV Type Library · VibDocument Object : Save Method*

### Description

Saves the changes to the document.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## SaveAs Method

*Quelle: `PSV~VibDocument~SaveAs.html` · Polytec PSV Type Library · VibDocument Object : SaveAs Method*

### Description

Saves the document to a new file with the given file name.

### Syntax

*Visual Basic:*
```
Public Sub SaveAs( _
   ByVal bstrFileName As String _
)
```

### Parameters

bstrFileName

The file name.


---

## AcquisitionMode Property

*Quelle: `PSV~VibDocument~AcquisitionMode.html` · Polytec PSV Type Library · VibDocument Object : AcquisitionMode Property*

### Description

The acquisition mode for this document.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AcquisitionMode As PTCAcqMode
```


---

## AcquisitionProperties Property

*Quelle: `PSV~VibDocument~AcquisitionProperties.html` · Polytec PSV Type Library · VibDocument Object : AcquisitionProperties Property*

### Description

The acquisition properties for this document.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AcquisitionProperties As IAcquisitionProperties3
```


---

## Exporter Property

*Quelle: `PSV~VibDocument~Exporter.html` · Polytec PSV Type Library · VibDocument Object : Exporter Property*

### Description

Gets the exporter object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exporter( _
   ByVal exportType As PTCExportType _
) As IExporter
```

### Parameters

exportType

| Value | Description |
|---|---|
| ptcExportTypeAsamOdsAtfx | ASAM ODS ATFX export file type |
| ptcExportTypeMEScope | ME'scope export file type |
| ptcExportTypeUniversalFile | Universal File (UFF) export file type |
The type of the export file.

### Return Type

The exporter object.


---

## Name Property

*Quelle: `PSV~VibDocument~Name.html` · Polytec PSV Type Library · VibDocument Object : Name Property*

### Description

Specifies the name of the document.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `PSV~VibDocument~Type.html` · Polytec PSV Type Library · VibDocument Object : Type Property*

### Description

The type of the document.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCDocumentType
```


---

## Windows Property

*Quelle: `PSV~VibDocument~Windows.html` · Polytec PSV Type Library · VibDocument Object : Windows Property*

### Description

The collection of Window objects belonging to this document.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Windows As Windows
```


---

## Close Event

*Quelle: `PSV~VibDocument~Close_EV.html` · Polytec PSV Type Library · VibDocument Object : Close Event*

### Description

The document has been closed.

### Syntax

*Visual Basic:*
```
Public Event Close()
```
