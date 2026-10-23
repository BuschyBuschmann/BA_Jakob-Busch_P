# Polytec_IO_VibInterfaces – IBaseFilterRangeCollection

## IBaseFilterRangeCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~IBaseFilterRangeCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the filter ranges of a filter.

### Object Model


---

## IBaseFilterRangeCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~IBaseFilterRangeCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Contains | Returns true, if the collection contains an item with the given name. |
|---|---|

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item of the collection with the given name or index. |


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~IBaseFilterRangeCollection~Contains.html` · Polytec IO VibInterfaces Type Library · IBaseFilterRangeCollection Collection : Contains Method*

### Description

Returns true, if the collection contains an item with the given name.

### Syntax

*Visual Basic:*
```
Public Function Contains( _
   ByVal index As Variant _
) As Boolean
```

### Parameters

index

The name of the item.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~IBaseFilterRangeCollection~Count.html` · Polytec IO VibInterfaces Type Library · IBaseFilterRangeCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IBaseFilterRangeCollection~Item.html` · Polytec IO VibInterfaces Type Library · IBaseFilterRangeCollection Collection : Item Property*

### Description

Returns the item of the collection with the given name or index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As IBaseFilterRange
```

### Parameters

index

The name or 0-based index of the item.
