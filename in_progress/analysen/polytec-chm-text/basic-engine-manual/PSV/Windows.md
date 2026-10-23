# PSV – Windows

## Windows Collection

*Quelle: `PSV~Windows.html` · Polytec PSV Type Library*

### Description

The collection of the windows.

### Object Model


---

## Windows Collection Members

*Quelle: `PSV~Windows_members.html` · Polytec PSV Type Library*

### Public Methods

| Add | Opens a new window. If there is no window specified a new window is created for the active window. |
|---|---|
| Arrange | Arranges all document windows. |
| CloseAll | Closes all windows in the collection. |

### Public Properties

| Count | The number of items of the collection. |
|---|---|
| Item | Returns the item with the given index of the collection. |


---

## Add Method

*Quelle: `PSV~Windows~Add.html` · Polytec PSV Type Library · Windows Collection : Add Method*

### Description

Opens a new window. If there is no window specified a new window is created for the active window.

### Syntax

*Visual Basic:*
```
Public Function Add( _
   Optional ByVal Window As Variant _
) As Window
```

### Parameters

Window

The sibling window of the new window.


---

## Arrange Method

*Quelle: `PSV~Windows~Arrange.html` · Polytec PSV Type Library · Windows Collection : Arrange Method*

### Description

Arranges all document windows.

### Syntax

*Visual Basic:*
```
Public Sub Arrange( _
   ByVal ArrangeStyle As PTCArrangeStyle _
)
```

### Parameters

ArrangeStyle

| Value | Description |
|---|---|
| ptcArrangeCascaded | Cascade the windows. |
| ptcArrangeIcons | Arrange all windows as minimized icons. |
| ptcArrangeTiledHorizontal | Tile the windows horizontally. |
| ptcArrangeTiledVertical | Tile the windows vertically. |
The arrange window style.


---

## CloseAll Method

*Quelle: `PSV~Windows~CloseAll.html` · Polytec PSV Type Library · Windows Collection : CloseAll Method*

### Description

Closes all windows in the collection.

### Syntax

*Visual Basic:*
```
Public Sub CloseAll()
```


---

## Count Property

*Quelle: `PSV~Windows~Count.html` · Polytec PSV Type Library · Windows Collection : Count Property*

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

*Quelle: `PSV~Windows~Item.html` · Polytec PSV Type Library · Windows Collection : Item Property*

### Description

Returns the item with the given index of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal nIndex As Long _
) As Window
```

### Parameters

nIndex

The index of the item.
