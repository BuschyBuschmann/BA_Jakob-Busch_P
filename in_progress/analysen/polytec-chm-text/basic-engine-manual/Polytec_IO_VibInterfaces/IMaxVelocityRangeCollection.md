# Polytec_IO_VibInterfaces – IMaxVelocityRangeCollection

## IMaxVelocityRangeCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~IMaxVelocityRangeCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the maximum velocity ranges of the decoder.

### Object Model


---

## IMaxVelocityRangeCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~IMaxVelocityRangeCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Contains | Returns true, if the collection contains an item with the given name. |
|---|---|
| IndexOf | Returns the 0-based index of the given item in the collection. |
| IsEqual | Returns true, if the given maximum velocity range collection is equal to this collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an item of the collection with the given name or index. |


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~IMaxVelocityRangeCollection~Contains.html` · Polytec IO VibInterfaces Type Library · IMaxVelocityRangeCollection Collection : Contains Method*

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

*Quelle: `Polytec_IO_VibInterfaces~IMaxVelocityRangeCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · IMaxVelocityRangeCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item in the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal maxVelocityRangeObj As IMaxVelocityRange _
) As Long
```

### Parameters

maxVelocityRangeObj

The item of the collection.

### Remarks

The method returns -1 if the item is not contained in the collection.


---

## IsEqual Method

*Quelle: `Polytec_IO_VibInterfaces~IMaxVelocityRangeCollection~IsEqual.html` · Polytec IO VibInterfaces Type Library · IMaxVelocityRangeCollection Collection : IsEqual Method*

### Description

Returns true, if the given maximum velocity range collection is equal to this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal maxVelocityRangeList As IMaxVelocityRangeCollection _
) As Boolean
```

### Parameters

maxVelocityRangeList

The other maximum velocity range collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~IMaxVelocityRangeCollection~Count.html` · Polytec IO VibInterfaces Type Library · IMaxVelocityRangeCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IMaxVelocityRangeCollection~Item.html` · Polytec IO VibInterfaces Type Library · IMaxVelocityRangeCollection Collection : Item Property*

### Description

Returns an item of the collection with the given name or index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As IMaxVelocityRange
```

### Parameters

index

The name or 0-based index of the item.
