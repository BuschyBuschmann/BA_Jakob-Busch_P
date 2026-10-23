# POLYFILELib – XAxis

## XAxis Object

*Quelle: `POLYFILELib~XAxis.html` · Polytec PolyFile Type Library*

### Description

Contains information about the x-axis for the data returned by GetData().


---

## XAxis Object Members

*Quelle: `POLYFILELib~XAxis_members.html` · Polytec PolyFile Type Library*

### Public Methods

| GetIndex | Returns the index to the data value that should be displayed at position X of the x-axis. |
|---|---|
| GetLeftX | Returns the x-axis position of the left edge of the bin that should display the data value with index lIndex. |
| GetMidX | Returns the x-axis position of the middle of the bin that should display the data. |
| GetRightX | Returns the x-axis position of the right edge of the bin that should display the data. |

### Public Properties

| Max | Returns the maximum x-axis value of the data. |
|---|---|
| MaxCount | Returns the number of data values. |
| Min | Returns the minimum x-axis value of the data. |
| Name | Returns the label of the x-axis. |
| Unit | Returns the unit of the data values. |


---

## GetIndex Method

*Quelle: `POLYFILELib~XAxis~GetIndex.html` · Polytec PolyFile Type Library · XAxis Object : GetIndex Method*

### Description

Returns the index to the data value that should be displayed at position X of the x-axis.

### Syntax

*Visual Basic:*
```
Public Function GetIndex( _
   ByVal dX As Double _
) As Long
```

### Parameters

dX

Position on x-axis

### Return Type

The returned index value is zero-based and corresponds to the arrays returned by GetData().

### Remarks

If the array returned by GetData() contains interleaved values (e.g. for displays ptcDisplayMagPhase or ptcDisplayRealImag) you have to multiply Index by two to get the position of the value pair of these displays.


---

## GetLeftX Method

*Quelle: `POLYFILELib~XAxis~GetLeftX.html` · Polytec PolyFile Type Library · XAxis Object : GetLeftX Method*

### Description

Returns the x-axis position of the left edge of the bin that should display the data value with index lIndex.

### Syntax

*Visual Basic:*
```
Public Function GetLeftX( _
   ByVal lIndex As Long _
) As Double
```

### Parameters

lIndex

Index of the data point


---

## GetMidX Method

*Quelle: `POLYFILELib~XAxis~GetMidX.html` · Polytec PolyFile Type Library · XAxis Object : GetMidX Method*

### Description

Returns the x-axis position of the middle of the bin that should display the data.

### Syntax

*Visual Basic:*
```
Public Function GetMidX( _
   ByVal lIndex As Long _
) As Double
```

### Parameters

lIndex

Index of the data point


---

## GetRightX Method

*Quelle: `POLYFILELib~XAxis~GetRightX.html` · Polytec PolyFile Type Library · XAxis Object : GetRightX Method*

### Description

Returns the x-axis position of the right edge of the bin that should display the data.

### Syntax

*Visual Basic:*
```
Public Function GetRightX( _
   ByVal lIndex As Long _
) As Double
```

### Parameters

lIndex

Index of the data point


---

## Max Property

*Quelle: `POLYFILELib~XAxis~Max.html` · Polytec PolyFile Type Library · XAxis Object : Max Property*

### Description

Returns the maximum x-axis value of the data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Max As Double
```


---

## MaxCount Property

*Quelle: `POLYFILELib~XAxis~MaxCount.html` · Polytec PolyFile Type Library · XAxis Object : MaxCount Property*

### Description

Returns the number of data values.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxCount As Long
```


---

## Min Property

*Quelle: `POLYFILELib~XAxis~Min.html` · Polytec PolyFile Type Library · XAxis Object : Min Property*

### Description

Returns the minimum x-axis value of the data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Min As Double
```


---

## Name Property

*Quelle: `POLYFILELib~XAxis~Name.html` · Polytec PolyFile Type Library · XAxis Object : Name Property*

### Description

Returns the label of the x-axis.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Unit Property

*Quelle: `POLYFILELib~XAxis~Unit.html` · Polytec PolyFile Type Library · XAxis Object : Unit Property*

### Description

Returns the unit of the data values.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Unit As String
```
