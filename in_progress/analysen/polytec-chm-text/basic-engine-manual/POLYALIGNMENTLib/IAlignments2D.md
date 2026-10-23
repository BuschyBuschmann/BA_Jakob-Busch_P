# POLYALIGNMENTLib – IAlignments2D

## IAlignments2D Collection

*Quelle: `POLYALIGNMENTLib~IAlignments2D.html` · Polytec PolyAlignment Type Library*

### Description

Collection of Alignment2D objects.

### Object Model

### Remarks

It is recommended to cast to the Alignments2D collection.


---

## IAlignments2D Collection Members

*Quelle: `POLYALIGNMENTLib~IAlignments2D_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Add | Adds a new Alignment2D to the collection and returns it. |
|---|---|
| Clear | Removes all items from the collection. |
| Remove | Removes an item from the collection. |

### Public Properties

| Count | The number of items in this collection. |
|---|---|
| Item | Returns an item of the collection. |


---

## Add Method

*Quelle: `POLYALIGNMENTLib~IAlignments2D~Add.html` · Polytec PolyAlignment Type Library · IAlignments2D Collection : Add Method*

### Description

Adds a new Alignment2D to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As IAlignment2D
```


---

## Clear Method

*Quelle: `POLYALIGNMENTLib~IAlignments2D~Clear.html` · Polytec PolyAlignment Type Library · IAlignments2D Collection : Clear Method*

### Description

Removes all items from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Remove Method

*Quelle: `POLYALIGNMENTLib~IAlignments2D~Remove.html` · Polytec PolyAlignment Type Library · IAlignments2D Collection : Remove Method*

### Description

Removes an item from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal lIndex As Long _
)
```

### Parameters

lIndex

Index of the item.


---

## Count Property

*Quelle: `POLYALIGNMENTLib~IAlignments2D~Count.html` · Polytec PolyAlignment Type Library · IAlignments2D Collection : Count Property*

### Description

The number of items in this collection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYALIGNMENTLib~IAlignments2D~Item.html` · Polytec PolyAlignment Type Library · IAlignments2D Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal lIndex As Long _
) As IAlignment2D
```

### Parameters

lIndex

The index of the item.
