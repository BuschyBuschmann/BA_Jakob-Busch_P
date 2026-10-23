# PSV – SigProDocument

## SigProDocument Object

*Quelle: `PSV~SigProDocument.html` · Polytec PSV Type Library*

### Description

The document object for signal processor files. Derived from the Document object.

### Object Model


---

## SigProDocument Object Members

*Quelle: `PSV~SigProDocument_members.html` · Polytec PSV Type Library*

### Public Methods

| Close | Closes the document and all related windows. |
|---|---|
| NewWindow | Opens a new window for this document and returns the new window. |
| Save | Saves the changes to the document. |
| SaveAs | Saves the document to a new file with the given file name. |

### Public Properties

| Name | Specifies the name of the document. |
|---|---|
| Type | The type of the document. |
| Windows | The collection of Window objects belonging to this document. |

### Events

| Close | The document has been closed. |
|---|---|


---

## Close Method

*Quelle: `PSV~SigProDocument~Close.html` · Polytec PSV Type Library · SigProDocument Object : Close Method*

### Description

Closes the document and all related windows.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## NewWindow Method

*Quelle: `PSV~SigProDocument~NewWindow.html` · Polytec PSV Type Library · SigProDocument Object : NewWindow Method*

### Description

Opens a new window for this document and returns the new window.

### Syntax

*Visual Basic:*
```
Public Function NewWindow() As Window
```


---

## Save Method

*Quelle: `PSV~SigProDocument~Save.html` · Polytec PSV Type Library · SigProDocument Object : Save Method*

### Description

Saves the changes to the document.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## SaveAs Method

*Quelle: `PSV~SigProDocument~SaveAs.html` · Polytec PSV Type Library · SigProDocument Object : SaveAs Method*

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

## Name Property

*Quelle: `PSV~SigProDocument~Name.html` · Polytec PSV Type Library · SigProDocument Object : Name Property*

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

*Quelle: `PSV~SigProDocument~Type.html` · Polytec PSV Type Library · SigProDocument Object : Type Property*

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

*Quelle: `PSV~SigProDocument~Windows.html` · Polytec PSV Type Library · SigProDocument Object : Windows Property*

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

*Quelle: `PSV~SigProDocument~Close_EV.html` · Polytec PSV Type Library · SigProDocument Object : Close Event*

### Description

The document has been closed.

### Syntax

*Visual Basic:*
```
Public Event Close()
```
