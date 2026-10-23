# PSV – Window

## Window Object

*Quelle: `PSV~Window.html` · Polytec PSV Type Library*

### Description

Item of the Windows collection. The window object is the base object of windows of different types: AnalyzerWindow for documents containing single point vibration data, AreaWindow for documents containing scans of vibration data and SigProWindow for the signal processor documents.

### Object Model

### Remarks

You can use the Type property to find out the type of the window. You can then cast to the window object of the more specific object type.


---

## Window Object Members

*Quelle: `PSV~Window_members.html` · Polytec PSV Type Library*

### Public Methods

| Activate | Activates the window and brings it to the front. |
|---|---|
| Close | Closes the window. |

### Public Properties

| Active | True, if the window is active. |
|---|---|
| Caption | The title of the window. |
| Settings | Specifies the settings of the window. |
| Type | The type of the window. |


---

## Activate Method

*Quelle: `PSV~Window~Activate.html` · Polytec PSV Type Library · Window Object : Activate Method*

### Description

Activates the window and brings it to the front.

### Syntax

*Visual Basic:*
```
Public Sub Activate()
```


---

## Close Method

*Quelle: `PSV~Window~Close.html` · Polytec PSV Type Library · Window Object : Close Method*

### Description

Closes the window.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## Active Property

*Quelle: `PSV~Window~Active.html` · Polytec PSV Type Library · Window Object : Active Property*

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

## Caption Property

*Quelle: `PSV~Window~Caption.html` · Polytec PSV Type Library · Window Object : Caption Property*

### Description

The title of the window.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caption As String
```


---

## Settings Property

*Quelle: `PSV~Window~Settings.html` · Polytec PSV Type Library · Window Object : Settings Property*

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

*Quelle: `PSV~Window~Type.html` · Polytec PSV Type Library · Window Object : Type Property*

### Description

The type of the window.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCWindowType
```
