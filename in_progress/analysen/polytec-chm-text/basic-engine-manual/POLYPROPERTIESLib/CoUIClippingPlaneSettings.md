# POLYPROPERTIESLib – CoUIClippingPlaneSettings

## CoUIClippingPlaneSettings Object

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings for the clipping plane functionality for the 3D view.

### Object Model


---

## CoUIClippingPlaneSettings Object Members

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the clipping plane settings, including the length unit, from the given settings object to this object. |
| Equal | Checks whether the clipping plane settings, including the length unit, stored in the specified settings object are identical to those stored in this object. |
| GetActive | Queries the activation flag of the specified clipping plane. |
| GetPositionBoxSizeRatio | Queries the relative position of the specified clipping plane. |
| SetActive | Sets the activation flag of the specified clipping plane. |
| SetPositionBoxSizeRatio | Sets the relative position of the specified clipping plane. |
| SetSettings | Sets a complete configuration for the clipping planes. |

### Public Properties

| LengthUnit | Specifies the length unit to be used for the display of the absolute position of the clipping planes in the clipping plane configuration dialog. |
|---|---|
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~Clone.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~Copy.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : Copy Method*

### Description

Copies the clipping plane settings, including the length unit, from the given settings object to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal UISettings As IUISettings _
)
```

### Parameters

UISettings

The settings object from which to copy the clipping plane settings.


---

## Equal Method

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~Equal.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : Equal Method*

### Description

Checks whether the clipping plane settings, including the length unit, stored in the specified settings object are identical to those stored in this object.

### Syntax

*Visual Basic:*
```
Public Function Equal( _
   ByVal UISettings As IUISettings _
) As Boolean
```

### Parameters

UISettings

The settings object providing access to the other clipping plane settings.

### Return Type

True if the clipping plane settings are identical.


---

## GetActive Method

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~GetActive.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : GetActive Method*

### Description

Queries the activation flag of the specified clipping plane.

### Syntax

*Visual Basic:*
```
Public Function GetActive( _
   ByVal plane As PTCClippingPlane _
) As Boolean
```

### Parameters

plane

| Value | Description |
|---|---|
| ptcClippingPlaneFar | The back clipping plane perpendicular to the view direction of the virtual camera. |
| ptcClippingPlaneMaxX | The clipping plane oriented towards bigger x-coordinates and perpendicular to the x-axis. |
| ptcClippingPlaneMaxY | The clipping plane oriented towards bigger y-coordinates and perpendicular to the y-axis. |
| ptcClippingPlaneMaxZ | The clipping plane oriented towards bigger z-coordinates and perpendicular to the z-axis. |
| ptcClippingPlaneMinX | The clipping plane oriented towards lower x-coordinates and perpendicular to the x-axis. |
| ptcClippingPlaneMinY | The clipping plane oriented towards lower y-coordinates and perpendicular to the y-axis. |
| ptcClippingPlaneMinZ | The clipping plane oriented towards lower z-coordinates and perpendicular to the z-axis. |
| ptcClippingPlaneNear | The front clipping plane perpendicular to the view direction of the virtual camera. |
The clipping plane.

### Return Type

True if the specified clipping plane is enabled.

### Remarks

For 2D geometries with a configurable vibration direction, the specified clipping plane refers to the coordinate system defined by the currently set vibration direction.


---

## GetPositionBoxSizeRatio Method

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~GetPositionBoxSizeRatio.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : GetPositionBoxSizeRatio Method*

### Description

Queries the relative position of the specified clipping plane.

### Syntax

*Visual Basic:*
```
Public Function GetPositionBoxSizeRatio( _
   ByVal plane As PTCClippingPlane _
) As Double
```

### Parameters

plane

| Value | Description |
|---|---|
| ptcClippingPlaneFar | The back clipping plane perpendicular to the view direction of the virtual camera. |
| ptcClippingPlaneMaxX | The clipping plane oriented towards bigger x-coordinates and perpendicular to the x-axis. |
| ptcClippingPlaneMaxY | The clipping plane oriented towards bigger y-coordinates and perpendicular to the y-axis. |
| ptcClippingPlaneMaxZ | The clipping plane oriented towards bigger z-coordinates and perpendicular to the z-axis. |
| ptcClippingPlaneMinX | The clipping plane oriented towards lower x-coordinates and perpendicular to the x-axis. |
| ptcClippingPlaneMinY | The clipping plane oriented towards lower y-coordinates and perpendicular to the y-axis. |
| ptcClippingPlaneMinZ | The clipping plane oriented towards lower z-coordinates and perpendicular to the z-axis. |
| ptcClippingPlaneNear | The front clipping plane perpendicular to the view direction of the virtual camera. |
The clipping plane.

### Return Type

The relative clipping plane position.

### Remarks

For 2D geometries with a configurable vibration direction, the specified clipping plane refers to the coordinate system defined by the currently set vibration direction.

For the definition of the relative plane position please see the documentation of PTSClippingPlaneSetting.


---

## SetActive Method

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~SetActive.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : SetActive Method*

### Description

Sets the activation flag of the specified clipping plane.

### Syntax

*Visual Basic:*
```
Public Sub SetActive( _
   ByVal plane As PTCClippingPlane, _
   ByVal enablePlane As Boolean _
)
```

### Parameters

plane

| Value | Description |
|---|---|
| ptcClippingPlaneFar | The back clipping plane perpendicular to the view direction of the virtual camera. |
| ptcClippingPlaneMaxX | The clipping plane oriented towards bigger x-coordinates and perpendicular to the x-axis. |
| ptcClippingPlaneMaxY | The clipping plane oriented towards bigger y-coordinates and perpendicular to the y-axis. |
| ptcClippingPlaneMaxZ | The clipping plane oriented towards bigger z-coordinates and perpendicular to the z-axis. |
| ptcClippingPlaneMinX | The clipping plane oriented towards lower x-coordinates and perpendicular to the x-axis. |
| ptcClippingPlaneMinY | The clipping plane oriented towards lower y-coordinates and perpendicular to the y-axis. |
| ptcClippingPlaneMinZ | The clipping plane oriented towards lower z-coordinates and perpendicular to the z-axis. |
| ptcClippingPlaneNear | The front clipping plane perpendicular to the view direction of the virtual camera. |
The clipping plane.

enablePlane

True to enable the specified clipping plane.

### Remarks

For 2D geometries with a configurable vibration direction, the specified clipping plane refers to the coordinate system defined by the currently set vibration direction.


---

## SetPositionBoxSizeRatio Method

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~SetPositionBoxSizeRatio.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : SetPositionBoxSizeRatio Method*

### Description

Sets the relative position of the specified clipping plane.

### Syntax

*Visual Basic:*
```
Public Sub SetPositionBoxSizeRatio( _
   ByVal plane As PTCClippingPlane, _
   ByVal planePositionBoxSizeRatio As Double _
)
```

### Parameters

plane

| Value | Description |
|---|---|
| ptcClippingPlaneFar | The back clipping plane perpendicular to the view direction of the virtual camera. |
| ptcClippingPlaneMaxX | The clipping plane oriented towards bigger x-coordinates and perpendicular to the x-axis. |
| ptcClippingPlaneMaxY | The clipping plane oriented towards bigger y-coordinates and perpendicular to the y-axis. |
| ptcClippingPlaneMaxZ | The clipping plane oriented towards bigger z-coordinates and perpendicular to the z-axis. |
| ptcClippingPlaneMinX | The clipping plane oriented towards lower x-coordinates and perpendicular to the x-axis. |
| ptcClippingPlaneMinY | The clipping plane oriented towards lower y-coordinates and perpendicular to the y-axis. |
| ptcClippingPlaneMinZ | The clipping plane oriented towards lower z-coordinates and perpendicular to the z-axis. |
| ptcClippingPlaneNear | The front clipping plane perpendicular to the view direction of the virtual camera. |
The clipping plane.

planePositionBoxSizeRatio

The relative clipping plane position.

### Remarks

For 2D geometries with a configurable vibration direction, the specified clipping plane refers to the coordinate system defined by the currently set vibration direction.

For the definition of the relative plane position please see the documentation of PTSClippingPlaneSetting.


---

## SetSettings Method

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~SetSettings.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : SetSettings Method*

### Description

Sets a complete configuration for the clipping planes.

### Syntax

*Visual Basic:*
```
Public Sub SetSettings( _
   ByRef planeSettingsParam As PTSClippingPlaneSettings _
)
```

### Parameters

planeSettingsParam

The settings for the clipping planes.

### Remarks

For 2D geometries with a configurable vibration direction, the specified settings always refer to the coordinate system defined by +Z as the vibration direction, i.e. independently of the currently set vibration direction. If a vibration direction other than +Z is set, the settings are converted internally accordingly.


---

## LengthUnit Property

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~LengthUnit.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : LengthUnit Property*

### Description

Specifies the length unit to be used for the display of the absolute position of the clipping planes in the clipping plane configuration dialog.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LengthUnit As PTCLengthUnit
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~Modified.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : Modified Property*

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

## Parent Property

*Quelle: `POLYPROPERTIESLib~CoUIClippingPlaneSettings~Parent.html` · Polytec PolyProperties Type Library · CoUIClippingPlaneSettings Object : Parent Property*

### Description

The parent of the settings object, if the object is attached, or nothing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Parent As Object
```
