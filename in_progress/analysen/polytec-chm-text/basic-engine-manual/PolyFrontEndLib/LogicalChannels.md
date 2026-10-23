# PolyFrontEndLib – LogicalChannels

## LogicalChannels Collection

*Quelle: `PolyFrontEndLib~LogicalChannels.html` · Polytec PolyFrontEnd Type Library*

### Description

Named collection of the available logical channels of the front-end.

### Object Model


---

## LogicalChannels Collection Members

*Quelle: `PolyFrontEndLib~LogicalChannels_members.html` · Polytec PolyFrontEnd Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Exists | Returns true if the item with the given name exists in the collection. |
| Item | Returns the item with the given index or name of the collection. |


---

## Count Property

*Quelle: `PolyFrontEndLib~LogicalChannels~Count.html` · Polytec PolyFrontEnd Type Library · LogicalChannels Collection : Count Property*

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

## Exists Property

*Quelle: `PolyFrontEndLib~LogicalChannels~Exists.html` · Polytec PolyFrontEnd Type Library · LogicalChannels Collection : Exists Property*

### Description

Returns true if the item with the given name exists in the collection.

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

*Quelle: `PolyFrontEndLib~LogicalChannels~Item.html` · Polytec PolyFrontEnd Type Library · LogicalChannels Collection : Item Property*

### Description

Returns the item with the given index or name of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As LogicalChannel
```

### Parameters

Index

The index or name of the item.
