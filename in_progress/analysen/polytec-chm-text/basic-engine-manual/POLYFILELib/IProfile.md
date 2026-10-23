# POLYFILELib – IProfile

## IProfile Interface

*Quelle: `POLYFILELib~IProfile.html` · Polytec PolyFile Type Library*

### Description

Item of the Profiles collection.

### Remarks

It is recommended to cast to the Profile object.


---

## IProfile Interface Members

*Quelle: `POLYFILELib~IProfile_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Save | Saves the Profile in the underlying file if its modified. |
|---|---|

### Public Properties

| Color | Returns the Color code. |
|---|---|
| Lines | Returns the x- and y-coordinates of the profile in video units. |
| Type | Returns the type of the Profile object. |


---

## Save Method

*Quelle: `POLYFILELib~IProfile~Save.html` · Polytec PolyFile Type Library · IProfile Interface : Save Method*

### Description

Saves the Profile in the underlying file if its modified.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## Color Property

*Quelle: `POLYFILELib~IProfile~Color.html` · Polytec PolyFile Type Library · IProfile Interface : Color Property*

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

## Lines Property

*Quelle: `POLYFILELib~IProfile~Lines.html` · Polytec PolyFile Type Library · IProfile Interface : Lines Property*

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

## Type Property

*Quelle: `POLYFILELib~IProfile~Type.html` · Polytec PolyFile Type Library · IProfile Interface : Type Property*

### Description

Returns the type of the Profile object.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCProfileType
```
