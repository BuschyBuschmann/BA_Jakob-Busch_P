# POLYPROPERTIESLib – AreaViewSettings

## AreaViewSettings Object

*Quelle: `POLYPROPERTIESLib~AreaViewSettings.html` · Polytec PolyProperties Type Library*

### Description

User interface settings of an area view.

### Object Model


---

## AreaViewSettings Object Members

*Quelle: `POLYPROPERTIESLib~AreaViewSettings_members.html` · Polytec PolyProperties Type Library*

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
| ShowScanRange | Specifies whether the scan range of the scanning heads is shown in the 3D view. |
| ShowSensorDirection | Specifies whether the sensor directions are shown in the 3D view. |
| ShowSurfaceNormal | Specifies whether the surface normals are shown in the 3D view. |
| ShowTitle | Specifies whether a title is shown. |
| ShowVideo | Specifies whether the full video image is shown in the 3D view. |
| ShowZeroPosition | Specifies whether a grid of the scan points at their zero position is shown. |
| Title | The title. |
| TitleFont | The font of the title. |
| VideoPlaneStyle | The video plane style for the 3D view. |
| VideoTransparency | The transparency of the full video image in the 3D view in percent. |
| ViewMode | The view mode. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~Clone.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~Copy.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~Equal.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : Equal Method*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ActiveBand.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ActiveBand Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~AnimationPhase.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : AnimationPhase Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~AreaCursorSettings.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : AreaCursorSettings Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~AreaView.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : AreaView Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~AreaViewStyle.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : AreaViewStyle Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~AutoScaleAmplitudeMax.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : AutoScaleAmplitudeMax Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~AutoScaleAmplitudeMin.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : AutoScaleAmplitudeMin Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~BkColor.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : BkColor Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~CameraSettings.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : CameraSettings Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ClippingPlaneSettings.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ClippingPlaneSettings Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~CurrentFrame.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : CurrentFrame Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~DataTransparency.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : DataTransparency Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~DisplaySettings.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : DisplaySettings Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~IndexColor.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : IndexColor Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~IsolineThickness.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : IsolineThickness Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~LegendColor.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : LegendColor Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~Modified.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~NumberOfIsolines.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : NumberOfIsolines Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~Parent.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : Parent Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~PointSelection.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : PointSelection Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ScaleAmplitudeValueMax.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ScaleAmplitudeValueMax Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ScaleAmplitudeValueMin.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ScaleAmplitudeValueMin Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ScaleFactor.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ScaleFactor Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ScanRangeStyle.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ScanRangeStyle Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~SelectedComponents.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : SelectedComponents Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowAxis.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowAxis Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowDataGrid.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowDataGrid Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowDirection.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowDirection Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowImportedTexture.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowImportedTexture Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowIndices.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowIndices Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowLightSource.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowLightSource Property*

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

## ShowScanRange Property

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowScanRange.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowScanRange Property*

### Description

Specifies whether the scan range of the scanning heads is shown in the 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowScanRange As Boolean
```


---

## ShowSensorDirection Property

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowSensorDirection.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowSensorDirection Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowSurfaceNormal.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowSurfaceNormal Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowTitle.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowTitle Property*

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

## ShowVideo Property

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowVideo.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowVideo Property*

### Description

Specifies whether the full video image is shown in the 3D view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowVideo As Boolean
```


---

## ShowZeroPosition Property

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ShowZeroPosition.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ShowZeroPosition Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~Title.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : Title Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~TitleFont.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : TitleFont Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~VideoPlaneStyle.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : VideoPlaneStyle Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~VideoTransparency.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : VideoTransparency Property*

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

*Quelle: `POLYPROPERTIESLib~AreaViewSettings~ViewMode.html` · Polytec PolyProperties Type Library · AreaViewSettings Object : ViewMode Property*

### Description

The view mode.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ViewMode As PTCViewMode
```
