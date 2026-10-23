# POLYPROPERTIESLib – DoubleCursorSettings

## DoubleCursorSettings Object

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings of the double cursor.

### Object Model


---

## DoubleCursorSettings Object Members

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| CursorType | The type of the cursor. |
|---|---|
| LeftPosition | The position of the left line of the double cursor. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| RightPosition | The position of the right line of the double cursor. |
| ShowDampedSineFitCurve | Specifies, whether a damped sine fit curve is show for time traces.. |
| ShowDampedSineFitParameters | Specifies whether the parameters for the damped sine fit to a time trace are shown in the readout of the analyzer. |
| ShowHorizontalLine | Specifies, whether a horizontal line is shown at the intersection of the cursor lines and the data. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~Clone.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~Copy.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~Equal.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : Equal Method*

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

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~CursorType.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : CursorType Property*

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

Always ptcCursorTypeDouble.


---

## LeftPosition Property

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~LeftPosition.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : LeftPosition Property*

### Description

The position of the left line of the double cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LeftPosition As Double
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~Modified.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~Parent.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : Parent Property*

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

## RightPosition Property

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~RightPosition.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : RightPosition Property*

### Description

The position of the right line of the double cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RightPosition As Double
```


---

## ShowDampedSineFitCurve Property

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~ShowDampedSineFitCurve.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : ShowDampedSineFitCurve Property*

### Description

Specifies, whether a damped sine fit curve is show for time traces..

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowDampedSineFitCurve As Boolean
```


---

## ShowDampedSineFitParameters Property

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~ShowDampedSineFitParameters.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : ShowDampedSineFitParameters Property*

### Description

Specifies whether the parameters for the damped sine fit to a time trace are shown in the readout of the analyzer.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowDampedSineFitParameters As Boolean
```


---

## ShowHorizontalLine Property

*Quelle: `POLYPROPERTIESLib~DoubleCursorSettings~ShowHorizontalLine.html` · Polytec PolyProperties Type Library · DoubleCursorSettings Object : ShowHorizontalLine Property*

### Description

Specifies, whether a horizontal line is shown at the intersection of the cursor lines and the data.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowHorizontalLine As Boolean
```
