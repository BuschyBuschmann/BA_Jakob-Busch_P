# POLYPROPERTIESLib – WindowSettings

## WindowSettings Object

*Quelle: `POLYPROPERTIESLib~WindowSettings.html` · Polytec PolyProperties Type Library*

### Description

User interface settings of a window.

### Object Model


---

## WindowSettings Object Members

*Quelle: `POLYPROPERTIESLib~WindowSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Height | Specifies the height of the window in pixel. |
|---|---|
| Left | Specifies the position of the left border of the window in pixel. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Top | Specifies the position of the top border of the window in pixel. |
| Width | Specifies the width of the window in pixel. |
| WindowState | Specifies the state of the window. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~WindowSettings~Clone.html` · Polytec PolyProperties Type Library · WindowSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~WindowSettings~Copy.html` · Polytec PolyProperties Type Library · WindowSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~WindowSettings~Equal.html` · Polytec PolyProperties Type Library · WindowSettings Object : Equal Method*

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

## Height Property

*Quelle: `POLYPROPERTIESLib~WindowSettings~Height.html` · Polytec PolyProperties Type Library · WindowSettings Object : Height Property*

### Description

Specifies the height of the window in pixel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Height As Long
```


---

## Left Property

*Quelle: `POLYPROPERTIESLib~WindowSettings~Left.html` · Polytec PolyProperties Type Library · WindowSettings Object : Left Property*

### Description

Specifies the position of the left border of the window in pixel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Left As Long
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~WindowSettings~Modified.html` · Polytec PolyProperties Type Library · WindowSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~WindowSettings~Parent.html` · Polytec PolyProperties Type Library · WindowSettings Object : Parent Property*

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

## Top Property

*Quelle: `POLYPROPERTIESLib~WindowSettings~Top.html` · Polytec PolyProperties Type Library · WindowSettings Object : Top Property*

### Description

Specifies the position of the top border of the window in pixel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Top As Long
```


---

## Width Property

*Quelle: `POLYPROPERTIESLib~WindowSettings~Width.html` · Polytec PolyProperties Type Library · WindowSettings Object : Width Property*

### Description

Specifies the width of the window in pixel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Width As Long
```


---

## WindowState Property

*Quelle: `POLYPROPERTIESLib~WindowSettings~WindowState.html` · Polytec PolyProperties Type Library · WindowSettings Object : WindowState Property*

### Description

Specifies the state of the window.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property WindowState As PTCWindowState
```
