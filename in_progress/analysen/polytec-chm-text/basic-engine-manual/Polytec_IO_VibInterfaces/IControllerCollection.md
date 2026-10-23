# Polytec_IO_VibInterfaces – IControllerCollection

## IControllerCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~IControllerCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the controllers.

### Object Model


---

## IControllerCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~IControllerCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Add | Adds a controller to the collection. |
|---|---|
| IndexOf | Returns the 0-based index of the given controller of the collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item of the collection with the given index. |


---

## Add Method

*Quelle: `Polytec_IO_VibInterfaces~IControllerCollection~Add.html` · Polytec IO VibInterfaces Type Library · IControllerCollection Collection : Add Method*

### Description

Adds a controller to the collection.

### Syntax

*Visual Basic:*
```
Public Sub Add( _
   ByVal controller As IController _
)
```

### Parameters

controller

The controller to add.


---

## IndexOf Method

*Quelle: `Polytec_IO_VibInterfaces~IControllerCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · IControllerCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given controller of the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal controller As IController _
) As Long
```

### Parameters

controller

The controller to get the index for.

### Remarks

Returns -1 if the given item is not contained in the collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerCollection~Count.html` · Polytec IO VibInterfaces Type Library · IControllerCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IControllerCollection~Item.html` · Polytec IO VibInterfaces Type Library · IControllerCollection Collection : Item Property*

### Description

Returns the item of the collection with the given index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Long _
) As IController
```

### Parameters

index

The 0-based index of the item.
