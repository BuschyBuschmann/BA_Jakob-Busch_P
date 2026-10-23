# POLYFILELib – IXAxis

## IXAxis Interface

*Quelle: `POLYFILELib~IXAxis.html` · Polytec PolyFile Type Library*

### Description

Contains information about the x-axis for the data returned by GetData().

### Remarks

It is recommended to cast to the XAxis object


---

## IXAxis Interface Members

*Quelle: `POLYFILELib~IXAxis_members.html` · Polytec PolyFile Type Library*

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

*Quelle: `POLYFILELib~IXAxis~GetIndex.html` · Polytec PolyFile Type Library · IXAxis Interface : GetIndex Method*

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

*Quelle: `POLYFILELib~IXAxis~GetLeftX.html` · Polytec PolyFile Type Library · IXAxis Interface : GetLeftX Method*

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

*Quelle: `POLYFILELib~IXAxis~GetMidX.html` · Polytec PolyFile Type Library · IXAxis Interface : GetMidX Method*

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

*Quelle: `POLYFILELib~IXAxis~GetRightX.html` · Polytec PolyFile Type Library · IXAxis Interface : GetRightX Method*

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

*Quelle: `POLYFILELib~IXAxis~Max.html` · Polytec PolyFile Type Library · IXAxis Interface : Max Property*

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

*Quelle: `POLYFILELib~IXAxis~MaxCount.html` · Polytec PolyFile Type Library · IXAxis Interface : MaxCount Property*

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

*Quelle: `POLYFILELib~IXAxis~Min.html` · Polytec PolyFile Type Library · IXAxis Interface : Min Property*

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

*Quelle: `POLYFILELib~IXAxis~Name.html` · Polytec PolyFile Type Library · IXAxis Interface : Name Property*

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

*Quelle: `POLYFILELib~IXAxis~Unit.html` · Polytec PolyFile Type Library · IXAxis Interface : Unit Property*

### Description

Returns the unit of the data values.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Unit As String
```
