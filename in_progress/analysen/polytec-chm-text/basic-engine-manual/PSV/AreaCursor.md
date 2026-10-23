# PSV – AreaCursor

## AreaCursor Object

*Quelle: `PSV~AreaCursor.html` · Polytec PSV Type Library*

### Description

The values of the current area cursor.


---

## AreaCursor Object Members

*Quelle: `PSV~AreaCursor_members.html` · Polytec PSV Type Library*

### Public Methods

| MeasPointLabelToIndex | Converts the displayed label number of a scan point to it's internal index. |
|---|---|

### Public Properties

| Values | An array with the vibration data values at the current area cursor position. |
|---|---|


---

## MeasPointLabelToIndex Method

*Quelle: `PSV~AreaCursor~MeasPointLabelToIndex.html` · Polytec PSV Type Library · AreaCursor Object : MeasPointLabelToIndex Method*

### Description

Converts the displayed label number of a scan point to it's internal index.

### Syntax

*Visual Basic:*
```
Public Function MeasPointLabelToIndex( _
   ByVal lLabel As Long _
) As Long
```

### Parameters

lLabel

The label (index that is displayed in the user interface of the application) of the san point.

### Remarks

The returned index can be used as an index into the array returned by the Values property to get the data value of the given scan point.


---

## Values Property

*Quelle: `PSV~AreaCursor~Values.html` · Polytec PSV Type Library · AreaCursor Object : Values Property*

### Description

An array with the vibration data values at the current area cursor position.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Values As Double()
```

### Return Type

One dimensional, 0-based array of double. The size of the array corresponds to the number of scan points.

### Remarks

Depending on the current display these values can be real or complex (alternating real and imaginary values).

### Example
