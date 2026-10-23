# PSV – PeakCursor

## PeakCursor Object

*Quelle: `PSV~PeakCursor.html` · Polytec PSV Type Library*

### Description

Object representing the current values of the peak cursor. Derived from DataCursor.


---

## PeakCursor Object Members

*Quelle: `PSV~PeakCursor_members.html` · Polytec PSV Type Library*

### Public Properties

| CursorType | The type of the data cursor. |
|---|---|
| DampingValues | Returns an array with the 3 dB width of the peak curve fitted to the data values between the cursor lines. |
| FMaxValues | Returns an array with the frequency of the maximum of the peak curve fitted to the data values between the cursor lines. |
| LeftValues | Returns an array with the data values at the current position of the left cursor line. |
| MeanValues | Returns an array with the means of the data values between the cursor lines. |
| QFactorValues | Returns an array of the Q-factor values of the peaks. |
| RightValues | Returns an array with the data values at the current position of the right cursor line. |
| RMSValues | Returns an array with the RMS value of the data values between the cursor lines. |
| StdDevValues | Returns an array with the standard deviation value of the data values between the cursor lines. |
| XMaxValues | Returns an array with the positions of the maxima of the data values between the cursor lines on the x-axis. |
| XMinValues | Returns an array with the positions of the minima of the data values between the cursor lines on the x-axis. |
| YMaxValues | Returns an array with the positions of the maxima of the data values between the cursor lines on the y-axes. |
| YMinValues | Returns an array with the positions of the minima of the data values between the cursor lines on the y-axes. |
| ZetaValues | Returns an array of the Zeta values of the peaks. |


---

## CursorType Property

*Quelle: `PSV~PeakCursor~CursorType.html` · Polytec PSV Type Library · PeakCursor Object : CursorType Property*

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

Always ptcCursorTypePeak.


---

## DampingValues Property

*Quelle: `PSV~PeakCursor~DampingValues.html` · Polytec PSV Type Library · PeakCursor Object : DampingValues Property*

### Description

Returns an array with the 3 dB width of the peak curve fitted to the data values between the cursor lines.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DampingValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display). If there are two graphs, both values are the same.


---

## FMaxValues Property

*Quelle: `PSV~PeakCursor~FMaxValues.html` · Polytec PSV Type Library · PeakCursor Object : FMaxValues Property*

### Description

Returns an array with the frequency of the maximum of the peak curve fitted to the data values between the cursor lines.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FMaxValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display). If there are two graphs, both values are the same.


---

## LeftValues Property

*Quelle: `PSV~PeakCursor~LeftValues.html` · Polytec PSV Type Library · PeakCursor Object : LeftValues Property*

### Description

Returns an array with the data values at the current position of the left cursor line.

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

## MeanValues Property

*Quelle: `PSV~PeakCursor~MeanValues.html` · Polytec PSV Type Library · PeakCursor Object : MeanValues Property*

### Description

Returns an array with the means of the data values between the cursor lines.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MeanValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display).

### Example


---

## QFactorValues Property

*Quelle: `PSV~PeakCursor~QFactorValues.html` · Polytec PSV Type Library · PeakCursor Object : QFactorValues Property*

### Description

Returns an array of the Q-factor values of the peaks.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property QFactorValues As Double()
```

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display). The Q-factor is the frequency of the peak divided by the width at -3 dB.

### Example


---

## RightValues Property

*Quelle: `PSV~PeakCursor~RightValues.html` · Polytec PSV Type Library · PeakCursor Object : RightValues Property*

### Description

Returns an array with the data values at the current position of the right cursor line.

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


---

## RMSValues Property

*Quelle: `PSV~PeakCursor~RMSValues.html` · Polytec PSV Type Library · PeakCursor Object : RMSValues Property*

### Description

Returns an array with the RMS value of the data values between the cursor lines.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property RMSValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display). If there are two graphs, both values are the same and correspond to graph 1.


---

## StdDevValues Property

*Quelle: `PSV~PeakCursor~StdDevValues.html` · Polytec PSV Type Library · PeakCursor Object : StdDevValues Property*

### Description

Returns an array with the standard deviation value of the data values between the cursor lines.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property StdDevValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display). If there are two graphs, both values are the same and correspond to graph 1.


---

## XMaxValues Property

*Quelle: `PSV~PeakCursor~XMaxValues.html` · Polytec PSV Type Library · PeakCursor Object : XMaxValues Property*

### Description

Returns an array with the positions of the maxima of the data values between the cursor lines on the x-axis.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property XMaxValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display).


---

## XMinValues Property

*Quelle: `PSV~PeakCursor~XMinValues.html` · Polytec PSV Type Library · PeakCursor Object : XMinValues Property*

### Description

Returns an array with the positions of the minima of the data values between the cursor lines on the x-axis.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property XMinValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display).


---

## YMaxValues Property

*Quelle: `PSV~PeakCursor~YMaxValues.html` · Polytec PSV Type Library · PeakCursor Object : YMaxValues Property*

### Description

Returns an array with the positions of the maxima of the data values between the cursor lines on the y-axes.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property YMaxValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display).


---

## YMinValues Property

*Quelle: `PSV~PeakCursor~YMinValues.html` · Polytec PSV Type Library · PeakCursor Object : YMinValues Property*

### Description

Returns an array with the positions of the minima of the data values between the cursor lines on the y-axes.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property YMinValues As Double()
```

### Return Type

One dimensional, 0-based array of doubles.

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display).

### Example


---

## ZetaValues Property

*Quelle: `PSV~PeakCursor~ZetaValues.html` · Polytec PSV Type Library · PeakCursor Object : ZetaValues Property*

### Description

Returns an array of the Zeta values of the peaks.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ZetaValues As Double()
```

### Remarks

The number of values depends on the display type of the analyzer view (1 graph or 2 graph display). The damping coefficient Zeta is the with of the peak at -3 dB divided by the doubled frequency of the peak. This is only valid for small damping values.

### Example
