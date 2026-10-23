# Polytec_IO_VibInterfaces – DecoderClearModeCollection

## DecoderClearModeCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~DecoderClearModeCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the decoder clear modes the controller supports.

### Object Model


---

## DecoderClearModeCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~DecoderClearModeCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Contains | Returns true, if the item with the given name or index is contained in the collection. |
|---|---|
| IndexOf | Returns the 0-based index of the given item of the collection. |
| IsEqual | Checks whether this collection is equal to the specified collection. |

### Public Properties

| Count | The number of items of the collection. |
|---|---|
| Item | Returns the item of the collection with the given index or name. |


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~DecoderClearModeCollection~Contains.html` · Polytec IO VibInterfaces Type Library · DecoderClearModeCollection Collection : Contains Method*

### Description

Returns true, if the item with the given name or index is contained in the collection.

### Syntax

*Visual Basic:*
```
Public Function Contains( _
   ByVal index As Variant _
) As Boolean
```

### Parameters

index

The name or index of the decoder clear mode.


---

## IndexOf Method

*Quelle: `Polytec_IO_VibInterfaces~DecoderClearModeCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · DecoderClearModeCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item of the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal decoderClearModeObj As DecoderClearMode _
) As Long
```

### Parameters

decoderClearModeObj

The item of the collection.


---

## IsEqual Method

*Quelle: `Polytec_IO_VibInterfaces~DecoderClearModeCollection~IsEqual.html` · Polytec IO VibInterfaces Type Library · DecoderClearModeCollection Collection : IsEqual Method*

### Description

Checks whether this collection is equal to the specified collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal decoderClearModeList As DecoderClearModeCollection _
) As Boolean
```

### Parameters

decoderClearModeList

The other decoder clear mode collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~DecoderClearModeCollection~Count.html` · Polytec IO VibInterfaces Type Library · DecoderClearModeCollection Collection : Count Property*

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

## Item Property

*Quelle: `Polytec_IO_VibInterfaces~DecoderClearModeCollection~Item.html` · Polytec IO VibInterfaces Type Library · DecoderClearModeCollection Collection : Item Property*

### Description

Returns the item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As DecoderClearMode
```

### Parameters

index

The 0-based index or name of the item.
