# PSV – SingleCursor

## SingleCursor Object

*Quelle: `PSV~SingleCursor.html` · Polytec PSV Type Library*

### Description

Object representing the current values of the single cursor. Derived from the DataCursor Object.


---

## SingleCursor Object Members

*Quelle: `PSV~SingleCursor_members.html` · Polytec PSV Type Library*

### Public Properties

| CursorType | The type of the data cursor. |
|---|---|
| Values | Returns an array with the data values at the current cursor position. |


---

## CursorType Property

*Quelle: `PSV~SingleCursor~CursorType.html` · Polytec PSV Type Library · SingleCursor Object : CursorType Property*

### Description

The type of the data cursor.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CursorType As PTCCursorType
```

### Remarks

Always ptcCursorTypeSingle.


---

## Values Property

*Quelle: `PSV~SingleCursor~Values.html` · Polytec PSV Type Library · SingleCursor Object : Values Property*

### Description

Returns an array with the data values at the current cursor position.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Values As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display).
