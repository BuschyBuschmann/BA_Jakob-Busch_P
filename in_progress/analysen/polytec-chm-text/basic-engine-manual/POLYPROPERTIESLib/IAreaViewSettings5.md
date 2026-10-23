# POLYPROPERTIESLib – IAreaViewSettings5

## IAreaViewSettings5 Interface

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5.html` · Polytec PolyProperties Type Library*

### Description

User interface settings of an area view.

### Object Model

### Remarks

It is recommended to cast to the AreaViewSettings Object.


---

## IAreaViewSettings5 Interface Members

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| ActiveBand | The name of the active frequency band. This is one of the names returned by the Bands property of the AreaView object . |
|---|---|
| AnimationPhase | The current phase of the animation in degree. |
| AreaCursorSettings | The settings of the area cursor. |
| AreaView | The area view type. |
| AreaViewStyle | The area view style. |
| AutoScaleAmplitudeMax | The flags, whether the maximum amplitude values for scaling should be calculated automatically. |
| AutoScaleAmplitudeMin | The flags, whether the minimum amplitude values for scaling should be calculated automatically. |
| BkColor | The background color of the view. |
| CameraSettings | The settings of the virtual camera that is used for the 3D view. |
| ClippingPlaneSettings | The settings of the clipping planes available for the 3D view. |
| CurrentFrame | The number of the current frame. This is one of the numbers returned by the AvailableFrames property of the AreaView . |
| DataTransparency | The data transparency in percent |
| DisplaySettings | The display settings of the view. |
| IndexColor | The color of the indices (labels) of the scan points. |
| IsolineThickness | The thickness of the isolines in screen pixel. |
| LegendColor | The color of the legend. |
| Modified | Returns whether the settings object has been modified. |
| NumberOfIsolines | The number of isolines. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| PointSelection | The labels (displayed indices) of the selected scan points. |
| ScaleAmplitudeValueMax | The maximum values for scaling the amplitudes. |
| ScaleAmplitudeValueMin | The minimum values for scaling the amplitudes. |
| ScaleFactor | The factor for the amplitude scaling. |
| ScanRangeStyle | Specifies whether and how the scan ranges of the scanning heads are displayed in 3D view. |
| SelectedComponents | The selected components. |
| ShowAxis | Specifies whether a coordinate system is shown in the 3D view. |
| ShowDataGrid | Specifies whether the data grid is shown. |
| ShowDirection | The direction in which the current signal is displayed. |
| ShowImportedTexture | Specifies whether imported textures are shown in area view. |
| ShowIndices | Specifies whether the labels (displayed indices) of the scan points are shown. |
| ShowLightSource | Specifies whether a lighting model is active for the 3D view. |
| ShowSensorDirection | Specifies whether the sensor directions are shown in the 3D view. |
| ShowSurfaceNormal | Specifies whether the surface normals are shown in the 3D view. |
| ShowTitle | Specifies whether a title is shown. |
| ShowZeroPosition | Specifies whether a grid of the scan points at their zero position is shown. |
| Title | The title. |
| TitleFont | The font of the title. |
| VideoPlaneStyle | The video plane style for the 3D view. |
| VideoTransparency | The transparency of the full video image in the 3D view in percent. |
| ViewMode | The view mode. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~Clone.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~Copy.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~Equal.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : Equal Method*

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

## ActiveBand Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ActiveBand.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ActiveBand Property*

### Description

The name of the active frequency band. This is one of the names returned by the Bands property of the AreaView object.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ActiveBand As String
```


---

## AnimationPhase Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~AnimationPhase.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : AnimationPhase Property*

### Description

The current phase of the animation in degree.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AnimationPhase As Double
```


---

## AreaCursorSettings Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~AreaCursorSettings.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : AreaCursorSettings Property*

### Description

The settings of the area cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AreaCursorSettings As AreaCursorSettings
```


---

## AreaView Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~AreaView.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : AreaView Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~AreaViewStyle.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : AreaViewStyle Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~AutoScaleAmplitudeMax.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : AutoScaleAmplitudeMax Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~AutoScaleAmplitudeMin.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : AutoScaleAmplitudeMin Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~BkColor.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : BkColor Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~CameraSettings.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : CameraSettings Property*

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

## ClippingPlaneSettings Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ClippingPlaneSettings.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ClippingPlaneSettings Property*

### Description

The settings of the clipping planes available for the 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ClippingPlaneSettings As CoUIClippingPlaneSettings
```


---

## CurrentFrame Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~CurrentFrame.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : CurrentFrame Property*

### Description

The number of the current frame. This is one of the numbers returned by the AvailableFrames property of the AreaView.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CurrentFrame As Long
```


---

## DataTransparency Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~DataTransparency.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : DataTransparency Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~DisplaySettings.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : DisplaySettings Property*

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

## IndexColor Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~IndexColor.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : IndexColor Property*

### Description

The color of the indices (labels) of the scan points.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property IndexColor As PTCColor
```


---

## IsolineThickness Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~IsolineThickness.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : IsolineThickness Property*

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

## LegendColor Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~LegendColor.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : LegendColor Property*

### Description

The color of the legend.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LegendColor As PTCColor
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~Modified.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~NumberOfIsolines.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : NumberOfIsolines Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~Parent.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : Parent Property*

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

## PointSelection Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~PointSelection.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : PointSelection Property*

### Description

The labels (displayed indices) of the selected scan points.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PointSelection As Long()
```

### Return Type

One dimensional, 0-based array of Long.


---

## ScaleAmplitudeValueMax Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ScaleAmplitudeValueMax.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ScaleAmplitudeValueMax Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ScaleAmplitudeValueMin.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ScaleAmplitudeValueMin Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ScaleFactor.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ScaleFactor Property*

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

## ScanRangeStyle Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ScanRangeStyle.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ScanRangeStyle Property*

### Description

Specifies whether and how the scan ranges of the scanning heads are displayed in 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScanRangeStyle As PTCScanRangeStyle
```


---

## SelectedComponents Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~SelectedComponents.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : SelectedComponents Property*

### Description

The selected components.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SelectedComponents As String()
```

### Return Type

An array of strings where every string represents a selected geometry component. A string of a selected component starts with the path to the component where the parent components are separated by \ (backslash).

### Remarks

When setting the property you can use * in the component paths to select all children of the component with the specified path. Use * as the only character in the string to select all components.


---

## ShowAxis Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowAxis.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowAxis Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowDataGrid.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowDataGrid Property*

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

## ShowDirection Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowDirection.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowDirection Property*

### Description

The direction in which the current signal is displayed.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowDirection As PTCSignalDirection
```


---

## ShowImportedTexture Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowImportedTexture.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowImportedTexture Property*

### Description

Specifies whether imported textures are shown in area view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowImportedTexture As Boolean
```

### Remarks

If the property is set to false the video image is shown as texture.


---

## ShowIndices Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowIndices.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowIndices Property*

### Description

Specifies whether the labels (displayed indices) of the scan points are shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowIndices As PTCAreaShowIndices
```


---

## ShowLightSource Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowLightSource.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowLightSource Property*

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

## ShowSensorDirection Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowSensorDirection.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowSensorDirection Property*

### Description

Specifies whether the sensor directions are shown in the 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowSensorDirection As Boolean
```


---

## ShowSurfaceNormal Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowSurfaceNormal.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowSurfaceNormal Property*

### Description

Specifies whether the surface normals are shown in the 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowSurfaceNormal As Boolean
```


---

## ShowTitle Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowTitle.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowTitle Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ShowZeroPosition.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ShowZeroPosition Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~Title.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : Title Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~TitleFont.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : TitleFont Property*

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

## VideoPlaneStyle Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~VideoPlaneStyle.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : VideoPlaneStyle Property*

### Description

The video plane style for the 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VideoPlaneStyle As PTCVideoPlaneStyle
```


---

## VideoTransparency Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~VideoTransparency.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : VideoTransparency Property*

### Description

The transparency of the full video image in the 3D view in percent.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VideoTransparency As Long
```


---

## ViewMode Property

*Quelle: `POLYPROPERTIESLib~IAreaViewSettings5~ViewMode.html` · Polytec PolyProperties Type Library · IAreaViewSettings5 Interface : ViewMode Property*

### Description

The view mode.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ViewMode As PTCViewMode
```
