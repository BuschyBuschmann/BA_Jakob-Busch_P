# POLYPROPERTIESLib – SpectrogramAreaViewSettings

## SpectrogramAreaViewSettings Object

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings.html` · Polytec PolyProperties Type Library*

### Description

User interface settings of an area view of a spectrogram or Campbell diagram.

### Object Model


---

## SpectrogramAreaViewSettings Object Members

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| AreaView | The area view type. |
|---|---|
| AreaViewStyle | The area view style. |
| AutoScaleAmplitudeMax | The flags, whether the maximum amplitude values for scaling should be calculated automatically. |
| AutoScaleAmplitudeMin | The flags, whether the minimum amplitude values for scaling should be calculated automatically. |
| BkColor | The background color of the view. |
| CameraSettings | The settings of the virtual camera that is used for the 3D view. |
| CursorType | The type of the currently displayed cursors. |
| DataTransparency | The data transparency in percent |
| DisplaySettings | The display settings of the view. |
| GridLineColor | Specifies the color of the grid. |
| IsolineThickness | The thickness of the isolines in screen pixel. |
| Modified | Returns whether the settings object has been modified. |
| NumberOfIsolines | The number of isolines. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| ScaleAmplitudeValueMax | The maximum values for scaling the amplitudes. |
| ScaleAmplitudeValueMin | The minimum values for scaling the amplitudes. |
| ScaleFactor | The factor for the amplitude scaling. |
| ShowAxis | Specifies whether a coordinate system is shown in the 3D view. |
| ShowDataGrid | Specifies whether the data grid is shown. |
| ShowLightSource | Specifies whether a lighting model is active for the 3D view. |
| ShowTitle | Specifies whether a title is shown. |
| ShowZeroPosition | Specifies whether a grid of the scan points at their zero position is shown. |
| Title | The title. |
| TitleFont | The font of the title. |
| XRangeSettings | The settings of the range of the x-axis. |
| YRangeSettings | The settings of the range of the y-axis. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~Clone.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~Copy.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : Copy Method*

### Description

Copies the properties of the given settings object to this settings object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal UISettings As IUISettings _
)
```

### Parameters

UISettings

The other settings object.


---

## Equal Method

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~Equal.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : Equal Method*

### Description

Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values.

### Syntax

*Visual Basic:*
```
Public Function Equal( _
   ByVal UISettings As IUISettings _
) As Boolean
```

### Parameters

UISettings

The other settings object.

### Return Type

True if all properties are equal.


---

## AreaView Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~AreaView.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : AreaView Property*

### Description

The area view type.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AreaView As PTCAreaView
```


---

## AreaViewStyle Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~AreaViewStyle.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : AreaViewStyle Property*

### Description

The area view style.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AreaViewStyle As PTCAreaViewStyle
```


---

## AutoScaleAmplitudeMax Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~AutoScaleAmplitudeMax.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : AutoScaleAmplitudeMax Property*

### Description

The flags, whether the maximum amplitude values for scaling should be calculated automatically.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AutoScaleAmplitudeMax As Boolean()
```

### Return Type

One dimensional, 0-based array of Boolean.

### Remarks

The number of values in the array depends on the display type of the area view (1 graph or 2 graphs).


---

## AutoScaleAmplitudeMin Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~AutoScaleAmplitudeMin.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : AutoScaleAmplitudeMin Property*

### Description

The flags, whether the minimum amplitude values for scaling should be calculated automatically.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AutoScaleAmplitudeMin As Boolean()
```

### Return Type

One dimensional, 0-based array of Boolean.

### Remarks

The number of values in the array depends on the display type of the area view (1 graph or 2 graphs).


---

## BkColor Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~BkColor.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : BkColor Property*

### Description

The background color of the view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property BkColor As PTCColor
```


---

## CameraSettings Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~CameraSettings.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : CameraSettings Property*

### Description

The settings of the virtual camera that is used for the 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CameraSettings As IUICameraSettings
```


---

## CursorType Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~CursorType.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : CursorType Property*

### Description

The type of the currently displayed cursors.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CursorType As PTCAreaCursorType
```


---

## DataTransparency Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~DataTransparency.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : DataTransparency Property*

### Description

The data transparency in percent

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DataTransparency As Long
```


---

## DisplaySettings Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~DisplaySettings.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : DisplaySettings Property*

### Description

The display settings of the view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DisplaySettings As DisplaySettings
```


---

## GridLineColor Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~GridLineColor.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : GridLineColor Property*

### Description

Specifies the color of the grid.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property GridLineColor As PTCColor
```


---

## IsolineThickness Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~IsolineThickness.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : IsolineThickness Property*

### Description

The thickness of the isolines in screen pixel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property IsolineThickness As Long
```

### Example


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~Modified.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : Modified Property*

### Description

Returns whether the settings object has been modified.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Modified As Boolean
```


---

## NumberOfIsolines Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~NumberOfIsolines.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : NumberOfIsolines Property*

### Description

The number of isolines.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property NumberOfIsolines As Long
```


---

## Parent Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~Parent.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : Parent Property*

### Description

The parent of the settings object, if the object is attached, or nothing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Parent As Object
```


---

## ScaleAmplitudeValueMax Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~ScaleAmplitudeValueMax.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : ScaleAmplitudeValueMax Property*

### Description

The maximum values for scaling the amplitudes.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScaleAmplitudeValueMax As Double()
```

### Return Type

One dimensional, 0-based array of Double.

### Remarks

The number of values in the array depends on the display type of the area view (1 graph or 2 graphs).


---

## ScaleAmplitudeValueMin Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~ScaleAmplitudeValueMin.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : ScaleAmplitudeValueMin Property*

### Description

The minimum values for scaling the amplitudes.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScaleAmplitudeValueMin As Double()
```

### Return Type

One dimensional, 0-based array of Double.

### Remarks

The number of values in the array depends on the display type of the area view (1 graph or 2 graphs).


---

## ScaleFactor Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~ScaleFactor.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : ScaleFactor Property*

### Description

The factor for the amplitude scaling.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScaleFactor As Double
```


---

## ShowAxis Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~ShowAxis.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : ShowAxis Property*

### Description

Specifies whether a coordinate system is shown in the 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowAxis As Boolean
```


---

## ShowDataGrid Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~ShowDataGrid.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : ShowDataGrid Property*

### Description

Specifies whether the data grid is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowDataGrid As Boolean
```


---

## ShowLightSource Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~ShowLightSource.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : ShowLightSource Property*

### Description

Specifies whether a lighting model is active for the 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowLightSource As Boolean
```


---

## ShowTitle Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~ShowTitle.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : ShowTitle Property*

### Description

Specifies whether a title is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowTitle As Boolean
```


---

## ShowZeroPosition Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~ShowZeroPosition.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : ShowZeroPosition Property*

### Description

Specifies whether a grid of the scan points at their zero position is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowZeroPosition As Boolean
```


---

## Title Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~Title.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : Title Property*

### Description

The title.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Title As String
```


---

## TitleFont Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~TitleFont.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : TitleFont Property*

### Description

The font of the title.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property TitleFont As Font
```


---

## XRangeSettings Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~XRangeSettings.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : XRangeSettings Property*

### Description

The settings of the range of the x-axis.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property XRangeSettings As RangeSettings
```


---

## YRangeSettings Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAreaViewSettings~YRangeSettings.html` · Polytec PolyProperties Type Library · SpectrogramAreaViewSettings Object : YRangeSettings Property*

### Description

The settings of the range of the y-axis.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property YRangeSettings As RangeSettings
```
