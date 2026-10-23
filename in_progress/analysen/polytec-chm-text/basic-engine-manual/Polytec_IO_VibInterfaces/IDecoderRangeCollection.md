# Polytec_IO_VibInterfaces – IDecoderRangeCollection

## IDecoderRangeCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRangeCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the decoder ranges.

### Object Model


---

## IDecoderRangeCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRangeCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Contains | Returns true, if the collection contains an item with the given name. |
|---|---|
| IndexOf | Returns the 0-based index of the given item in the collection. |
| IsEqual | Returns true, if the given decoder ranges collection is equal to this collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an item of the collection with the given name or index. |


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRangeCollection~Contains.html` · Polytec IO VibInterfaces Type Library · IDecoderRangeCollection Collection : Contains Method*

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

## IndexOf Method

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRangeCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · IDecoderRangeCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item in the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal decoderRange As IDecoderRange _
) As Long
```

### Parameters

decoderRange

The item of the collection.

### Remarks

The method returns -1 if the item is not contained in the collection.


---

## IsEqual Method

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRangeCollection~IsEqual.html` · Polytec IO VibInterfaces Type Library · IDecoderRangeCollection Collection : IsEqual Method*

### Description

Returns true, if the given decoder ranges collection is equal to this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal decoderRanges As IDecoderRangeCollection _
) As Boolean
```

### Parameters

decoderRanges

The other decoder ranges collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRangeCollection~Count.html` · Polytec IO VibInterfaces Type Library · IDecoderRangeCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRangeCollection~Item.html` · Polytec IO VibInterfaces Type Library · IDecoderRangeCollection Collection : Item Property*

### Description

Returns an item of the collection with the given name or index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As IDecoderRange
```

### Parameters

index

The name or 0-based index of the item.
