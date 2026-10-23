# POLYSIGNALLib – Attribute

## Attribute Object

*Quelle: `POLYSIGNALLib~Attribute.html` · Polytec PolySignal Type Library*

### Description

Item of the Attributes Collection.

### Remarks

Attributes are used to attach additional values to objects like e.g. the description of a signal. The attributes are persisted with the object they are attached to.


---

## Attribute Object Members

*Quelle: `POLYSIGNALLib~Attribute_members.html` · Polytec PolySignal Type Library*

### Public Methods

| IsEqual | Returns whether the properties of the given attribute are equal to the properties of this attribute. |
|---|---|

### Public Properties

| Description | The description of the attribute. |
|---|---|
| Name | The name of the attribute. |
| Quantity | The quantity of the value of the attribute. |
| Unit | The unit of the value of the attribute. |
| Value | The value of the attribute. |


---

## IsEqual Method

*Quelle: `POLYSIGNALLib~Attribute~IsEqual.html` · Polytec PolySignal Type Library · Attribute Object : IsEqual Method*

### Description

Returns whether the properties of the given attribute are equal to the properties of this attribute.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIAttribute As Attribute _
) As Boolean
```

### Parameters

pIAttribute

The attribute to compare the properties with.

### Return Type

True when the properties of the given attribute are equal to the properties of this attribute.


---

## Description Property

*Quelle: `POLYSIGNALLib~Attribute~Description.html` · Polytec PolySignal Type Library · Attribute Object : Description Property*

### Description

The description of the attribute.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Description As String
```


---

## Name Property

*Quelle: `POLYSIGNALLib~Attribute~Name.html` · Polytec PolySignal Type Library · Attribute Object : Name Property*

### Description

The name of the attribute.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Remarks

The name must be unique in the Attributes Collection.


---

## Quantity Property

*Quelle: `POLYSIGNALLib~Attribute~Quantity.html` · Polytec PolySignal Type Library · Attribute Object : Quantity Property*

### Description

The quantity of the value of the attribute.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Quantity As String
```

### Remarks

The string can be empty.


---

## Unit Property

*Quelle: `POLYSIGNALLib~Attribute~Unit.html` · Polytec PolySignal Type Library · Attribute Object : Unit Property*

### Description

The unit of the value of the attribute.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Unit As String
```

### Remarks

The string can be empty.


---

## Value Property

*Quelle: `POLYSIGNALLib~Attribute~Value.html` · Polytec PolySignal Type Library · Attribute Object : Value Property*

### Description

The value of the attribute.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Value As Variant
```

### Remarks

The following variant types are supported: VT_I2, VT_I4, VT_R4, VT_R8, VT_DATE, VT_BSTR, VT_BOOL, VT_DECIMAL, VT_I1, VT_UI1, VT_UI2, VT_UI4, VT_I8, VT_INT, VT_UINT, VT_LPSTR, VT_LPWSTR, VT_FILETIME. Variants passed by reference (VT_BYREF) are copied. Arrays are not supported.

### Example
