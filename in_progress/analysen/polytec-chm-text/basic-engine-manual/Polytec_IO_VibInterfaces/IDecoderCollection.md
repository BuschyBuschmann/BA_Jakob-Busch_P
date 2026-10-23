# Polytec_IO_VibInterfaces – IDecoderCollection

## IDecoderCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~IDecoderCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the decoders of the vibrometer controller.

### Object Model


---

## IDecoderCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~IDecoderCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Contains | Returns true, if the collection contains a decoder with the given name. |
|---|---|
| IndexOf | Returns the 0-based index of the given item of the collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | The item of the collection with the given index or name. |


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~IDecoderCollection~Contains.html` · Polytec IO VibInterfaces Type Library · IDecoderCollection Collection : Contains Method*

### Description

Returns true, if the collection contains a decoder with the given name.

### Syntax

*Visual Basic:*
```
Public Function Contains( _
   ByVal index As Variant _
) As Boolean
```

### Parameters

index

The name of the decoder.


---

## IndexOf Method

*Quelle: `Polytec_IO_VibInterfaces~IDecoderCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · IDecoderCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item of the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal decoderObj As IDecoder _
) As Long
```

### Parameters

decoderObj

The decoder to get the index for.

### Remarks

Returns -1 if the item is not contained in the collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderCollection~Count.html` · Polytec IO VibInterfaces Type Library · IDecoderCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IDecoderCollection~Item.html` · Polytec IO VibInterfaces Type Library · IDecoderCollection Collection : Item Property*

### Description

The item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As IDecoder
```

### Parameters

index

The 0-based index or name of the item.
