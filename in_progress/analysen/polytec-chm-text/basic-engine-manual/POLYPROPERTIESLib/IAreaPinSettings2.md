# POLYPROPERTIESLib – IAreaPinSettings2

## IAreaPinSettings2 Interface

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2.html` · Polytec PolyProperties Type Library*

### Description

The settings for pinning area view settings to other open area views.

### Object Model

### Remarks

It is recommended to cast to the AreaPinSettings Object.


---

## IAreaPinSettings2 Interface Members

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Cursor | Specifies whether the cursor settings of the area view should be pinned to other area views. |
|---|---|
| General | Specifies whether the general settings of the area view should be pinned to other area views. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Signal | Specifies whether the signal settings of the area view should be pinned to other area views. |
| View | Specifies whether the view settings of the area view should be pinned to other area views. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2~Clone.html` · Polytec PolyProperties Type Library · IAreaPinSettings2 Interface : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2~Copy.html` · Polytec PolyProperties Type Library · IAreaPinSettings2 Interface : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2~Equal.html` · Polytec PolyProperties Type Library · IAreaPinSettings2 Interface : Equal Method*

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

## Cursor Property

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2~Cursor.html` · Polytec PolyProperties Type Library · IAreaPinSettings2 Interface : Cursor Property*

### Description

Specifies whether the cursor settings of the area view should be pinned to other area views.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Cursor As Boolean
```


---

## General Property

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2~General.html` · Polytec PolyProperties Type Library · IAreaPinSettings2 Interface : General Property*

### Description

Specifies whether the general settings of the area view should be pinned to other area views.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property General As Boolean
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2~Modified.html` · Polytec PolyProperties Type Library · IAreaPinSettings2 Interface : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2~Parent.html` · Polytec PolyProperties Type Library · IAreaPinSettings2 Interface : Parent Property*

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

## Signal Property

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2~Signal.html` · Polytec PolyProperties Type Library · IAreaPinSettings2 Interface : Signal Property*

### Description

Specifies whether the signal settings of the area view should be pinned to other area views.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Signal As Boolean
```


---

## View Property

*Quelle: `POLYPROPERTIESLib~IAreaPinSettings2~View.html` · Polytec PolyProperties Type Library · IAreaPinSettings2 Interface : View Property*

### Description

Specifies whether the view settings of the area view should be pinned to other area views.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property View As Boolean
```
