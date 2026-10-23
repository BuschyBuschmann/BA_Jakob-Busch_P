# Polytec_IO_VibInterfaces – IBandwidthRangeCollection

## IBandwidthRangeCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~IBandwidthRangeCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the bandwidth ranges of the decoder.

### Object Model


---

## IBandwidthRangeCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~IBandwidthRangeCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Contains | Returns true, if the collection contains an item with the given name or index. |
|---|---|
| IndexOf | Returns the 0-based index of the given item in the collection. |
| IsEqual | Returns true, if the given decoder ranges collection is equal to this collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an item of the collection with the given name or index. |


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~IBandwidthRangeCollection~Contains.html` · Polytec IO VibInterfaces Type Library · IBandwidthRangeCollection Collection : Contains Method*

### Description

Returns true, if the collection contains an item with the given name or index.

### Syntax

*Visual Basic:*
```
Public Function Contains( _
   ByVal index As Variant _
) As Boolean
```

### Parameters

index

The name or index of the item.


---

## IndexOf Method

*Quelle: `Polytec_IO_VibInterfaces~IBandwidthRangeCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · IBandwidthRangeCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item in the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal bandwidthRangeObj As IBandwidthRange _
) As Long
```

### Parameters

bandwidthRangeObj

The item of the collection.

### Remarks

The method returns -1 if the item is not contained in the collection.


---

## IsEqual Method

*Quelle: `Polytec_IO_VibInterfaces~IBandwidthRangeCollection~IsEqual.html` · Polytec IO VibInterfaces Type Library · IBandwidthRangeCollection Collection : IsEqual Method*

### Description

Returns true, if the given decoder ranges collection is equal to this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal bandwidthRangeList As IBandwidthRangeCollection _
) As Boolean
```

### Parameters

bandwidthRangeList

The decoder ranges collection to compare with.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~IBandwidthRangeCollection~Count.html` · Polytec IO VibInterfaces Type Library · IBandwidthRangeCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IBandwidthRangeCollection~Item.html` · Polytec IO VibInterfaces Type Library · IBandwidthRangeCollection Collection : Item Property*

### Description

Returns an item of the collection with the given name or index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As IBandwidthRange
```

### Parameters

index

The name or index of the item.
