# POLYSIGNALLib – ISignals

## ISignals Collection

*Quelle: `POLYSIGNALLib~ISignals.html` · Polytec PolySignal Type Library*

### Description

Named collection of the available signals of a Channel.

### Object Model

### Remarks

It is recommended to cast to the Signals collection.


---

## ISignals Collection Members

*Quelle: `POLYSIGNALLib~ISignals_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Exists | Returns true if the item with the given index or name exists in the collection. |
| Item | Returns an item of the collection with the given index or name. |


---

## Count Property

*Quelle: `POLYSIGNALLib~ISignals~Count.html` · Polytec PolySignal Type Library · ISignals Collection : Count Property*

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

*Quelle: `POLYSIGNALLib~ISignals~Exists.html` · Polytec PolySignal Type Library · ISignals Collection : Exists Property*

### Description

Returns true if the item with the given index or name exists in the collection.

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

The index or name of the item.


---

## Item Property

*Quelle: `POLYSIGNALLib~ISignals~Item.html` · Polytec PolySignal Type Library · ISignals Collection : Item Property*

### Description

Returns an item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As ISignal
```

### Parameters

Index

The index or name of the item.
