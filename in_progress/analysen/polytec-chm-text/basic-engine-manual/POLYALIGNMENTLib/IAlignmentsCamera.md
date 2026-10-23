# POLYALIGNMENTLib – IAlignmentsCamera

## IAlignmentsCamera Collection

*Quelle: `POLYALIGNMENTLib~IAlignmentsCamera.html` · Polytec PolyAlignment Type Library*

### Description

Collection of AlignmentCamera objects.

### Object Model

### Remarks

It is recommended to cast to the AlignmentsCamera collection.


---

## IAlignmentsCamera Collection Members

*Quelle: `POLYALIGNMENTLib~IAlignmentsCamera_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Add | Adds a new AlignmentCamera to the collection and returns it. |
|---|---|
| Clear | Removes all items from the collection. |
| Remove | Removes an item from the collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an item of the collection. |


---

## Add Method

*Quelle: `POLYALIGNMENTLib~IAlignmentsCamera~Add.html` · Polytec PolyAlignment Type Library · IAlignmentsCamera Collection : Add Method*

### Description

Adds a new AlignmentCamera to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As IAlignmentCamera2
```

### Return Type

The added item.


---

## Clear Method

*Quelle: `POLYALIGNMENTLib~IAlignmentsCamera~Clear.html` · Polytec PolyAlignment Type Library · IAlignmentsCamera Collection : Clear Method*

### Description

Removes all items from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Remove Method

*Quelle: `POLYALIGNMENTLib~IAlignmentsCamera~Remove.html` · Polytec PolyAlignment Type Library · IAlignmentsCamera Collection : Remove Method*

### Description

Removes an item from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal indexParam As Long _
)
```

### Parameters

indexParam

The index of the item.


---

## Count Property

*Quelle: `POLYALIGNMENTLib~IAlignmentsCamera~Count.html` · Polytec PolyAlignment Type Library · IAlignmentsCamera Collection : Count Property*

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

*Quelle: `POLYALIGNMENTLib~IAlignmentsCamera~Item.html` · Polytec PolyAlignment Type Library · IAlignmentsCamera Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal indexParam As Long _
) As IAlignmentCamera2
```

### Parameters

indexParam

The index of the item.

### Return Type

The addressed item.
