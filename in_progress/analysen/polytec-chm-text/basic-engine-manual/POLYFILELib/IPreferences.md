# POLYFILELib – IPreferences

## IPreferences Collection

*Quelle: `POLYFILELib~IPreferences.html` · Polytec PolyFile Type Library*

### Description

IPreferences Interface

### Object Model

### Remarks

It it is recommended to cast to the Preferences Collection.


---

## IPreferences Collection Members

*Quelle: `POLYFILELib~IPreferences_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Count | Returns the number of items in the Preferences collection. |
|---|---|
| Exists | Returns True if the item exists in the collection. |
| Item | Returns an item of the collection. |
| Type | Returns an item of the collection. |


---

## Count Property

*Quelle: `POLYFILELib~IPreferences~Count.html` · Polytec PolyFile Type Library · IPreferences Collection : Count Property*

### Description

Returns the number of items in the Preferences collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `POLYFILELib~IPreferences~Exists.html` · Polytec PolyFile Type Library · IPreferences Collection : Exists Property*

### Description

Returns True if the item exists in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal IndexOrType As Variant _
) As Boolean
```

### Parameters

IndexOrType

Name (string) or type (PTCPrefType) of the item.


---

## Item Property

*Quelle: `POLYFILELib~IPreferences~Item.html` · Polytec PolyFile Type Library · IPreferences Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal IndexOrName As Variant _
) As IPref
```

### Parameters

IndexOrName

Name (string) or index (integer) of the item


---

## Type Property

*Quelle: `POLYFILELib~IPreferences~Type.html` · Polytec PolyFile Type Library · IPreferences Collection : Type Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type( _
   ByVal ptcPrefType As PTCPrefType _
) As IPref
```

### Parameters

ptcPrefType

| Value | Description |
|---|---|
| ptcPrefDbReferences | DbReferences |
| ptcPrefNone | This type is not used. |
The type of preferences.
