# POLYPROPERTIESLib – IDataCursorSettings

## IDataCursorSettings Interface

*Quelle: `POLYPROPERTIESLib~IDataCursorSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings of a data cursor. This interface is implemented by the DoubleCursorSettings object, the HarmonicCursorSettings object, the PeakCursorSettings object and the SingleCursorSettings object.

### Object Model

### Remarks

To access the specific properties of the data cursor, check the CursorType property and cast to the corresponding object.


---

## IDataCursorSettings Interface Members

*Quelle: `POLYPROPERTIESLib~IDataCursorSettings_members.html` · Polytec PolyProperties Type Library*

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


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~IDataCursorSettings~Clone.html` · Polytec PolyProperties Type Library · IDataCursorSettings Interface : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~IDataCursorSettings~Copy.html` · Polytec PolyProperties Type Library · IDataCursorSettings Interface : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~IDataCursorSettings~Equal.html` · Polytec PolyProperties Type Library · IDataCursorSettings Interface : Equal Method*

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

*Quelle: `POLYPROPERTIESLib~IDataCursorSettings~CursorType.html` · Polytec PolyProperties Type Library · IDataCursorSettings Interface : CursorType Property*

### Description

The type of the data cursor.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CursorType As PTCCursorType
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~IDataCursorSettings~Modified.html` · Polytec PolyProperties Type Library · IDataCursorSettings Interface : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~IDataCursorSettings~Parent.html` · Polytec PolyProperties Type Library · IDataCursorSettings Interface : Parent Property*

### Description

The parent of the settings object, if the object is attached, or nothing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Parent As Object
```
