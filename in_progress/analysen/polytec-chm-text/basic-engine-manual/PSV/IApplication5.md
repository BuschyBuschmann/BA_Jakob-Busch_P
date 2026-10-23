# PSV – IApplication5

## IApplication5 Interface

*Quelle: `PSV~IApplication5.html` · Polytec PSV Type Library*

### Description

The object representing the application (PSV or VibSoft).

### Object Model

### Remarks

It is recommended to cast to the Application Object.


---

## IApplication5 Interface Members

*Quelle: `PSV~IApplication5_members.html` · Polytec PSV Type Library*

### Public Methods

| Activate | Activates the application. The application window comes to the front. |
|---|---|
| NewWindow | Opens a new window for the active document and returns it. |
| PrintOut | Prints the active window. |
| Quit | Terminates the application. |

### Public Properties

| Acquisition | The Acquisition object that represents the data acquisition of PSV and VibSoft. |
|---|---|
| ActiveDocument | The active document. |
| ActiveWindow | The active window. |
| Application | The Application object . |
| DigitalPorts | The collection of DigitalPorts representing all digital i/o ports of the front end. |
| Documents | The collection of all open documents. |
| Height | Specifies the height of the application window, in pixel. |
| Left | Specifies the position of the left border of the application window, in pixel. |
| MessagesLoggingEnabled | Specifies whether the logging of messages to the windows event log is enabled. |
| Mode | Specifies the application mode. |
| Name | The name of the application. |
| Settings | The settings object that represents the current application settings (A/D Settings, scan point definition, camera and alignment, and window layout). |
| SuppressMessagesForAutomation | Specifies if messages are suppressed during automation. |
| Top | Specifies the position of the top border of the application window, in pixel. |
| Version | The version number of the application. |
| Visible | Specifies whether the application window is visible. |
| WarningLevel | Specifies the warning level for the application. |
| Width | Specifies the width of the application window, in pixel. |
| Windows | The collection of all open document windows. |
| WindowState | Specifies the status of the application window. |


---

## Activate Method

*Quelle: `PSV~IApplication5~Activate.html` · Polytec PSV Type Library · IApplication5 Interface : Activate Method*

### Description

Activates the application. The application window comes to the front.

### Syntax

*Visual Basic:*
```
Public Sub Activate()
```


---

## NewWindow Method

*Quelle: `PSV~IApplication5~NewWindow.html` · Polytec PSV Type Library · IApplication5 Interface : NewWindow Method*

### Description

Opens a new window for the active document and returns it.

### Syntax

*Visual Basic:*
```
Public Function NewWindow() As Window
```


---

## PrintOut Method

*Quelle: `PSV~IApplication5~PrintOut.html` · Polytec PSV Type Library · IApplication5 Interface : PrintOut Method*

### Description

Prints the active window.

### Syntax

*Visual Basic:*
```
Public Sub PrintOut()
```


---

## Quit Method

*Quelle: `PSV~IApplication5~Quit.html` · Polytec PSV Type Library · IApplication5 Interface : Quit Method*

### Description

Terminates the application.

### Syntax

*Visual Basic:*
```
Public Sub Quit()
```


---

## Acquisition Property

*Quelle: `PSV~IApplication5~Acquisition.html` · Polytec PSV Type Library · IApplication5 Interface : Acquisition Property*

### Description

The Acquisition object that represents the data acquisition of PSV and VibSoft.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Acquisition As IAcquisition6
```

### Example


---

## ActiveDocument Property

*Quelle: `PSV~IApplication5~ActiveDocument.html` · Polytec PSV Type Library · IApplication5 Interface : ActiveDocument Property*

### Description

The active document.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ActiveDocument As Document
```

### Remarks

If there are no documents open, an error occurs.


---

## ActiveWindow Property

*Quelle: `PSV~IApplication5~ActiveWindow.html` · Polytec PSV Type Library · IApplication5 Interface : ActiveWindow Property*

### Description

The active window.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ActiveWindow As Window
```

### Remarks

If there are no windows open an error occurs.


---

## Application Property

*Quelle: `PSV~IApplication5~Application.html` · Polytec PSV Type Library · IApplication5 Interface : Application Property*

### Description

The Application object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Application As IApplication5
```


---

## DigitalPorts Property

*Quelle: `PSV~IApplication5~DigitalPorts.html` · Polytec PSV Type Library · IApplication5 Interface : DigitalPorts Property*

### Description

The collection of DigitalPorts representing all digital i/o ports of the front end.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DigitalPorts As DigitalPorts
```


---

## Documents Property

*Quelle: `PSV~IApplication5~Documents.html` · Polytec PSV Type Library · IApplication5 Interface : Documents Property*

### Description

The collection of all open documents.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Documents As Documents
```

### Remarks

The acquisition document is not part of this collection.


---

## Height Property

*Quelle: `PSV~IApplication5~Height.html` · Polytec PSV Type Library · IApplication5 Interface : Height Property*

### Description

Specifies the height of the application window, in pixel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Height As Long
```


---

## Left Property

*Quelle: `PSV~IApplication5~Left.html` · Polytec PSV Type Library · IApplication5 Interface : Left Property*

### Description

Specifies the position of the left border of the application window, in pixel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Left As Long
```


---

## MessagesLoggingEnabled Property

*Quelle: `PSV~IApplication5~MessagesLoggingEnabled.html` · Polytec PSV Type Library · IApplication5 Interface : MessagesLoggingEnabled Property*

### Description

Specifies whether the logging of messages to the windows event log is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MessagesLoggingEnabled As Boolean
```


---

## Mode Property

*Quelle: `PSV~IApplication5~Mode.html` · Polytec PSV Type Library · IApplication5 Interface : Mode Property*

### Description

Specifies the application mode.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Mode As PTCApplicationMode
```

### Remarks

This property is relevant for PSV only.


---

## Name Property

*Quelle: `PSV~IApplication5~Name.html` · Polytec PSV Type Library · IApplication5 Interface : Name Property*

### Description

The name of the application.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Settings Property

*Quelle: `PSV~IApplication5~Settings.html` · Polytec PSV Type Library · IApplication5 Interface : Settings Property*

### Description

The settings object that represents the current application settings (A/D Settings, scan point definition, camera and alignment, and window layout).

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Settings As Settings
```

### Example


---

## SuppressMessagesForAutomation Property

*Quelle: `PSV~IApplication5~SuppressMessagesForAutomation.html` · Polytec PSV Type Library · IApplication5 Interface : SuppressMessagesForAutomation Property*

### Description

Specifies if messages are suppressed during automation.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SuppressMessagesForAutomation As Boolean
```

### Remarks

The property is set true as default. You can set the property to false during development of a macro to receive all informational and error messages.


---

## Top Property

*Quelle: `PSV~IApplication5~Top.html` · Polytec PSV Type Library · IApplication5 Interface : Top Property*

### Description

Specifies the position of the top border of the application window, in pixel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Top As Long
```


---

## Version Property

*Quelle: `PSV~IApplication5~Version.html` · Polytec PSV Type Library · IApplication5 Interface : Version Property*

### Description

The version number of the application.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Version As String
```


---

## Visible Property

*Quelle: `PSV~IApplication5~Visible.html` · Polytec PSV Type Library · IApplication5 Interface : Visible Property*

### Description

Specifies whether the application window is visible.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Visible As Boolean
```


---

## WarningLevel Property

*Quelle: `PSV~IApplication5~WarningLevel.html` · Polytec PSV Type Library · IApplication5 Interface : WarningLevel Property*

### Description

Specifies the warning level for the application.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property WarningLevel As PTCWarningLevel
```


---

## Width Property

*Quelle: `PSV~IApplication5~Width.html` · Polytec PSV Type Library · IApplication5 Interface : Width Property*

### Description

Specifies the width of the application window, in pixel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Width As Long
```


---

## Windows Property

*Quelle: `PSV~IApplication5~Windows.html` · Polytec PSV Type Library · IApplication5 Interface : Windows Property*

### Description

The collection of all open document windows.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Windows As Windows
```

### Remarks

The analyzer windows of the acquisition document are included in this list.


---

## WindowState Property

*Quelle: `PSV~IApplication5~WindowState.html` · Polytec PSV Type Library · IApplication5 Interface : WindowState Property*

### Description

Specifies the status of the application window.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property WindowState As PTCWindowState
```
