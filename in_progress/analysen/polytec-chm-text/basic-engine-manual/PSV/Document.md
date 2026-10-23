# PSV – Document

## Document Object

*Quelle: `PSV~Document.html` · Polytec PSV Type Library*

### Description

The document class is the base object of documents of different types: VibDocument for files containing vibration data and SigProDocument for the signal processor documents.

### Object Model

### Remarks

You can use the Type property to find out the type of the document. You can then cast to the document of the more specific object type.


---

## Document Object Members

*Quelle: `PSV~Document_members.html` · Polytec PSV Type Library*

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

*Quelle: `PSV~Document~Close.html` · Polytec PSV Type Library · Document Object : Close Method*

### Description

Closes the document and all related windows.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## NewWindow Method

*Quelle: `PSV~Document~NewWindow.html` · Polytec PSV Type Library · Document Object : NewWindow Method*

### Description

Opens a new window for this document and returns the new window.

### Syntax

*Visual Basic:*
```
Public Function NewWindow() As Window
```


---

## Save Method

*Quelle: `PSV~Document~Save.html` · Polytec PSV Type Library · Document Object : Save Method*

### Description

Saves the changes to the document.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## SaveAs Method

*Quelle: `PSV~Document~SaveAs.html` · Polytec PSV Type Library · Document Object : SaveAs Method*

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

*Quelle: `PSV~Document~Name.html` · Polytec PSV Type Library · Document Object : Name Property*

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

*Quelle: `PSV~Document~Type.html` · Polytec PSV Type Library · Document Object : Type Property*

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

*Quelle: `PSV~Document~Windows.html` · Polytec PSV Type Library · Document Object : Windows Property*

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

*Quelle: `PSV~Document~Close_EV.html` · Polytec PSV Type Library · Document Object : Close Event*

### Description

The document has been closed.

### Syntax

*Visual Basic:*
```
Public Event Close()
```
