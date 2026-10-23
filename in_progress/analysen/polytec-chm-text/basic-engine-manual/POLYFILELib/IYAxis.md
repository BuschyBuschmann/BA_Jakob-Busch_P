# POLYFILELib – IYAxis

## IYAxis Interface

*Quelle: `POLYFILELib~IYAxis.html` · Polytec PolyFile Type Library*

### Description

Contains information about the y-axis used to display the data returned by GetData. Item of the YAxes collection.

### Remarks

It is recommended to cast to the YAxis Object.


---

## IYAxis Interface Members

*Quelle: `POLYFILELib~IYAxis_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Max | Returns the maximum y-axis value of the data. |
|---|---|
| Min | Returns the minimum y-axis value of the data. |
| Name | Returns the label of the y-axis. |
| Unit | Returns the y-axis unit of the data values. |


---

## Max Property

*Quelle: `POLYFILELib~IYAxis~Max.html` · Polytec PolyFile Type Library · IYAxis Interface : Max Property*

### Description

Returns the maximum y-axis value of the data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Max As Double
```

### Remarks

It is not guaranteed, that the data is between Min and Max. The Min and Max values of the y-axis are used by the analyzer for the default scale of the display.


---

## Min Property

*Quelle: `POLYFILELib~IYAxis~Min.html` · Polytec PolyFile Type Library · IYAxis Interface : Min Property*

### Description

Returns the minimum y-axis value of the data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Min As Double
```

### Remarks

It is not guaranteed, that the data is between Min and Max. The Min and Max values of the y-axis are used by the analyzer for the default scale of the display.


---

## Name Property

*Quelle: `POLYFILELib~IYAxis~Name.html` · Polytec PolyFile Type Library · IYAxis Interface : Name Property*

### Description

Returns the label of the y-axis.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Unit Property

*Quelle: `POLYFILELib~IYAxis~Unit.html` · Polytec PolyFile Type Library · IYAxis Interface : Unit Property*

### Description

Returns the y-axis unit of the data values.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Unit As String
```
