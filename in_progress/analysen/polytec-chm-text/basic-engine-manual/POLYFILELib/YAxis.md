# POLYFILELib – YAxis

## YAxis Object

*Quelle: `POLYFILELib~YAxis.html` · Polytec PolyFile Type Library*

### Description

Contains information about the y-axis used to display the data returned by GetData. Item of the YAxes collection.


---

## YAxis Object Members

*Quelle: `POLYFILELib~YAxis_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Max | Returns the maximum y-axis value of the data. |
|---|---|
| Min | Returns the minimum y-axis value of the data. |
| Name | Returns the label of the y-axis. |
| Unit | Returns the y-axis unit of the data values. |


---

## Max Property

*Quelle: `POLYFILELib~YAxis~Max.html` · Polytec PolyFile Type Library · YAxis Object : Max Property*

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

*Quelle: `POLYFILELib~YAxis~Min.html` · Polytec PolyFile Type Library · YAxis Object : Min Property*

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

*Quelle: `POLYFILELib~YAxis~Name.html` · Polytec PolyFile Type Library · YAxis Object : Name Property*

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

*Quelle: `POLYFILELib~YAxis~Unit.html` · Polytec PolyFile Type Library · YAxis Object : Unit Property*

### Description

Returns the y-axis unit of the data values.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Unit As String
```
