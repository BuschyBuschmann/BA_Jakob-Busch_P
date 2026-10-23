# POLYPROPERTIESLib – SingleCursorSettings

## SingleCursorSettings Object

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings of the single cursor.

### Object Model


---

## SingleCursorSettings Object Members

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| CursorType | The type of the data cursor. |
|---|---|
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Position | The position of the line of the single cursor. |
| ShowHorizontalLine | Specifies whether a horizontal line is shown at the intersection of the cursor line with the data. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings~Clone.html` · Polytec PolyProperties Type Library · SingleCursorSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings~Copy.html` · Polytec PolyProperties Type Library · SingleCursorSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings~Equal.html` · Polytec PolyProperties Type Library · SingleCursorSettings Object : Equal Method*

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

## CursorType Property

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings~CursorType.html` · Polytec PolyProperties Type Library · SingleCursorSettings Object : CursorType Property*

### Description

The type of the data cursor.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CursorType As PTCCursorType
```

### Return Type

Always ptcCursorTypeSingle.


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings~Modified.html` · Polytec PolyProperties Type Library · SingleCursorSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings~Parent.html` · Polytec PolyProperties Type Library · SingleCursorSettings Object : Parent Property*

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

## Position Property

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings~Position.html` · Polytec PolyProperties Type Library · SingleCursorSettings Object : Position Property*

### Description

The position of the line of the single cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Position As Double
```


---

## ShowHorizontalLine Property

*Quelle: `POLYPROPERTIESLib~SingleCursorSettings~ShowHorizontalLine.html` · Polytec PolyProperties Type Library · SingleCursorSettings Object : ShowHorizontalLine Property*

### Description

Specifies whether a horizontal line is shown at the intersection of the cursor line with the data.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowHorizontalLine As Boolean
```
