# POLYSIGNALLib – SignalYAxis

## SignalYAxis Object

*Quelle: `POLYSIGNALLib~SignalYAxis.html` · Polytec PolySignal Type Library*

### Description

The y-axis of the signal.

### Object Model


---

## SignalYAxis Object Members

*Quelle: `POLYSIGNALLib~SignalYAxis_members.html` · Polytec PolySignal Type Library*

### Public Methods

| Clone | Returns a copy of the object. |
|---|---|
| Copy | Copies the properties of the given object to the object. |
| IsEqual | Returns whether the properties of the object are equal to the properties of the given object. |

### Public Properties

| Max | Returns the maximum y-axis value of the data. |
|---|---|
| Min | Returns the minimum y-axis value of the data. |
| Name | Returns the label of the y-axis. |
| Unit | Returns the y-axis unit of the data values. |


---

## Clone Method

*Quelle: `POLYSIGNALLib~SignalYAxis~Clone.html` · Polytec PolySignal Type Library · SignalYAxis Object : Clone Method*

### Description

Returns a copy of the object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As SignalYAxis
```


---

## Copy Method

*Quelle: `POLYSIGNALLib~SignalYAxis~Copy.html` · Polytec PolySignal Type Library · SignalYAxis Object : Copy Method*

### Description

Copies the properties of the given object to the object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIYAxis As SignalYAxis _
)
```

### Parameters

pIYAxis

The object to copy the properties from.


---

## IsEqual Method

*Quelle: `POLYSIGNALLib~SignalYAxis~IsEqual.html` · Polytec PolySignal Type Library · SignalYAxis Object : IsEqual Method*

### Description

Returns whether the properties of the object are equal to the properties of the given object.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIYAxis As SignalYAxis _
) As Boolean
```

### Parameters

pIYAxis

The object to compare the properties to.

### Example


---

## Max Property

*Quelle: `POLYSIGNALLib~SignalYAxis~Max.html` · Polytec PolySignal Type Library · SignalYAxis Object : Max Property*

### Description

Returns the maximum y-axis value of the data.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Max As Double
```

### Remarks

It is not guaranteed, that the data is between Min and Max. The Min and Max values of the y-axis are used by the analyzer for the default scale of the display.


---

## Min Property

*Quelle: `POLYSIGNALLib~SignalYAxis~Min.html` · Polytec PolySignal Type Library · SignalYAxis Object : Min Property*

### Description

Returns the minimum y-axis value of the data.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Min As Double
```

### Remarks

It is not guaranteed, that the data is between Min and Max. The Min and Max values of the y-axis are used by the analyzer for the default scale of the display.


---

## Name Property

*Quelle: `POLYSIGNALLib~SignalYAxis~Name.html` · Polytec PolySignal Type Library · SignalYAxis Object : Name Property*

### Description

Returns the label of the y-axis.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Unit Property

*Quelle: `POLYSIGNALLib~SignalYAxis~Unit.html` · Polytec PolySignal Type Library · SignalYAxis Object : Unit Property*

### Description

Returns the y-axis unit of the data values.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Unit As String
```
