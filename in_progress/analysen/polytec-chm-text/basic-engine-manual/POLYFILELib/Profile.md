# POLYFILELib – Profile

## Profile Object

*Quelle: `POLYFILELib~Profile.html` · Polytec PolyFile Type Library*

### Description

Item of the Profiles collection.


---

## Profile Object Members

*Quelle: `POLYFILELib~Profile_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Save | Saves the Profile in the underlying file if its modified. |
|---|---|

### Public Properties

| Color | Returns the Color code. |
|---|---|
| FileIndex | Returns the file index of the profile. |
| Lines | Returns the x- and y-coordinates of the profile in video units. |
| LineStyle | Returns the line style. |
| MarkerStyle | Returns the marker style. |
| Type | Returns the type of the Profile object. |


---

## Save Method

*Quelle: `POLYFILELib~Profile~Save.html` · Polytec PolyFile Type Library · Profile Object : Save Method*

### Description

Saves the Profile in the underlying file if its modified.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## Color Property

*Quelle: `POLYFILELib~Profile~Color.html` · Polytec PolyFile Type Library · Profile Object : Color Property*

### Description

Returns the Color code.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Color As ULong
```


---

## FileIndex Property

*Quelle: `POLYFILELib~Profile~FileIndex.html` · Polytec PolyFile Type Library · Profile Object : FileIndex Property*

### Description

Returns the file index of the profile.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FileIndex As Long
```

### Remarks

The file index is used to distinguish between profiles of different contained files in a combined file.


---

## Lines Property

*Quelle: `POLYFILELib~Profile~Lines.html` · Polytec PolyFile Type Library · Profile Object : Lines Property*

### Description

Returns the x- and y-coordinates of the profile in video units.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Lines As Single()
```

### Return Type

0-based, one dimensional array of float values. The x- and y-coordinates are stored alternating in the array.


---

## LineStyle Property

*Quelle: `POLYFILELib~Profile~LineStyle.html` · Polytec PolyFile Type Library · Profile Object : LineStyle Property*

### Description

Returns the line style.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LineStyle As Long
```


---

## MarkerStyle Property

*Quelle: `POLYFILELib~Profile~MarkerStyle.html` · Polytec PolyFile Type Library · Profile Object : MarkerStyle Property*

### Description

Returns the marker style.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MarkerStyle As Long
```


---

## Type Property

*Quelle: `POLYFILELib~Profile~Type.html` · Polytec PolyFile Type Library · Profile Object : Type Property*

### Description

Returns the type of the Profile object.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCProfileType
```
