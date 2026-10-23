# POLYSIGNALLib – IChannels2

## IChannels2 Collection

*Quelle: `POLYSIGNALLib~IChannels2.html` · Polytec PolySignal Type Library*

### Description

Named collection of the available channels for a given domain.

### Object Model

### Remarks

It is recommended to cast to the Channels collection.


---

## IChannels2 Collection Members

*Quelle: `POLYSIGNALLib~IChannels2_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Exists | Returns true if the item of the given name exists in the collection. |
| Item | Returns an item of the collection. |


---

## Count Property

*Quelle: `POLYSIGNALLib~IChannels2~Count.html` · Polytec PolySignal Type Library · IChannels2 Collection : Count Property*

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

*Quelle: `POLYSIGNALLib~IChannels2~Exists.html` · Polytec PolySignal Type Library · IChannels2 Collection : Exists Property*

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

*Quelle: `POLYSIGNALLib~IChannels2~Item.html` · Polytec PolySignal Type Library · IChannels2 Collection : Item Property*

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
