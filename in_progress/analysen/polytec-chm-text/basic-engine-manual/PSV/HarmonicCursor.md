# PSV – HarmonicCursor

## HarmonicCursor Object

*Quelle: `PSV~HarmonicCursor.html` · Polytec PSV Type Library*

### Description

Object representing the current values of the harmonic cursor. Derived from BaseCursor.


---

## HarmonicCursor Object Members

*Quelle: `PSV~HarmonicCursor_members.html` · Polytec PSV Type Library*

### Public Properties

| CursorType | The type of the cursor. |
|---|---|
| Positions | Returns an array with the current positions of the cursor lines on the x-axis. |
| Values | Returns an array with the data values at the current position of the cursor lines. |


---

## CursorType Property

*Quelle: `PSV~HarmonicCursor~CursorType.html` · Polytec PSV Type Library · HarmonicCursor Object : CursorType Property*

### Description

The type of the cursor.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CursorType As PTCCursorType
```

### Return Type

Always ptcCursorTypeHarmonic.


---

## Positions Property

*Quelle: `PSV~HarmonicCursor~Positions.html` · Polytec PSV Type Library · HarmonicCursor Object : Positions Property*

### Description

Returns an array with the current positions of the cursor lines on the x-axis.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Positions As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the number of cursor lines.


---

## Values Property

*Quelle: `PSV~HarmonicCursor~Values.html` · Polytec PSV Type Library · HarmonicCursor Object : Values Property*

### Description

Returns an array with the data values at the current position of the cursor lines.

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

The number of values depends on the number of cursor lines and the display type of the analyzer view (1 graph or 2 graph display). The values are returned line by line, alternating for the graphs.
