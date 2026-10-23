# POLYPROPERTIESLib – LineSettingsColl

## LineSettingsColl Collection

*Quelle: `POLYPROPERTIESLib~LineSettingsColl.html` · Polytec PolyProperties Type Library*

### Description

Collection of LineSettings objects.

### Object Model


---

## LineSettingsColl Collection Members

*Quelle: `POLYPROPERTIESLib~LineSettingsColl_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item of the collection with the given index. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~LineSettingsColl~Clone.html` · Polytec PolyProperties Type Library · LineSettingsColl Collection : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~LineSettingsColl~Copy.html` · Polytec PolyProperties Type Library · LineSettingsColl Collection : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~LineSettingsColl~Equal.html` · Polytec PolyProperties Type Library · LineSettingsColl Collection : Equal Method*

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

## Count Property

*Quelle: `POLYPROPERTIESLib~LineSettingsColl~Count.html` · Polytec PolyProperties Type Library · LineSettingsColl Collection : Count Property*

### Description

The number of items in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYPROPERTIESLib~LineSettingsColl~Item.html` · Polytec PolyProperties Type Library · LineSettingsColl Collection : Item Property*

### Description

Returns the item of the collection with the given index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Long _
) As LineSettings
```

### Parameters

Index

The index of the item.


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~LineSettingsColl~Modified.html` · Polytec PolyProperties Type Library · LineSettingsColl Collection : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~LineSettingsColl~Parent.html` · Polytec PolyProperties Type Library · LineSettingsColl Collection : Parent Property*

### Description

The parent of the settings object, if the object is attached, or nothing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Parent As Object
```
