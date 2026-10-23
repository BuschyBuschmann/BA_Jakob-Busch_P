# POLYALIGNMENTLib – IAlignments3D

## IAlignments3D Collection

*Quelle: `POLYALIGNMENTLib~IAlignments3D.html` · Polytec PolyAlignment Type Library*

### Description

Collection of Alignment3D objects.

### Object Model

### Remarks

It is recommended to cast to the Alignments3D collection.


---

## IAlignments3D Collection Members

*Quelle: `POLYALIGNMENTLib~IAlignments3D_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Add | Adds a new Alignment3D to the collection and returns it. |
|---|---|
| Clear | Removes all items from the collection. |
| Remove | Removes an item from the collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an item of the collection. |


---

## Add Method

*Quelle: `POLYALIGNMENTLib~IAlignments3D~Add.html` · Polytec PolyAlignment Type Library · IAlignments3D Collection : Add Method*

### Description

Adds a new Alignment3D to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As IAlignment3D
```


---

## Clear Method

*Quelle: `POLYALIGNMENTLib~IAlignments3D~Clear.html` · Polytec PolyAlignment Type Library · IAlignments3D Collection : Clear Method*

### Description

Removes all items from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Remove Method

*Quelle: `POLYALIGNMENTLib~IAlignments3D~Remove.html` · Polytec PolyAlignment Type Library · IAlignments3D Collection : Remove Method*

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

The index of the item.


---

## Count Property

*Quelle: `POLYALIGNMENTLib~IAlignments3D~Count.html` · Polytec PolyAlignment Type Library · IAlignments3D Collection : Count Property*

### Description

The number of items in the collection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYALIGNMENTLib~IAlignments3D~Item.html` · Polytec PolyAlignment Type Library · IAlignments3D Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal lIndex As Long _
) As IAlignment3D
```

### Parameters

lIndex

The index of the item.
