# POLYFILELib – Preferences

## Preferences Collection

*Quelle: `POLYFILELib~Preferences.html` · Polytec PolyFile Type Library*

### Description

Preferences is a named and typed collection holding items of different type.

### Object Model


---

## Preferences Collection Members

*Quelle: `POLYFILELib~Preferences_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Count | Returns the number of items in the Preferences collection. |
|---|---|
| DbReferences | Returns the DbReferences item of the collection. |
| Exists | Returns True if the item exists in the collection. |
| HasDbReferences | Returns whether the collection has a DbReferences item. |
| Item | Returns an item of the collection. |
| Type | Returns an item of the collection. |


---

## Count Property

*Quelle: `POLYFILELib~Preferences~Count.html` · Polytec PolyFile Type Library · Preferences Collection : Count Property*

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

## DbReferences Property

*Quelle: `POLYFILELib~Preferences~DbReferences.html` · Polytec PolyFile Type Library · Preferences Collection : DbReferences Property*

### Description

Returns the DbReferences item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DbReferences As DbReferences
```

### Return Type

The DbReferences item.


---

## Exists Property

*Quelle: `POLYFILELib~Preferences~Exists.html` · Polytec PolyFile Type Library · Preferences Collection : Exists Property*

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

## HasDbReferences Property

*Quelle: `POLYFILELib~Preferences~HasDbReferences.html` · Polytec PolyFile Type Library · Preferences Collection : HasDbReferences Property*

### Description

Returns whether the collection has a DbReferences item.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasDbReferences As Boolean
```

### Return Type

True when the collection has a DbReferences item.


---

## Item Property

*Quelle: `POLYFILELib~Preferences~Item.html` · Polytec PolyFile Type Library · Preferences Collection : Item Property*

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

*Quelle: `POLYFILELib~Preferences~Type.html` · Polytec PolyFile Type Library · Preferences Collection : Type Property*

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
