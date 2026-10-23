# PSV – AreaWindow

## AreaWindow Object

*Quelle: `PSV~AreaWindow.html` · Polytec PSV Type Library*

### Description

The window object for documents with vibration data of scans. Derived from the Window object.

### Object Model

### Example

The example demonstrates how to export animations and analyzer graphics for the active area window in the application.

- Example (Visual Basic)

```
'#Language "WWB.NET"

Sub Main
    Dim fileNameAreaPNG As String = "D:\Temp\Area.png"
    Dim fileNameAreaMP4 As String = "D:\Temp\Area.mp4"
    Dim fileNameAreaWMV As String = "D:\Temp\Area.wmv"
    Dim fileNameAnalyzerJPG As String = "D:\Temp\Analyzer.jpg"

    Dim oWnd As Window = Application.ActiveWindow
    If (Not IsNothing(oWnd) And oWnd.Type = PTCWindowType.ptcWindowTypeArea) Then
        Dim oAreaWindow As AreaWindow = oWnd
        oAreaWindow.AreaView.Export(fileNameAreaPNG, PTCFileFormat.ptcFileFormatGraphic)
        oAreaWindow.ExportAnimation(fileNameAreaMP4, PTCViewSelection.ptcViewSelectionUpper)
        oAreaWindow.ExportAnimation(fileNameAreaWMV, PTCViewSelection.ptcViewSelectionBoth)

        Dim oAnalyzerView As AnalyzerView = oAreaWindow.AnalyzerView
        If (Not IsNothing(oAnalyzerView)) Then
            oAnalyzerView.Export(fileNameAnalyzerJPG, PTCFileFormat.ptcFileFormatGraphic)
        End If
    End If
End Sub
```


---

## AreaWindow Object Members

*Quelle: `PSV~AreaWindow_members.html` · Polytec PSV Type Library*

### Public Methods

| Activate | Activates the window and brings it to the front. |
|---|---|
| Close | Closes the window. |
| ExportAnimation | Exports the animation from the requested view(s) into a file. |
| PrintOut | Prints the window. |

### Public Properties

| Active | True, if the window is active. |
|---|---|
| AnalyzerView | The analyzer view pane of the window. |
| AreaView | The area view pane of the window. |
| Caption | The window title. |
| Document | The window's document object. |
| Settings | Specifies the settings of the window. |
| Type | The type of the window. |


---

## Activate Method

*Quelle: `PSV~AreaWindow~Activate.html` · Polytec PSV Type Library · AreaWindow Object : Activate Method*

### Description

Activates the window and brings it to the front.

### Syntax

*Visual Basic:*
```
Public Sub Activate()
```


---

## Close Method

*Quelle: `PSV~AreaWindow~Close.html` · Polytec PSV Type Library · AreaWindow Object : Close Method*

### Description

Closes the window.

### Syntax

*Visual Basic:*
```
Public Sub Close()
```


---

## ExportAnimation Method

*Quelle: `PSV~AreaWindow~ExportAnimation.html` · Polytec PSV Type Library · AreaWindow Object : ExportAnimation Method*

### Description

Exports the animation from the requested view(s) into a file.

### Syntax

*Visual Basic:*
```
Public Sub ExportAnimation( _
   ByVal outputFileName As String, _
   ByVal viewSelection As PTCViewSelection _
)
```

### Parameters

outputFileName

The file name of the export file. The extensions .avi and .gif are supported.

viewSelection

| Value | Description |
|---|---|
| ptcViewSelectionBoth | Both the upper and the lower view are selected. |
| ptcViewSelectionLower | The lower view is selected. |
| ptcViewSelectionUpper | The upper view is selected. |
The view(s) to select.

### Example

For an example see AreaWindow Object.


---

## PrintOut Method

*Quelle: `PSV~AreaWindow~PrintOut.html` · Polytec PSV Type Library · AreaWindow Object : PrintOut Method*

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

*Quelle: `PSV~AreaWindow~Active.html` · Polytec PSV Type Library · AreaWindow Object : Active Property*

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

*Quelle: `PSV~AreaWindow~AnalyzerView.html` · Polytec PSV Type Library · AreaWindow Object : AnalyzerView Property*

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

*Quelle: `PSV~AreaWindow~AreaView.html` · Polytec PSV Type Library · AreaWindow Object : AreaView Property*

### Description

The area view pane of the window.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AreaView As AreaView
```


---

## Caption Property

*Quelle: `PSV~AreaWindow~Caption.html` · Polytec PSV Type Library · AreaWindow Object : Caption Property*

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

*Quelle: `PSV~AreaWindow~Document.html` · Polytec PSV Type Library · AreaWindow Object : Document Property*

### Description

The window's document object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Document As VibDocument
```


---

## Settings Property

*Quelle: `PSV~AreaWindow~Settings.html` · Polytec PSV Type Library · AreaWindow Object : Settings Property*

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

*Quelle: `PSV~AreaWindow~Type.html` · Polytec PSV Type Library · AreaWindow Object : Type Property*

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

Always ptcWindowTypeArea.
