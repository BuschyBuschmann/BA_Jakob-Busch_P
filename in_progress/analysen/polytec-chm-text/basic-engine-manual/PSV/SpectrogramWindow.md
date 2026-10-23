# PSV – SpectrogramWindow

## SpectrogramWindow Object

*Quelle: `PSV~SpectrogramWindow.html` · Polytec PSV Type Library*

### Description

The window object for documents with spectrograms or Campbell diagrams. Derived from the Window object.

### Object Model


---

## SpectrogramWindow Object Members

*Quelle: `PSV~SpectrogramWindow_members.html` · Polytec PSV Type Library*

### Public Methods

| Activate | Activates the window and brings it to the front. |
|---|---|
| Close | Closes the window. |
| PrintOut | Prints the window. |

### Public Properties

| Active | True, if the window is active. |
|---|---|
| AnalyzerView | The analyzer view pane of the window. |
| AreaView | The are view pane of the window. |
| Caption | The window title. |
| Document | The windows Document object. |
| Settings | Specifies the settings of the window. |
| Type | The type of the window. |


---

## Activate Method

*Quelle: `PSV~SpectrogramWindow~Activate.html` · Polytec PSV Type Library · SpectrogramWindow Object : Activate Method*

### Description

Activates the window and brings it to the front.

### Syntax

*Visual Basic:*
```
Public Sub Activate()
```


---

## Close Method

*Quelle: `PSV~SpectrogramWindow~Close.html` · Polytec PSV Type Library · SpectrogramWindow Object : Close Method*

### Description

Closes the window.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## PrintOut Method

*Quelle: `PSV~SpectrogramWindow~PrintOut.html` · Polytec PSV Type Library · SpectrogramWindow Object : PrintOut Method*

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


---

## Active Property

*Quelle: `PSV~SpectrogramWindow~Active.html` · Polytec PSV Type Library · SpectrogramWindow Object : Active Property*

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

*Quelle: `PSV~SpectrogramWindow~AnalyzerView.html` · Polytec PSV Type Library · SpectrogramWindow Object : AnalyzerView Property*

### Description

The analyzer view pane of the window.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AnalyzerView As AnalyzerView
```


---

## AreaView Property

*Quelle: `PSV~SpectrogramWindow~AreaView.html` · Polytec PSV Type Library · SpectrogramWindow Object : AreaView Property*

### Description

The are view pane of the window.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AreaView As SpectrogramAreaView
```


---

## Caption Property

*Quelle: `PSV~SpectrogramWindow~Caption.html` · Polytec PSV Type Library · SpectrogramWindow Object : Caption Property*

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

*Quelle: `PSV~SpectrogramWindow~Document.html` · Polytec PSV Type Library · SpectrogramWindow Object : Document Property*

### Description

The windows Document object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Document As VibDocument
```


---

## Settings Property

*Quelle: `PSV~SpectrogramWindow~Settings.html` · Polytec PSV Type Library · SpectrogramWindow Object : Settings Property*

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

*Quelle: `PSV~SpectrogramWindow~Type.html` · Polytec PSV Type Library · SpectrogramWindow Object : Type Property*

### Description

The type of the window.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCWindowType
```

### Remarks

Always ptcWindowTypeAnalyzer.
