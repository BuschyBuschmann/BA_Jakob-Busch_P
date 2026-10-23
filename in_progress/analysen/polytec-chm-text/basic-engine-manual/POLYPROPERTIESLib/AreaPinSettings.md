# POLYPROPERTIESLib – AreaPinSettings

## AreaPinSettings Object

*Quelle: `POLYPROPERTIESLib~AreaPinSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings for pinning area view settings to other open area views.

### Object Model


---

## AreaPinSettings Object Members

*Quelle: `POLYPROPERTIESLib~AreaPinSettings_members.html` · Polytec PolyProperties Type Library*

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

*Quelle: `POLYPROPERTIESLib~AreaPinSettings~Clone.html` · Polytec PolyProperties Type Library · AreaPinSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~AreaPinSettings~Copy.html` · Polytec PolyProperties Type Library · AreaPinSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~AreaPinSettings~Equal.html` · Polytec PolyProperties Type Library · AreaPinSettings Object : Equal Method*

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

*Quelle: `POLYPROPERTIESLib~AreaPinSettings~Cursor.html` · Polytec PolyProperties Type Library · AreaPinSettings Object : Cursor Property*

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

*Quelle: `POLYPROPERTIESLib~AreaPinSettings~General.html` · Polytec PolyProperties Type Library · AreaPinSettings Object : General Property*

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

*Quelle: `POLYPROPERTIESLib~AreaPinSettings~Modified.html` · Polytec PolyProperties Type Library · AreaPinSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~AreaPinSettings~Parent.html` · Polytec PolyProperties Type Library · AreaPinSettings Object : Parent Property*

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

*Quelle: `POLYPROPERTIESLib~AreaPinSettings~Signal.html` · Polytec PolyProperties Type Library · AreaPinSettings Object : Signal Property*

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

*Quelle: `POLYPROPERTIESLib~AreaPinSettings~View.html` · Polytec PolyProperties Type Library · AreaPinSettings Object : View Property*

### Description

Specifies whether the view settings of the area view should be pinned to other area views.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property View As Boolean
```
