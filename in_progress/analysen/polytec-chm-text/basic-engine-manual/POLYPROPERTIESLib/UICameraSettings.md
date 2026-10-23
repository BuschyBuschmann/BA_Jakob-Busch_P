# POLYPROPERTIESLib – UICameraSettings

## UICameraSettings Object

*Quelle: `POLYPROPERTIESLib~UICameraSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings of the virtual camera that is used for the 3D view.

### Object Model

### Remarks

The origin of coordinate system for the focal point, the position and the view-up vector of the camera is the centroid of the scan points. The maximum distance of a scan point to the centroid in this coordinate system is 1.


---

## UICameraSettings Object Members

*Quelle: `POLYPROPERTIESLib~UICameraSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| FocalPointX | The x-coordinate of the focal point (point of view). |
|---|---|
| FocalPointY | The y-coordinate of the focal point (point of view). |
| FocalPointZ | The z-coordinate of the focal point (point of view). |
| Modified | Returns whether the settings object has been modified. |
| ParallelScale | The scale of the camera for parallel projection. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| PositionX | The x-coordinate of the position of the camera. |
| PositionY | The y-coordinate of the position of the camera. |
| PositionZ | The z-coordinate of the position of the camera. |
| Projection | The projection mode of the camera. |
| RotationOriginX | The x-coordinate of the origin of the camera rotation. |
| RotationOriginY | The y-coordinate of the origin of the camera rotation. |
| RotationOriginZ | The z-coordinate of the origin of the camera rotation. |
| ViewAngle | The view angle of the camera in degree. |
| ViewUpX | The x-coordinate of the view-up vector of the camera. |
| ViewUpY | The y-coordinate of the view-up vector of the camera. |
| ViewUpZ | The z-coordinate of the view-up vector of the camera. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~UICameraSettings~Clone.html` · Polytec PolyProperties Type Library · UICameraSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~UICameraSettings~Copy.html` · Polytec PolyProperties Type Library · UICameraSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~UICameraSettings~Equal.html` · Polytec PolyProperties Type Library · UICameraSettings Object : Equal Method*

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

## FocalPointX Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~FocalPointX.html` · Polytec PolyProperties Type Library · UICameraSettings Object : FocalPointX Property*

### Description

The x-coordinate of the focal point (point of view).

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FocalPointX As Double
```


---

## FocalPointY Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~FocalPointY.html` · Polytec PolyProperties Type Library · UICameraSettings Object : FocalPointY Property*

### Description

The y-coordinate of the focal point (point of view).

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FocalPointY As Double
```


---

## FocalPointZ Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~FocalPointZ.html` · Polytec PolyProperties Type Library · UICameraSettings Object : FocalPointZ Property*

### Description

The z-coordinate of the focal point (point of view).

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FocalPointZ As Double
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~Modified.html` · Polytec PolyProperties Type Library · UICameraSettings Object : Modified Property*

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

## ParallelScale Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~ParallelScale.html` · Polytec PolyProperties Type Library · UICameraSettings Object : ParallelScale Property*

### Description

The scale of the camera for parallel projection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ParallelScale As Double
```


---

## Parent Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~Parent.html` · Polytec PolyProperties Type Library · UICameraSettings Object : Parent Property*

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

## PositionX Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~PositionX.html` · Polytec PolyProperties Type Library · UICameraSettings Object : PositionX Property*

### Description

The x-coordinate of the position of the camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PositionX As Double
```


---

## PositionY Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~PositionY.html` · Polytec PolyProperties Type Library · UICameraSettings Object : PositionY Property*

### Description

The y-coordinate of the position of the camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PositionY As Double
```


---

## PositionZ Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~PositionZ.html` · Polytec PolyProperties Type Library · UICameraSettings Object : PositionZ Property*

### Description

The z-coordinate of the position of the camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PositionZ As Double
```


---

## Projection Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~Projection.html` · Polytec PolyProperties Type Library · UICameraSettings Object : Projection Property*

### Description

The projection mode of the camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Projection As PTCCameraProjection
```


---

## RotationOriginX Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~RotationOriginX.html` · Polytec PolyProperties Type Library · UICameraSettings Object : RotationOriginX Property*

### Description

The x-coordinate of the origin of the camera rotation.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RotationOriginX As Double
```


---

## RotationOriginY Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~RotationOriginY.html` · Polytec PolyProperties Type Library · UICameraSettings Object : RotationOriginY Property*

### Description

The y-coordinate of the origin of the camera rotation.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RotationOriginY As Double
```


---

## RotationOriginZ Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~RotationOriginZ.html` · Polytec PolyProperties Type Library · UICameraSettings Object : RotationOriginZ Property*

### Description

The z-coordinate of the origin of the camera rotation.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RotationOriginZ As Double
```


---

## ViewAngle Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~ViewAngle.html` · Polytec PolyProperties Type Library · UICameraSettings Object : ViewAngle Property*

### Description

The view angle of the camera in degree.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ViewAngle As Double
```


---

## ViewUpX Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~ViewUpX.html` · Polytec PolyProperties Type Library · UICameraSettings Object : ViewUpX Property*

### Description

The x-coordinate of the view-up vector of the camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ViewUpX As Double
```


---

## ViewUpY Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~ViewUpY.html` · Polytec PolyProperties Type Library · UICameraSettings Object : ViewUpY Property*

### Description

The y-coordinate of the view-up vector of the camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ViewUpY As Double
```


---

## ViewUpZ Property

*Quelle: `POLYPROPERTIESLib~UICameraSettings~ViewUpZ.html` · Polytec PolyProperties Type Library · UICameraSettings Object : ViewUpZ Property*

### Description

The z-coordinate of the view-up vector of the camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ViewUpZ As Double
```
