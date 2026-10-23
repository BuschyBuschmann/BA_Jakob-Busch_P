# PSV – SigProWindow

## SigProWindow Object

*Quelle: `PSV~SigProWindow.html` · Polytec PSV Type Library*

### Description

The window object for signal processor documents. Derived from the Window object.

### Object Model


---

## SigProWindow Object Members

*Quelle: `PSV~SigProWindow_members.html` · Polytec PSV Type Library*

### Public Methods

| Activate | Activates the window and brings it to the front. |
|---|---|
| Close | Closes the window. |
| PrintOut | Prints the window. |

### Public Properties

| Active | True, if the window is active. |
|---|---|
| AnalyzerView | The analyzer view pane of the window. |
| Caption | The window title. |
| Document | The windows Document object. |
| Settings | Specifies the settings of the window. |
| Type | The type of the window. |


---

## Activate Method

*Quelle: `PSV~SigProWindow~Activate.html` · Polytec PSV Type Library · SigProWindow Object : Activate Method*

### Description

Activates the window and brings it to the front.

### Syntax

*Visual Basic:*
```
Public Sub Activate()
```


---

## Close Method

*Quelle: `PSV~SigProWindow~Close.html` · Polytec PSV Type Library · SigProWindow Object : Close Method*

### Description

Closes the window.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## PrintOut Method

*Quelle: `PSV~SigProWindow~PrintOut.html` · Polytec PSV Type Library · SigProWindow Object : PrintOut Method*

### Description

Prints the window.

### Syntax

*Visual Basic:*
```
Public Sub PrintOut( _
   ByVal PTCPrintOptions As PTCPrintOptions _
)
```

### Parameters

PTCPrintOptions

| Value | Description |
|---|---|
| ptcPrintLower | Print the lower pane of the window. |
| ptcPrintNoUserPrompt | Do not prompt the user. |
| ptcPrintUpper | Print the upper pane of the window. |
The printing options.


---

## Active Property

*Quelle: `PSV~SigProWindow~Active.html` · Polytec PSV Type Library · SigProWindow Object : Active Property*

### Description

True, if the window is active.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Active As Boolean
```


---

## AnalyzerView Property

*Quelle: `PSV~SigProWindow~AnalyzerView.html` · Polytec PSV Type Library · SigProWindow Object : AnalyzerView Property*

### Description

The analyzer view pane of the window.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AnalyzerView As SigProAnalyzerView
```


---

## Caption Property

*Quelle: `PSV~SigProWindow~Caption.html` · Polytec PSV Type Library · SigProWindow Object : Caption Property*

### Description

The window title.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caption As String
```


---

## Document Property

*Quelle: `PSV~SigProWindow~Document.html` · Polytec PSV Type Library · SigProWindow Object : Document Property*

### Description

The windows Document object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Document As SigProDocument
```


---

## Settings Property

*Quelle: `PSV~SigProWindow~Settings.html` · Polytec PSV Type Library · SigProWindow Object : Settings Property*

### Description

Specifies the settings of the window.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Settings As IWindowSettings
```


---

## Type Property

*Quelle: `PSV~SigProWindow~Type.html` · Polytec PSV Type Library · SigProWindow Object : Type Property*

### Description

The type of the window.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCWindowType
```

### Return Type

Always ptcWindowTypeSigPro.
