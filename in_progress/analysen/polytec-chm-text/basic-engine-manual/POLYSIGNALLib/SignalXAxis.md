# POLYSIGNALLib – SignalXAxis

## SignalXAxis Object

*Quelle: `POLYSIGNALLib~SignalXAxis.html` · Polytec PolySignal Type Library*

### Description

The x-axis of the signal.

### Object Model


---

## SignalXAxis Object Members

*Quelle: `POLYSIGNALLib~SignalXAxis_members.html` · Polytec PolySignal Type Library*

### Public Methods

| Clone | Returns a copy of the object. |
|---|---|
| Copy | Copies the properties of the given object to the object. |
| GetIndex | Returns the index to the data value that should be displayed at position X of the x-axis. |
| GetLeftX | Returns the x-axis position of the left edge of the bin that should display the data value with index lIndex. |
| GetMidX | Returns the x-axis position of the middle of the bin that should display the data. |
| GetRightX | Returns the x-axis position of the right edge of the bin that should display the data. |
| IsEqual | Returns whether the properties of the object are equal to the properties of the given object. |

### Public Properties

| Max | Returns the maximum x-axis value of the data. |
|---|---|
| MaxCount | Returns the number of data values. |
| Min | Returns the minimum x-axis value of the data. |
| Name | Returns the label of the x-axis. |
| Unit | Returns the unit of the data values. |


---

## Clone Method

*Quelle: `POLYSIGNALLib~SignalXAxis~Clone.html` · Polytec PolySignal Type Library · SignalXAxis Object : Clone Method*

### Description

Returns a copy of the object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As SignalXAxis
```

### Return Type

The newly created object.


---

## Copy Method

*Quelle: `POLYSIGNALLib~SignalXAxis~Copy.html` · Polytec PolySignal Type Library · SignalXAxis Object : Copy Method*

### Description

Copies the properties of the given object to the object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIXAxis As SignalXAxis _
)
```

### Parameters

pIXAxis

The object to copy the properties from.


---

## GetIndex Method

*Quelle: `POLYSIGNALLib~SignalXAxis~GetIndex.html` · Polytec PolySignal Type Library · SignalXAxis Object : GetIndex Method*

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

*Quelle: `POLYSIGNALLib~SignalXAxis~GetLeftX.html` · Polytec PolySignal Type Library · SignalXAxis Object : GetLeftX Method*

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

*Quelle: `POLYSIGNALLib~SignalXAxis~GetMidX.html` · Polytec PolySignal Type Library · SignalXAxis Object : GetMidX Method*

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

*Quelle: `POLYSIGNALLib~SignalXAxis~GetRightX.html` · Polytec PolySignal Type Library · SignalXAxis Object : GetRightX Method*

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

## IsEqual Method

*Quelle: `POLYSIGNALLib~SignalXAxis~IsEqual.html` · Polytec PolySignal Type Library · SignalXAxis Object : IsEqual Method*

### Description

Returns whether the properties of the object are equal to the properties of the given object.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIXAxis As SignalXAxis _
) As Boolean
```

### Parameters

pIXAxis

The object to compare the properties to.

### Return Type

True if the properties of the object are equal to the properties of the given object.

### Example


---

## Max Property

*Quelle: `POLYSIGNALLib~SignalXAxis~Max.html` · Polytec PolySignal Type Library · SignalXAxis Object : Max Property*

### Description

Returns the maximum x-axis value of the data.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Max As Double
```


---

## MaxCount Property

*Quelle: `POLYSIGNALLib~SignalXAxis~MaxCount.html` · Polytec PolySignal Type Library · SignalXAxis Object : MaxCount Property*

### Description

Returns the number of data values.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MaxCount As Long
```


---

## Min Property

*Quelle: `POLYSIGNALLib~SignalXAxis~Min.html` · Polytec PolySignal Type Library · SignalXAxis Object : Min Property*

### Description

Returns the minimum x-axis value of the data.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Min As Double
```


---

## Name Property

*Quelle: `POLYSIGNALLib~SignalXAxis~Name.html` · Polytec PolySignal Type Library · SignalXAxis Object : Name Property*

### Description

Returns the label of the x-axis.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Unit Property

*Quelle: `POLYSIGNALLib~SignalXAxis~Unit.html` · Polytec PolySignal Type Library · SignalXAxis Object : Unit Property*

### Description

Returns the unit of the data values.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Unit As String
```
