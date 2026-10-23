# POLYPROPERTIESLib – IUICameraSettings

## IUICameraSettings Interface

*Quelle: `POLYPROPERTIESLib~IUICameraSettings.html` · Polytec PolyProperties Type Library*

### Description

It is recommended to cast to the UICameraSettings Object.

### Object Model


---

## IUICameraSettings Interface Members

*Quelle: `POLYPROPERTIESLib~IUICameraSettings_members.html` · Polytec PolyProperties Type Library*

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
| ViewAngle | The view angle of the camera in degree. |
| ViewUpX | The x-coordinate of the view-up vector of the camera. |
| ViewUpY | The y-coordinate of the view-up vector of the camera. |
| ViewUpZ | The z-coordinate of the view-up vector of the camera. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~Clone.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~Copy.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~Equal.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : Equal Method*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~FocalPointX.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : FocalPointX Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~FocalPointY.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : FocalPointY Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~FocalPointZ.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : FocalPointZ Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~Modified.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~ParallelScale.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : ParallelScale Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~Parent.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : Parent Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~PositionX.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : PositionX Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~PositionY.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : PositionY Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~PositionZ.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : PositionZ Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~Projection.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : Projection Property*

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

## ViewAngle Property

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~ViewAngle.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : ViewAngle Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~ViewUpX.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : ViewUpX Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~ViewUpY.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : ViewUpY Property*

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

*Quelle: `POLYPROPERTIESLib~IUICameraSettings~ViewUpZ.html` · Polytec PolyProperties Type Library · IUICameraSettings Interface : ViewUpZ Property*

### Description

The z-coordinate of the view-up vector of the camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ViewUpZ As Double
```
