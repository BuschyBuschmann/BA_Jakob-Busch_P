# POLYPROPERTIESLib – HarmonicCursorSettings

## HarmonicCursorSettings Object

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings of the harmonic cursor.

### Object Model


---

## HarmonicCursorSettings Object Members

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| CursorType | The type of the data cursor. |
|---|---|
| Modified | Returns whether the settings object has been modified. |
| NumberOfLines | The number of lines of the harmonic cursor. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Position | The position of the left-most line of the harmonic cursor. |
| ShowHorizontalLine | Specifies, whether a horizontal line is shown at the intersection of the cursor lines and the data. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings~Clone.html` · Polytec PolyProperties Type Library · HarmonicCursorSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings~Copy.html` · Polytec PolyProperties Type Library · HarmonicCursorSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings~Equal.html` · Polytec PolyProperties Type Library · HarmonicCursorSettings Object : Equal Method*

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

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings~CursorType.html` · Polytec PolyProperties Type Library · HarmonicCursorSettings Object : CursorType Property*

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

Always ptcCursorTypeHarmonic.


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings~Modified.html` · Polytec PolyProperties Type Library · HarmonicCursorSettings Object : Modified Property*

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

## NumberOfLines Property

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings~NumberOfLines.html` · Polytec PolyProperties Type Library · HarmonicCursorSettings Object : NumberOfLines Property*

### Description

The number of lines of the harmonic cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property NumberOfLines As Long
```

### Remarks

The number of lines is limited to the range of 2 to 12.


---

## Parent Property

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings~Parent.html` · Polytec PolyProperties Type Library · HarmonicCursorSettings Object : Parent Property*

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

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings~Position.html` · Polytec PolyProperties Type Library · HarmonicCursorSettings Object : Position Property*

### Description

The position of the left-most line of the harmonic cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Position As Double
```


---

## ShowHorizontalLine Property

*Quelle: `POLYPROPERTIESLib~HarmonicCursorSettings~ShowHorizontalLine.html` · Polytec PolyProperties Type Library · HarmonicCursorSettings Object : ShowHorizontalLine Property*

### Description

Specifies, whether a horizontal line is shown at the intersection of the cursor lines and the data.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowHorizontalLine As Boolean
```
