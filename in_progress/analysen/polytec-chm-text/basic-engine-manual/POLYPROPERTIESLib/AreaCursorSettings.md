# POLYPROPERTIESLib – AreaCursorSettings

## AreaCursorSettings Object

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings of the area cursor.

### Object Model


---

## AreaCursorSettings Object Members

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Current | The current position of the area cursor. |
|---|---|
| CursorType | The type of the cursor. |
| End | The end of the range of the area cursor. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Start | The start of the range of the area cursor. |
| Step | The step size for the time domain animation. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~Clone.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~Copy.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~Equal.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : Equal Method*

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

## Current Property

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~Current.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : Current Property*

### Description

The current position of the area cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Current As Double
```


---

## CursorType Property

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~CursorType.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : CursorType Property*

### Description

The type of the cursor.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CursorType As PTCCursorType
```

### Return Type

Always ptcCursorTypeArea.


---

## End Property

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~End.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : End Property*

### Description

The end of the range of the area cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property End As Double
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~Modified.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~Parent.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : Parent Property*

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

## Start Property

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~Start.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : Start Property*

### Description

The start of the range of the area cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Start As Double
```


---

## Step Property

*Quelle: `POLYPROPERTIESLib~AreaCursorSettings~Step.html` · Polytec PolyProperties Type Library · AreaCursorSettings Object : Step Property*

### Description

The step size for the time domain animation.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Step As Long
```
