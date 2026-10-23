# PSV – DoubleCursor

## DoubleCursor Object

*Quelle: `PSV~DoubleCursor.html` · Polytec PSV Type Library*

### Description

Object representing the current values of the double cursor. Derived from DataCursor.


---

## DoubleCursor Object Members

*Quelle: `PSV~DoubleCursor_members.html` · Polytec PSV Type Library*

### Public Properties

| CursorType | The type of the cursor. |
|---|---|
| DampedSineFitDelta | The decay constant of the damped sine curve fitted to a time trace in 1/s. |
| DampedSineFitFrequency | The frequency of the damped sine curve fitted to a time trace in Hz. |
| LeftValues | The array with the data values at the current position of the left cursor line. |
| RightValues | The array with the data values at the current position of the right cursor line. |


---

## CursorType Property

*Quelle: `PSV~DoubleCursor~CursorType.html` · Polytec PSV Type Library · DoubleCursor Object : CursorType Property*

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

Always ptcCursorTypeDouble.


---

## DampedSineFitDelta Property

*Quelle: `PSV~DoubleCursor~DampedSineFitDelta.html` · Polytec PSV Type Library · DoubleCursor Object : DampedSineFitDelta Property*

### Description

The decay constant of the damped sine curve fitted to a time trace in 1/s.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DampedSineFitDelta As Double
```

### Return Type

The decay constant in 1/s.


---

## DampedSineFitFrequency Property

*Quelle: `PSV~DoubleCursor~DampedSineFitFrequency.html` · Polytec PSV Type Library · DoubleCursor Object : DampedSineFitFrequency Property*

### Description

The frequency of the damped sine curve fitted to a time trace in Hz.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DampedSineFitFrequency As Double
```

### Return Type

The frequency of the damped sine fit in Hz.


---

## LeftValues Property

*Quelle: `PSV~DoubleCursor~LeftValues.html` · Polytec PSV Type Library · DoubleCursor Object : LeftValues Property*

### Description

The array with the data values at the current position of the left cursor line.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LeftValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display).


---

## RightValues Property

*Quelle: `PSV~DoubleCursor~RightValues.html` · Polytec PSV Type Library · DoubleCursor Object : RightValues Property*

### Description

The array with the data values at the current position of the right cursor line.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property RightValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display).
