# PSV – Application

## Application Object

*Quelle: `PSV~Application.html` · Polytec PSV Type Library*

### Description

The object representing the application (PSV or VibSoft).

### Object Model

### Remarks

This class can be instantiated using the string "PSV.Application" and "VibSoft.Application", respectively.


---

## Application Object Members

*Quelle: `PSV~Application_members.html` · Polytec PSV Type Library*

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
| Exporter | Gets the exporter object. |
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

### Events

| MessageOccurred | This event is raised, when normally a message would be displayed to the user. If the SuppressMessagesForAutomation Property is set to true while a macro controls the application, no message boxes are shown but this event is raised. By setting the output parameter pVal you can simulate the corresponding answer of the user to the message box. |
|---|---|
| Quit | The application has been terminated. |
| QuitEx | The application is going to be terminated. |


---

## Activate Method

*Quelle: `PSV~Application~Activate.html` · Polytec PSV Type Library · Application Object : Activate Method*

### Description

Activates the application. The application window comes to the front.

### Syntax

*Visual Basic:*
```
Public Sub Activate()
```


---

## NewWindow Method

*Quelle: `PSV~Application~NewWindow.html` · Polytec PSV Type Library · Application Object : NewWindow Method*

### Description

Opens a new window for the active document and returns it.

### Syntax

*Visual Basic:*
```
Public Function NewWindow() As Window
```


---

## PrintOut Method

*Quelle: `PSV~Application~PrintOut.html` · Polytec PSV Type Library · Application Object : PrintOut Method*

### Description

Prints the active window.

### Syntax

*Visual Basic:*
```
Public Sub PrintOut()
```


---

## Quit Method

*Quelle: `PSV~Application~Quit.html` · Polytec PSV Type Library · Application Object : Quit Method*

### Description

Terminates the application.

### Syntax

*Visual Basic:*
```
Public Sub Quit()
```


---

## Acquisition Property

*Quelle: `PSV~Application~Acquisition.html` · Polytec PSV Type Library · Application Object : Acquisition Property*

### Description

The Acquisition object that represents the data acquisition of PSV and VibSoft.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Acquisition As Acquisition
```

### Example


---

## ActiveDocument Property

*Quelle: `PSV~Application~ActiveDocument.html` · Polytec PSV Type Library · Application Object : ActiveDocument Property*

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

*Quelle: `PSV~Application~ActiveWindow.html` · Polytec PSV Type Library · Application Object : ActiveWindow Property*

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

*Quelle: `PSV~Application~Application.html` · Polytec PSV Type Library · Application Object : Application Property*

### Description

The Application object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Application As Application
```


---

## DigitalPorts Property

*Quelle: `PSV~Application~DigitalPorts.html` · Polytec PSV Type Library · Application Object : DigitalPorts Property*

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

*Quelle: `PSV~Application~Documents.html` · Polytec PSV Type Library · Application Object : Documents Property*

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

## Exporter Property

*Quelle: `PSV~Application~Exporter.html` · Polytec PSV Type Library · Application Object : Exporter Property*

### Description

Gets the exporter object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exporter( _
   ByVal inputFileName As String, _
   ByVal exportType As PTCExportType _
) As Exporter
```

### Parameters

inputFileName

The file name of the file to export data from. The file can be a .pvd, .svd, .mvd or .set file.

exportType

| Value | Description |
|---|---|
| ptcExportTypeAsamOdsAtfx | ASAM ODS ATFX export file type |
| ptcExportTypeMEScope | ME'scope export file type |
| ptcExportTypeUniversalFile | Universal File (UFF) export file type |
The type of the export file.

### Return Type

The exporter object.

### Remarks

The exported object can be used to export geometry and measurement data from the specified file to one of the specified file formats.


---

## Height Property

*Quelle: `PSV~Application~Height.html` · Polytec PSV Type Library · Application Object : Height Property*

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

*Quelle: `PSV~Application~Left.html` · Polytec PSV Type Library · Application Object : Left Property*

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

*Quelle: `PSV~Application~MessagesLoggingEnabled.html` · Polytec PSV Type Library · Application Object : MessagesLoggingEnabled Property*

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

*Quelle: `PSV~Application~Mode.html` · Polytec PSV Type Library · Application Object : Mode Property*

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

*Quelle: `PSV~Application~Name.html` · Polytec PSV Type Library · Application Object : Name Property*

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

*Quelle: `PSV~Application~Settings.html` · Polytec PSV Type Library · Application Object : Settings Property*

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

*Quelle: `PSV~Application~SuppressMessagesForAutomation.html` · Polytec PSV Type Library · Application Object : SuppressMessagesForAutomation Property*

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

*Quelle: `PSV~Application~Top.html` · Polytec PSV Type Library · Application Object : Top Property*

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

*Quelle: `PSV~Application~Version.html` · Polytec PSV Type Library · Application Object : Version Property*

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

*Quelle: `PSV~Application~Visible.html` · Polytec PSV Type Library · Application Object : Visible Property*

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

*Quelle: `PSV~Application~WarningLevel.html` · Polytec PSV Type Library · Application Object : WarningLevel Property*

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

*Quelle: `PSV~Application~Width.html` · Polytec PSV Type Library · Application Object : Width Property*

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

*Quelle: `PSV~Application~Windows.html` · Polytec PSV Type Library · Application Object : Windows Property*

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

*Quelle: `PSV~Application~WindowState.html` · Polytec PSV Type Library · Application Object : WindowState Property*

### Description

Specifies the status of the application window.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property WindowState As PTCWindowState
```


---

## MessageOccurred Event

*Quelle: `PSV~Application~MessageOccurred_EV.html` · Polytec PSV Type Library · Application Object : MessageOccurred Event*

### Description

This event is raised, when normally a message would be displayed to the user. If the SuppressMessagesForAutomation Property is set to true while a macro controls the application, no message boxes are shown but this event is raised. By setting the output parameter pVal you can simulate the corresponding answer of the user to the message box.

### Syntax

*Visual Basic:*
```
Public Event MessageOccurred( _
   ByVal MessageStyle As PTCMessageStyle, _
   ByVal MessageText As String, _
   ByRef pVal As PTCMessageAnswer _
)
```

### Parameters

MessageStyle

| Value | Description |
|---|---|
| ptcMessageStyleABORTRETRYIGNORE | Abort, Retry and Ignore buttons. |
| ptcMessageStyleICONASTERISK | The asterix icon. |
| ptcMessageStyleICONEXCLAMATION | The exclamation mark icon. |
| ptcMessageStyleICONHAND | The hand icon. |
| ptcMessageStyleICONQUESTION | The question mark icon. |
| ptcMessageStyleOK | OK button. |
| ptcMessageStyleOKCANCEL | OK and Cancel button. |
| ptcMessageStyleRETRYCANCEL | Retry and Cancel buttons. |
| ptcMessageStyleYESNO | Yes and No buttons. |
| ptcMessageStyleYESNOCANCEL | Yes, No and Cancel buttons. |
The style of the message box, that would have been shown.

MessageText

The text of the message box, that would have been shown.

pVal

| Value | Description |
|---|---|
| ptcMessageAnswerAbort | Answer as if Abort was clicked. |
| ptcMessageAnswerCancel | Answer as if Cancel was clicked. |
| ptcMessageAnswerIgnore | Answer as if Ignore was clicked. |
| ptcMessageAnswerNo | Answer as if No was clicked. |
| ptcMessageAnswerOk | Answer as if Ok was clicked. |
| ptcMessageAnswerRetry | Answer as if Retry was clicked. |
| ptcMessageAnswerYes | Answer as if Yes was clicked. |
The answer to the message box.


---

## Quit Event

*Quelle: `PSV~Application~Quit_EV.html` · Polytec PSV Type Library · Application Object : Quit Event*

### Description

The application has been terminated.

### Syntax

*Visual Basic:*
```
Public Event Quit()
```


---

## QuitEx Event

*Quelle: `PSV~Application~QuitEx_EV.html` · Polytec PSV Type Library · Application Object : QuitEx Event*

### Description

The application is going to be terminated.

### Syntax

*Visual Basic:*
```
Public Event QuitEx( _
   ByRef stopQuitting As Boolean _
)
```

### Parameters

stopQuitting

By setting the variable to true, you can prevent the termination of the application.
