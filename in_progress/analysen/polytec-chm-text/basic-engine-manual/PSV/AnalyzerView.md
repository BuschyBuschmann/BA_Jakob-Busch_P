# PSV – AnalyzerView

## AnalyzerView Object

*Quelle: `PSV~AnalyzerView.html` · Polytec PSV Type Library*

### Description

The object representing the analyzer view pane of the analyzer window or area window.

### Object Model


---

## AnalyzerView Object Members

*Quelle: `PSV~AnalyzerView_members.html` · Polytec PSV Type Library*

### Public Methods

| Autoscale | Auto scales the y-axis depending on the currently displayed data. |
|---|---|
| Export | Saves the view content to a file. |
| GetDataSection | The displayed vibration data. |
| ZoomInX | Zooms the x-axis to the given range. |
| ZoomInY | Zooms the y-axis of the given graph to the given range. |
| ZoomOut | Undoes the last zoom in, or if Full is true, does a full zoom out of both the x- and the y-axis. |

### Public Properties

| AvailableFrames | Returns an array with the frame numbers of the available frames of the displayed vibration data. |
|---|---|
| Cursor | The current data cursor of the view. |
| Display | The current display of the view. |
| Domains | The collection of the domains of the vibration data of this view. |
| Pinned | Specifies whether the settings of the analyzer view are pinned to the settings of other analyzer views. |
| PinSettings | Specifies which settings of the analyzer view should be synchronized with other analyzer views when the Pinned Property of the analyzer views is set to True. |
| Settings | Specifies the settings of the view. |
| Window | The viewss Window object. |
| XAxis | The x-axis of the view. |
| YAxes | The collection of y-axes of the view. |


---

## Autoscale Method

*Quelle: `PSV~AnalyzerView~Autoscale.html` · Polytec PSV Type Library · AnalyzerView Object : Autoscale Method*

### Description

Auto scales the y-axis depending on the currently displayed data.

### Syntax

*Visual Basic:*
```
Public Sub Autoscale()
```


---

## Export Method

*Quelle: `PSV~AnalyzerView~Export.html` · Polytec PSV Type Library · AnalyzerView Object : Export Method*

### Description

Saves the view content to a file.

### Syntax

*Visual Basic:*
```
Public Sub Export( _
   ByVal bstrFileName As String, _
   ByVal PTCFileFormat As PTCFileFormat _
)
```

### Parameters

bstrFileName

The name of the file.

PTCFileFormat

| Value | Description |
|---|---|
| ptcFileFormatAnalyzer | Analyzer file format (.pvd). |
| ptcFileFormatGraphic | Graphic format. |
| ptcFileFormatText | ASCII format. |
The file format.

### Example

For an example see AreaWindow Object.


---

## GetDataSection Method

*Quelle: `PSV~AnalyzerView~GetDataSection.html` · Polytec PSV Type Library · AnalyzerView Object : GetDataSection Method*

### Description

The displayed vibration data.

### Syntax

*Visual Basic:*
```
Public Function GetDataSection( _
   ByVal Graph As Long, _
   ByVal Frame As Long, _
   ByVal FirstIndex As Long, _
   ByVal LastIndex As Long _
) As Single()
```

### Parameters

Graph

The index of the graph (0 or 1).

Frame

The frame number. This has to be one of the
values returned by AvailableFrames.

FirstIndex

0-based index of the first value to get.
This has to be in the range 0 to XAxis.MaxCount - 1.

LastIndex

0-based index of the last value to get.
This has to be in the range 0 to XAxis.MaxCount - 1.

### Return Type

One-dimensional, 0-based array of floats with Last  First + 1 values.


---

## ZoomInX Method

*Quelle: `PSV~AnalyzerView~ZoomInX.html` · Polytec PSV Type Library · AnalyzerView Object : ZoomInX Method*

### Description

Zooms the x-axis to the given range.

### Syntax

*Visual Basic:*
```
Public Sub ZoomInX( _
   ByVal XMin As Double, _
   ByVal XMax As Double _
)
```

### Parameters

XMin

The start of the range.

XMax

The end of the range.


---

## ZoomInY Method

*Quelle: `PSV~AnalyzerView~ZoomInY.html` · Polytec PSV Type Library · AnalyzerView Object : ZoomInY Method*

### Description

Zooms the y-axis of the given graph to the given range.

### Syntax

*Visual Basic:*
```
Public Sub ZoomInY( _
   ByVal Graph As Long, _
   ByVal YMin As Double, _
   ByVal Ymax As Double _
)
```

### Parameters

Graph

The index of the graph (0 or 1).

YMin

The start of the range.

Ymax

The end of the range.


---

## ZoomOut Method

*Quelle: `PSV~AnalyzerView~ZoomOut.html` · Polytec PSV Type Library · AnalyzerView Object : ZoomOut Method*

### Description

Undoes the last zoom in, or if Full is true, does a full zoom out of both the x- and the y-axis.

### Syntax

*Visual Basic:*
```
Public Sub ZoomOut( _
   ByVal bFull As Boolean _
)
```

### Parameters

bFull

If true, performs full zoom out.


---

## AvailableFrames Property

*Quelle: `PSV~AnalyzerView~AvailableFrames.html` · Polytec PSV Type Library · AnalyzerView Object : AvailableFrames Property*

### Description

Returns an array with the frame numbers of the available frames of the displayed vibration data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AvailableFrames As Long()
```

### Return Type

One dimensional, 0-based array of longs.

### Remarks

For multi frame data 0 is the average frame and the frames corresponding to the cycles start at 1. For other vibration data there is only frame 0 available. For user-defined data the frame numbers start at 1.


---

## Cursor Property

*Quelle: `PSV~AnalyzerView~Cursor.html` · Polytec PSV Type Library · AnalyzerView Object : Cursor Property*

### Description

The current data cursor of the view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Cursor As DataCursor
```


---

## Display Property

*Quelle: `PSV~AnalyzerView~Display.html` · Polytec PSV Type Library · AnalyzerView Object : Display Property*

### Description

The current display of the view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Display As IDisplay
```


---

## Domains Property

*Quelle: `PSV~AnalyzerView~Domains.html` · Polytec PSV Type Library · AnalyzerView Object : Domains Property*

### Description

The collection of the domains of the vibration data of this view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Domains As IDomains
```


---

## Pinned Property

*Quelle: `PSV~AnalyzerView~Pinned.html` · Polytec PSV Type Library · AnalyzerView Object : Pinned Property*

### Description

Specifies whether the settings of the analyzer view are pinned to the settings of other analyzer views.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Pinned As Boolean
```

### Remarks

The settings of all analyzer views with this property set to True are synchronized. If you change the settings of one of those analyzer views all other analyzer views will change accordingly. You can use the PinSettings Property to specify which settings should be synchronized.


---

## PinSettings Property

*Quelle: `PSV~AnalyzerView~PinSettings.html` · Polytec PSV Type Library · AnalyzerView Object : PinSettings Property*

### Description

Specifies which settings of the analyzer view should be synchronized with other analyzer views when the Pinned Property of the analyzer views is set to True.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PinSettings As IAnalyzerPinSettings2
```

### Return Type

The AnalyzerPinSettings object.


---

## Settings Property

*Quelle: `PSV~AnalyzerView~Settings.html` · Polytec PSV Type Library · AnalyzerView Object : Settings Property*

### Description

Specifies the settings of the view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Settings As IAnalyzerViewSettings4
```


---

## Window Property

*Quelle: `PSV~AnalyzerView~Window.html` · Polytec PSV Type Library · AnalyzerView Object : Window Property*

### Description

The viewss Window object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Window As AnalyzerWindow
```


---

## XAxis Property

*Quelle: `PSV~AnalyzerView~XAxis.html` · Polytec PSV Type Library · AnalyzerView Object : XAxis Property*

### Description

The x-axis of the view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property XAxis As IXAxis
```


---

## YAxes Property

*Quelle: `PSV~AnalyzerView~YAxes.html` · Polytec PSV Type Library · AnalyzerView Object : YAxes Property*

### Description

The collection of y-axes of the view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property YAxes As IYAxes
```

### Remarks

Depending on the current display type this collection contains one or two items.
