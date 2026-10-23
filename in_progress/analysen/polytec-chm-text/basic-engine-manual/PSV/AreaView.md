# PSV – AreaView

## AreaView Object

*Quelle: `PSV~AreaView.html` · Polytec PSV Type Library*

### Description

The object for the area view pane of the AreaWindow.

### Object Model


---

## AreaView Object Members

*Quelle: `PSV~AreaView_members.html` · Polytec PSV Type Library*

### Public Methods

| Export | Saves the view content to a file. |
|---|---|
| Pan | Pans the view by the given amount of screen pixels. |
| ProjectView | Projects the 3D coordinates of the scan points to the 2D plane using the current camera position and direction of the 3D view. |
| ResetSight | Resets the sight of the view to default sight. |
| ScaleDefault | Sets the scaling of the vibration data to a default value. |
| ScaleDown | Scales the vibration data down by a single step. |
| ScaleUp | Scales the vibration data up by a single step. |
| StartAnimation | Starts the animation of the vibration data of this view. |
| StepAnimationBackward | Moves the animation of the vibration data a single step backward. |
| StepAnimationForward | Moves the animation of the vibration data a single step forward. |
| StopAnimation | Stops the animation of the vibration data of this view. |
| Zoom | Zooms the view by the given factor. |

### Public Properties

| AreaCursor | The current area cursor of the view. |
|---|---|
| AvailableFrames | Returns an array with the frame numbers of the available frames of the displayed vibration data. |
| Bands | The array with the names of the frequency bands of this view. |
| Components | Gets an array of the names of the geometry components of the current area view. |
| Display | The current display of the view. |
| Domains | The collection of the domains of the vibration data of this view. |
| Pinned | Specifies whether the settings of the area view are pinned to the settings of other area views. |
| PinSettings | Specifies which settings of the area view should be synchronized with other area views when the Pinned Property of the area views is set to True. |
| Settings | Specifies the settings of the view. |
| Window | The view's window object. |


---

## Export Method

*Quelle: `PSV~AreaView~Export.html` · Polytec PSV Type Library · AreaView Object : Export Method*

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

## Pan Method

*Quelle: `PSV~AreaView~Pan.html` · Polytec PSV Type Library · AreaView Object : Pan Method*

### Description

Pans the view by the given amount of screen pixels.

### Syntax

*Visual Basic:*
```
Public Sub Pan( _
   ByVal XDiff As Long, _
   ByVal YDiff As Long _
)
```

### Parameters

XDiff

Pan by this number of pixels in x.

YDiff

Pan by this number of pixels in y.


---

## ProjectView Method

*Quelle: `PSV~AreaView~ProjectView.html` · Polytec PSV Type Library · AreaView Object : ProjectView Method*

### Description

Projects the 3D coordinates of the scan points to the 2D plane using the current camera position and direction of the 3D view.

### Syntax

*Visual Basic:*
```
Public Function ProjectView( _
   ByVal psaScanPointIndices() As Long _
) As Single()
```

### Parameters

psaScanPointIndices

An array of 1-based scan point indices.

### Return Type

One-dimensional, 0-based array of Single containing the alternating x, y, and depth coordinates for every scan point specified in the input array.

### Remarks

The size of the returned array is three times the size of the input array.

You can pass an empty or scan point indices array or Nothing to the method. Then the coordinates of all defined scan points will be returned.


---

## ResetSight Method

*Quelle: `PSV~AreaView~ResetSight.html` · Polytec PSV Type Library · AreaView Object : ResetSight Method*

### Description

Resets the sight of the view to default sight.

### Syntax

*Visual Basic:*
```
Public Sub ResetSight()
```


---

## ScaleDefault Method

*Quelle: `PSV~AreaView~ScaleDefault.html` · Polytec PSV Type Library · AreaView Object : ScaleDefault Method*

### Description

Sets the scaling of the vibration data to a default value.

### Syntax

*Visual Basic:*
```
Public Sub ScaleDefault()
```


---

## ScaleDown Method

*Quelle: `PSV~AreaView~ScaleDown.html` · Polytec PSV Type Library · AreaView Object : ScaleDown Method*

### Description

Scales the vibration data down by a single step.

### Syntax

*Visual Basic:*
```
Public Sub ScaleDown()
```


---

## ScaleUp Method

*Quelle: `PSV~AreaView~ScaleUp.html` · Polytec PSV Type Library · AreaView Object : ScaleUp Method*

### Description

Scales the vibration data up by a single step.

### Syntax

*Visual Basic:*
```
Public Sub ScaleUp()
```


---

## StartAnimation Method

*Quelle: `PSV~AreaView~StartAnimation.html` · Polytec PSV Type Library · AreaView Object : StartAnimation Method*

### Description

Starts the animation of the vibration data of this view.

### Syntax

*Visual Basic:*
```
Public Sub StartAnimation()
```


---

## StepAnimationBackward Method

*Quelle: `PSV~AreaView~StepAnimationBackward.html` · Polytec PSV Type Library · AreaView Object : StepAnimationBackward Method*

### Description

Moves the animation of the vibration data a single step backward.

### Syntax

*Visual Basic:*
```
Public Sub StepAnimationBackward()
```


---

## StepAnimationForward Method

*Quelle: `PSV~AreaView~StepAnimationForward.html` · Polytec PSV Type Library · AreaView Object : StepAnimationForward Method*

### Description

Moves the animation of the vibration data a single step forward.

### Syntax

*Visual Basic:*
```
Public Sub StepAnimationForward()
```


---

## StopAnimation Method

*Quelle: `PSV~AreaView~StopAnimation.html` · Polytec PSV Type Library · AreaView Object : StopAnimation Method*

### Description

Stops the animation of the vibration data of this view.

### Syntax

*Visual Basic:*
```
Public Sub StopAnimation()
```


---

## Zoom Method

*Quelle: `PSV~AreaView~Zoom.html` · Polytec PSV Type Library · AreaView Object : Zoom Method*

### Description

Zooms the view by the given factor.

### Syntax

*Visual Basic:*
```
Public Sub Zoom( _
   ByVal ZoomFactor As Double _
)
```

### Parameters

ZoomFactor

The zoom factor.

### Remarks

A factor > 1 zooms in, a factor < 1 zooms out.


---

## AreaCursor Property

*Quelle: `PSV~AreaView~AreaCursor.html` · Polytec PSV Type Library · AreaView Object : AreaCursor Property*

### Description

The current area cursor of the view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AreaCursor As AreaCursor
```


---

## AvailableFrames Property

*Quelle: `PSV~AreaView~AvailableFrames.html` · Polytec PSV Type Library · AreaView Object : AvailableFrames Property*

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

## Bands Property

*Quelle: `PSV~AreaView~Bands.html` · Polytec PSV Type Library · AreaView Object : Bands Property*

### Description

The array with the names of the frequency bands of this view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Bands As String()
```

### Return Type

One-dimensional, 0-based array of strings.


---

## Components Property

*Quelle: `PSV~AreaView~Components.html` · Polytec PSV Type Library · AreaView Object : Components Property*

### Description

Gets an array of the names of the geometry components of the current area view.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Components As String()
```

### Return Type

An array of strings where every string represents a geometry component. A string of a component starts with the path to the component where the parent components are separated by \ (backslash).


---

## Display Property

*Quelle: `PSV~AreaView~Display.html` · Polytec PSV Type Library · AreaView Object : Display Property*

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

*Quelle: `PSV~AreaView~Domains.html` · Polytec PSV Type Library · AreaView Object : Domains Property*

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

*Quelle: `PSV~AreaView~Pinned.html` · Polytec PSV Type Library · AreaView Object : Pinned Property*

### Description

Specifies whether the settings of the area view are pinned to the settings of other area views.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Pinned As Boolean
```

### Remarks

The settings of all area views with this property set to True are synchronized. If you change the settings of one of those area views all other area views will change accordingly. You can use the PinSettings Property to specify which settings should be synchronized.


---

## PinSettings Property

*Quelle: `PSV~AreaView~PinSettings.html` · Polytec PSV Type Library · AreaView Object : PinSettings Property*

### Description

Specifies which settings of the area view should be synchronized with other area views when the Pinned Property of the area views is set to True.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PinSettings As IAreaPinSettings2
```

### Return Type

The AreaPinSettings object.


---

## Settings Property

*Quelle: `PSV~AreaView~Settings.html` · Polytec PSV Type Library · AreaView Object : Settings Property*

### Description

Specifies the settings of the view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Settings As IAreaViewSettings5
```


---

## Window Property

*Quelle: `PSV~AreaView~Window.html` · Polytec PSV Type Library · AreaView Object : Window Property*

### Description

The view's window object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Window As AreaWindow
```
