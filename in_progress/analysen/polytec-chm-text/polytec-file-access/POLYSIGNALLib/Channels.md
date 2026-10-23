# POLYSIGNALLib – Channels

## Channels Collection

*Quelle: `POLYSIGNALLib~Channels.html` · Polytec PolySignal Type Library*

### Description

Named collection of the available channels for a given domain.

### Object Model


---

## Channels Collection Members

*Quelle: `POLYSIGNALLib~Channels_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Exists | Returns true if the item of the given name exists in the collection. |
| Item | Returns an item of the collection. |


---

## Count Property

*Quelle: `POLYSIGNALLib~Channels~Count.html` · Polytec PolySignal Type Library · Channels Collection : Count Property*

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

*Quelle: `POLYSIGNALLib~Channels~Exists.html` · Polytec PolySignal Type Library · Channels Collection : Exists Property*

### Description

Returns true if the item of the given name exists in the collection.

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

Name of the item.


---

## Item Property

*Quelle: `POLYSIGNALLib~Channels~Item.html` · Polytec PolySignal Type Library · Channels Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As Channel
```

### Parameters

Index

Index or name of the item.
