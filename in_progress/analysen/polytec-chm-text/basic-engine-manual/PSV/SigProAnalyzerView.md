# PSV – SigProAnalyzerView

## SigProAnalyzerView Object

*Quelle: `PSV~SigProAnalyzerView.html` · Polytec PSV Type Library*

### Description

The object for the analyzer view pane of the signal processor window.

### Object Model


---

## SigProAnalyzerView Object Members

*Quelle: `PSV~SigProAnalyzerView_members.html` · Polytec PSV Type Library*

### Public Methods

| Autoscale | Auto scales the y-axis depending on the currently displayed data. |
|---|---|
| Export | Saves the view content to a file. |
| GetDataSection | The displayed vibration data. |
| ZoomInX | Zooms the x-axis to the given range. |
| ZoomInY | Zooms the y-axis of the given graph to the given range. |
| ZoomOut | Undoes the last zoom in, or if Full is true, does a full zoom out of both the x- and the y-axis. |

### Public Properties

| AvailableBands | Returns an array with the band numbers of the available bands of the displayed vibration data. |
|---|---|
| AvailableFrames | Returns an array with the frame numbers of the available frames of the displayed vibration data. |
| AvailablePoints | Returns an array with the point labels (displayed indices) of the available points of the displayed vibration data. |
| Cursor | The current data cursor of the view. |
| Display | The current display of the view. |
| Domains | The collection of the domains of the vibration data of this view. |
| Settings | Specifies the settings of the view. |
| Window | The view's window object. |
| XAxis | The x-axis of the view. |
| YAxes | The collection of y-axes of the view. |


---

## Autoscale Method

*Quelle: `PSV~SigProAnalyzerView~Autoscale.html` · Polytec PSV Type Library · SigProAnalyzerView Object : Autoscale Method*

### Description

Auto scales the y-axis depending on the currently displayed data.

### Syntax

*Visual Basic:*
```
Public Sub Autoscale()
```


---

## Export Method

*Quelle: `PSV~SigProAnalyzerView~Export.html` · Polytec PSV Type Library · SigProAnalyzerView Object : Export Method*

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


---

## GetDataSection Method

*Quelle: `PSV~SigProAnalyzerView~GetDataSection.html` · Polytec PSV Type Library · SigProAnalyzerView Object : GetDataSection Method*

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

*Quelle: `PSV~SigProAnalyzerView~ZoomInX.html` · Polytec PSV Type Library · SigProAnalyzerView Object : ZoomInX Method*

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

*Quelle: `PSV~SigProAnalyzerView~ZoomInY.html` · Polytec PSV Type Library · SigProAnalyzerView Object : ZoomInY Method*

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

*Quelle: `PSV~SigProAnalyzerView~ZoomOut.html` · Polytec PSV Type Library · SigProAnalyzerView Object : ZoomOut Method*

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

## AvailableBands Property

*Quelle: `PSV~SigProAnalyzerView~AvailableBands.html` · Polytec PSV Type Library · SigProAnalyzerView Object : AvailableBands Property*

### Description

Returns an array with the band numbers of the available bands of the displayed vibration data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AvailableBands As Long()
```

### Return Type

One dimensional, 0-based array of longs.


---

## AvailableFrames Property

*Quelle: `PSV~SigProAnalyzerView~AvailableFrames.html` · Polytec PSV Type Library · SigProAnalyzerView Object : AvailableFrames Property*

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

## AvailablePoints Property

*Quelle: `PSV~SigProAnalyzerView~AvailablePoints.html` · Polytec PSV Type Library · SigProAnalyzerView Object : AvailablePoints Property*

### Description

Returns an array with the point labels (displayed indices) of the available points of the displayed vibration data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AvailablePoints As Long()
```

### Return Type

One dimensional, 0-based array of longs.


---

## Cursor Property

*Quelle: `PSV~SigProAnalyzerView~Cursor.html` · Polytec PSV Type Library · SigProAnalyzerView Object : Cursor Property*

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

*Quelle: `PSV~SigProAnalyzerView~Display.html` · Polytec PSV Type Library · SigProAnalyzerView Object : Display Property*

### Description

The current display of the view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Display As IDisplay2
```


---

## Domains Property

*Quelle: `PSV~SigProAnalyzerView~Domains.html` · Polytec PSV Type Library · SigProAnalyzerView Object : Domains Property*

### Description

The collection of the domains of the vibration data of this view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Domains As IDomains2
```


---

## Settings Property

*Quelle: `PSV~SigProAnalyzerView~Settings.html` · Polytec PSV Type Library · SigProAnalyzerView Object : Settings Property*

### Description

Specifies the settings of the view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Settings As ISigProAnalyzerViewSettings
```


---

## Window Property

*Quelle: `PSV~SigProAnalyzerView~Window.html` · Polytec PSV Type Library · SigProAnalyzerView Object : Window Property*

### Description

The view's window object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Window As SigProWindow
```


---

## XAxis Property

*Quelle: `PSV~SigProAnalyzerView~XAxis.html` · Polytec PSV Type Library · SigProAnalyzerView Object : XAxis Property*

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

*Quelle: `PSV~SigProAnalyzerView~YAxes.html` · Polytec PSV Type Library · SigProAnalyzerView Object : YAxes Property*

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
