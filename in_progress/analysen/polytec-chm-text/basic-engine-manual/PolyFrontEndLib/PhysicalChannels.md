# PolyFrontEndLib – PhysicalChannels

## PhysicalChannels Collection

*Quelle: `PolyFrontEndLib~PhysicalChannels.html` · Polytec PolyFrontEnd Type Library*

### Description

Named collection of the available physical channels of the front-end.

### Object Model


---

## PhysicalChannels Collection Members

*Quelle: `PolyFrontEndLib~PhysicalChannels_members.html` · Polytec PolyFrontEnd Type Library*

### Public Properties

| Count | The number of items of the collection. |
|---|---|
| Exists | Returns true, if an item with the given name exists in the collection. |
| Item | Returns the item with the given name or index of the collection. |


---

## Count Property

*Quelle: `PolyFrontEndLib~PhysicalChannels~Count.html` · Polytec PolyFrontEnd Type Library · PhysicalChannels Collection : Count Property*

### Description

The number of items of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `PolyFrontEndLib~PhysicalChannels~Exists.html` · Polytec PolyFrontEnd Type Library · PhysicalChannels Collection : Exists Property*

### Description

Returns true, if an item with the given name exists in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal Index As Variant _
) As Boolean
```

### Parameters

Index

The name of the item.


---

## Item Property

*Quelle: `PolyFrontEndLib~PhysicalChannels~Item.html` · Polytec PolyFrontEnd Type Library · PhysicalChannels Collection : Item Property*

### Description

Returns the item with the given name or index of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As PhysicalChannel
```

### Parameters

Index

The name or index of the item.
