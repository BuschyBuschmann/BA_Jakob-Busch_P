# PolyMathLib – Statistics

## Statistics Object

*Quelle: `PolyMathLib~Statistics.html` · Polytec PolyMath Type Library*

### Description

Statistics contains methods performing basic statistics operations on one dimensional arrays of Single or Double, interpreted as real vectors.


---

## Statistics Object Members

*Quelle: `PolyMathLib~Statistics_members.html` · Polytec PolyMath Type Library*

### Public Methods

| Add | Adds a vector to the statistic. Increases the Count by 1. |
|---|---|
| Clear | Clears the statistics object; resets the Count to 0. |

### Public Properties

| Count | Returns the current count. |
|---|---|
| Max | Returns an array containing the element-wise maximum of vectors added so far. |
| Mean | Returns an array containing the element-wise arithmetic mean of all vectors added so far. |
| Min | Returns an array containing the element-wise minimum of vectors added so far. |
| StandardDeviation | Returns an array containing the element-wise (N-1)-standard deviation of all vectors added so far. |


---

## Add Method

*Quelle: `PolyMathLib~Statistics~Add.html` · Polytec PolyMath Type Library · Statistics Object : Add Method*

### Description

Adds a vector to the statistic. Increases the Count by 1.

### Syntax

*Visual Basic:*
```
Public Sub Add( _
   ByVal varInput As Variant _
)
```

### Parameters

varInput

One-dimensional array of type Single or Double.

### Remarks

All added vectors must be of the same size and type. Arrays returned by Min, Max, Mean and StandardDeviation have the same dimensions and bounds as the first added vector.


---

## Clear Method

*Quelle: `PolyMathLib~Statistics~Clear.html` · Polytec PolyMath Type Library · Statistics Object : Clear Method*

### Description

Clears the statistics object; resets the Count to 0.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Count Property

*Quelle: `PolyMathLib~Statistics~Count.html` · Polytec PolyMath Type Library · Statistics Object : Count Property*

### Description

Returns the current count.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Max Property

*Quelle: `PolyMathLib~Statistics~Max.html` · Polytec PolyMath Type Library · Statistics Object : Max Property*

### Description

Returns an array containing the element-wise maximum of vectors added so far.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Max As Variant
```

### Remarks

At least one vector must have been added.


---

## Mean Property

*Quelle: `PolyMathLib~Statistics~Mean.html` · Polytec PolyMath Type Library · Statistics Object : Mean Property*

### Description

Returns an array containing the element-wise arithmetic mean of all vectors added so far.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Mean As Variant
```

### Remarks

At least one vector must have been added.


---

## Min Property

*Quelle: `PolyMathLib~Statistics~Min.html` · Polytec PolyMath Type Library · Statistics Object : Min Property*

### Description

Returns an array containing the element-wise minimum of vectors added so far.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Min As Variant
```

### Remarks

At least one vector must have been added.


---

## StandardDeviation Property

*Quelle: `PolyMathLib~Statistics~StandardDeviation.html` · Polytec PolyMath Type Library · Statistics Object : StandardDeviation Property*

### Description

Returns an array containing the element-wise (N-1)-standard deviation of all vectors added so far.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property StandardDeviation As Variant
```

### Remarks

At least two vectors must have been added.
