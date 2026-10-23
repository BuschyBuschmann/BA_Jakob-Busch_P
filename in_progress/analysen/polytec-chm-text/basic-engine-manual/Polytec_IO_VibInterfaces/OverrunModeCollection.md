# Polytec_IO_VibInterfaces – OverrunModeCollection

## OverrunModeCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~OverrunModeCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the overrun modes.

### Object Model


---

## OverrunModeCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~OverrunModeCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Contains | Returns true, if the collection contains an item with the given name. |
|---|---|
| IndexOf | Returns the 0-based index of the given item in the collection. |
| IsEqual | Returns true, if the given overrun mode collection is equal to this collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an item of the collection with the given name or index. |


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~OverrunModeCollection~Contains.html` · Polytec IO VibInterfaces Type Library · OverrunModeCollection Collection : Contains Method*

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

*Quelle: `Polytec_IO_VibInterfaces~OverrunModeCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · OverrunModeCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item in the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal overrunModeObj As OverrunMode _
) As Long
```

### Parameters

overrunModeObj

The item of the collection.

### Remarks

The method returns -1 if the item is not contained in the collection.


---

## IsEqual Method

*Quelle: `Polytec_IO_VibInterfaces~OverrunModeCollection~IsEqual.html` · Polytec IO VibInterfaces Type Library · OverrunModeCollection Collection : IsEqual Method*

### Description

Returns true, if the given overrun mode collection is equal to this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal overrunModeList As OverrunModeCollection _
) As Boolean
```

### Parameters

overrunModeList

The other overrun mode collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~OverrunModeCollection~Count.html` · Polytec IO VibInterfaces Type Library · OverrunModeCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~OverrunModeCollection~Item.html` · Polytec IO VibInterfaces Type Library · OverrunModeCollection Collection : Item Property*

### Description

Returns an item of the collection with the given name or index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As OverrunMode
```

### Parameters

index

The name or 0-based index of the item.
