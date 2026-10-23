# PSV – SpectrogramAreaView

## SpectrogramAreaView Object

*Quelle: `PSV~SpectrogramAreaView.html` · Polytec PSV Type Library*

### Description

The object for the area view pane of the SpectrogramWindow Object.

### Object Model


---

## SpectrogramAreaView Object Members

*Quelle: `PSV~SpectrogramAreaView_members.html` · Polytec PSV Type Library*

### Public Methods

| Export | Saves the view content to a file. |
|---|---|
| Pan | Pans the view by the given amount of screen pixels. |
| ResetSight | Resets the sight of the view to default sight. |
| ScaleDefault | Sets the scaling of the vibration data to a default value. |
| ScaleDown | Scales the vibration data down by a single step. |
| ScaleUp | Scales the vibration data up by a single step. |
| Zoom | Zooms the view by the given factor. |

### Public Properties

| Settings | Specifies the settings of the view. |
|---|---|
| Window | The view's window object. |


---

## Export Method

*Quelle: `PSV~SpectrogramAreaView~Export.html` · Polytec PSV Type Library · SpectrogramAreaView Object : Export Method*

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

*Quelle: `PSV~SpectrogramAreaView~Pan.html` · Polytec PSV Type Library · SpectrogramAreaView Object : Pan Method*

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

## ResetSight Method

*Quelle: `PSV~SpectrogramAreaView~ResetSight.html` · Polytec PSV Type Library · SpectrogramAreaView Object : ResetSight Method*

### Description

Resets the sight of the view to default sight.

### Syntax

*Visual Basic:*
```
Public Sub ResetSight()
```


---

## ScaleDefault Method

*Quelle: `PSV~SpectrogramAreaView~ScaleDefault.html` · Polytec PSV Type Library · SpectrogramAreaView Object : ScaleDefault Method*

### Description

Sets the scaling of the vibration data to a default value.

### Syntax

*Visual Basic:*
```
Public Sub ScaleDefault()
```


---

## ScaleDown Method

*Quelle: `PSV~SpectrogramAreaView~ScaleDown.html` · Polytec PSV Type Library · SpectrogramAreaView Object : ScaleDown Method*

### Description

Scales the vibration data down by a single step.

### Syntax

*Visual Basic:*
```
Public Sub ScaleDown()
```


---

## ScaleUp Method

*Quelle: `PSV~SpectrogramAreaView~ScaleUp.html` · Polytec PSV Type Library · SpectrogramAreaView Object : ScaleUp Method*

### Description

Scales the vibration data up by a single step.

### Syntax

*Visual Basic:*
```
Public Sub ScaleUp()
```


---

## Zoom Method

*Quelle: `PSV~SpectrogramAreaView~Zoom.html` · Polytec PSV Type Library · SpectrogramAreaView Object : Zoom Method*

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

## Settings Property

*Quelle: `PSV~SpectrogramAreaView~Settings.html` · Polytec PSV Type Library · SpectrogramAreaView Object : Settings Property*

### Description

Specifies the settings of the view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Settings As ISpectrogramAreaViewSettings
```


---

## Window Property

*Quelle: `PSV~SpectrogramAreaView~Window.html` · Polytec PSV Type Library · SpectrogramAreaView Object : Window Property*

### Description

The view's window object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Window As SpectrogramWindow
```
