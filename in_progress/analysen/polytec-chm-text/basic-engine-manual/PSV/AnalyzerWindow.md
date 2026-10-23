# PSV – AnalyzerWindow

## AnalyzerWindow Object

*Quelle: `PSV~AnalyzerWindow.html` · Polytec PSV Type Library*

### Description

The window for single point vibration data documents. Derived from the Window object.

### Object Model


---

## AnalyzerWindow Object Members

*Quelle: `PSV~AnalyzerWindow_members.html` · Polytec PSV Type Library*

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

*Quelle: `PSV~AnalyzerWindow~Activate.html` · Polytec PSV Type Library · AnalyzerWindow Object : Activate Method*

### Description

Activates the window and brings it to the front.

### Syntax

*Visual Basic:*
```
Public Sub Activate()
```


---

## Close Method

*Quelle: `PSV~AnalyzerWindow~Close.html` · Polytec PSV Type Library · AnalyzerWindow Object : Close Method*

### Description

Closes the window.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## PrintOut Method

*Quelle: `PSV~AnalyzerWindow~PrintOut.html` · Polytec PSV Type Library · AnalyzerWindow Object : PrintOut Method*

### Description

Prints the window.

### Syntax

*Visual Basic:*
```
Public Sub PrintOut()
```


---

## Active Property

*Quelle: `PSV~AnalyzerWindow~Active.html` · Polytec PSV Type Library · AnalyzerWindow Object : Active Property*

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

*Quelle: `PSV~AnalyzerWindow~AnalyzerView.html` · Polytec PSV Type Library · AnalyzerWindow Object : AnalyzerView Property*

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

## Caption Property

*Quelle: `PSV~AnalyzerWindow~Caption.html` · Polytec PSV Type Library · AnalyzerWindow Object : Caption Property*

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

*Quelle: `PSV~AnalyzerWindow~Document.html` · Polytec PSV Type Library · AnalyzerWindow Object : Document Property*

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

*Quelle: `PSV~AnalyzerWindow~Settings.html` · Polytec PSV Type Library · AnalyzerWindow Object : Settings Property*

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

*Quelle: `PSV~AnalyzerWindow~Type.html` · Polytec PSV Type Library · AnalyzerWindow Object : Type Property*

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
