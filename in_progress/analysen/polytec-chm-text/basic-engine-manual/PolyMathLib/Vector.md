# PolyMathLib – Vector

## Vector Object

*Quelle: `PolyMathLib~Vector.html` · Polytec PolyMath Type Library*

### Description

Vector contains methods performing basic mathematical operations on one dimensional arrays of Single or Double, interpreted as real or complex vectors.

### Remarks

A complex vector of size n is represented as a zero-based array of size 2n with the real parts on even and the imaginary parts on odd places.


---

## Vector Object Members

*Quelle: `PolyMathLib~Vector_members.html` · Polytec PolyMath Type Library*

### Public Methods

| Add | Sum of two vectors or a vector and a scalar. |
|---|---|
| Append | Returns the concatenation of two arrays. |
| Complex | Returns a complex vector with real parts from X and imaginary parts from Y. |
| Div | Quotient of real vectors or a (real or complex) vector and a scalar. |
| DivCplx | Quotient of complex vectors or a complex vector and a scalar. |
| Extract | Returns a sub array. |
| Imag | Returns the imaginary part of a complex vector in a real vector. |
| Magnitude | Returns the magnitude of a complex vector in a real vector. |
| Max | Returns the maximum value of the real vector X. |
| Mean | Returns the arithmetic mean value of the real vector X. |
| Min | Returns the minimum value of the real vector X. |
| Mul | Product of real vectors or a (real or complex) vector and a scalar. |
| MulCplx | Product of complex vectors or a complex vector and a scalar. Returns the product of the complex vectors X and Y. |
| PhaseDeg | Returns the phase (in degree) of a complex vector in a real vector. |
| PhaseRad | Returns the phase (in radian) of a complex vector in a real vector. |
| Real | Returns the real part of a complex vector in a real vector. |
| RMS | Returns the square root of the mean squared values of the real vector X. |
| StandardDeviation | Returns the (N-1) standard deviation of the real vector X. |
| Sub | Difference of two vectors or a vector and a scalar. |


---

## Add Method

*Quelle: `PolyMathLib~Vector~Add.html` · Polytec PolyMath Type Library · Vector Object : Add Method*

### Description

Sum of two vectors or a vector and a scalar.

### Syntax

*Visual Basic:*
```
Public Function Add( _
   ByVal varInput1 As Variant, _
   ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The real or complex vector X.

varInput2

The real or complex scalar or vector Y.

### Return Type

Array of the same type and size as X.

### Remarks

The input vectors are one-dimensional arrays of Single or Double. Both arrays have to be of the same type and size.

Or, Y can be a scalar value such as Single, Double, Integer or Long.

Or, if X is of even size, Y can be a one-dimensional array of size 2 and the same type as X. Then Y is interpreted as complex scalar value.


---

## Append Method

*Quelle: `PolyMathLib~Vector~Append.html` · Polytec PolyMath Type Library · Vector Object : Append Method*

### Description

Returns the concatenation of two arrays.

### Syntax

*Visual Basic:*
```
Public Function Append( _
   ByVal varInput1 As Variant, _
   ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The input array X.

varInput2

The input array Y.

### Return Type

Array of the same type as X.


---

## Complex Method

*Quelle: `PolyMathLib~Vector~Complex.html` · Polytec PolyMath Type Library · Vector Object : Complex Method*

### Description

Returns a complex vector with real parts from X and imaginary parts from Y.

### Syntax

*Visual Basic:*
```
Public Function Complex( _
   ByVal varInput1 As Variant, _
   Optional ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The real parts vector X.

varInput2

The imaginary parts vector X.

### Remarks

X is a one-dimensional array of Single or Double.

If Y is not present, a complex vector with real parts from X and imaginary parts zero is returned.


---

## Div Method

*Quelle: `PolyMathLib~Vector~Div.html` · Polytec PolyMath Type Library · Vector Object : Div Method*

### Description

Quotient of real vectors or a (real or complex) vector and a scalar.

### Syntax

*Visual Basic:*
```
Public Function Div( _
   ByVal varInput1 As Variant, _
   ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The real or complex vector X.

varInput2

The real or complex scalar or vector Y.

### Remarks

Division by zero is handled by setting the result value to infinity (= Val("-1.#IND)).

The input vectors are one-dimensional arrays of Single or Double. Both arrays have to be of the same type and size.

Or, Y can be a scalar value such as Single, Double, Integer or Long.

Or, if X is of even size, Y can be a one-dimensional array of size 2 and the same type as X. Then Y is interpreted as complex scalar value.

### Example


---

## DivCplx Method

*Quelle: `PolyMathLib~Vector~DivCplx.html` · Polytec PolyMath Type Library · Vector Object : DivCplx Method*

### Description

Quotient of complex vectors or a complex vector and a scalar.

### Syntax

*Visual Basic:*
```
Public Function DivCplx( _
   ByVal varInput1 As Variant, _
   ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The complex vector X.

varInput2

The complex vector or scalar Y.

### Remarks

Division by zero is handled by setting the result value to infinity (= Val("-1.#IND)).

The input vectors are one-dimensional arrays of Single or Double. Both arrays have to be of the same type and size. The size must be even.

Or, Y can be a scalar value such as Single, Double, Integer or Long.

Or, Y can be a one-dimensional array of size 2 and the same type as X. Then Y is interpreted as complex scalar value.

### Example


---

## Extract Method

*Quelle: `PolyMathLib~Vector~Extract.html` · Polytec PolyMath Type Library · Vector Object : Extract Method*

### Description

Returns a sub array.

### Syntax

*Visual Basic:*
```
Public Function Extract( _
   ByVal varInput As Variant, _
   ByVal lFirst As Long, _
   ByVal lCount As Long _
) As Variant
```

### Parameters

varInput

The vector X.

lFirst

Zero based index to the start position, the actual lower bound of X is ignored.

lCount

Length of the sub array.

### Return Type

Array of size Count and same type as X.


---

## Imag Method

*Quelle: `PolyMathLib~Vector~Imag.html` · Polytec PolyMath Type Library · Vector Object : Imag Method*

### Description

Returns the imaginary part of a complex vector in a real vector.

### Syntax

*Visual Basic:*
```
Public Function Imag( _
   ByVal varInput As Variant _
) As Variant
```

### Parameters

varInput

The complex vector X.

### Return Type

Array of the same type and half the size of X.

### Remarks

The input vector is a one-dimensional array of Single or Double of even size.


---

## Magnitude Method

*Quelle: `PolyMathLib~Vector~Magnitude.html` · Polytec PolyMath Type Library · Vector Object : Magnitude Method*

### Description

Returns the magnitude of a complex vector in a real vector.

### Syntax

*Visual Basic:*
```
Public Function Magnitude( _
   ByVal varInput As Variant _
) As Variant
```

### Parameters

varInput

The complex vector X.

### Return Type

Array of the same type and half the size of X.

### Remarks

The input vector is a one-dimensional array of Single or Double of even size.


---

## Max Method

*Quelle: `PolyMathLib~Vector~Max.html` · Polytec PolyMath Type Library · Vector Object : Max Method*

### Description

Returns the maximum value of the real vector X.

### Syntax

*Visual Basic:*
```
Public Function Max( _
   ByVal varInput As Variant _
) As Double
```

### Parameters

varInput

The real vector X.

### Remarks

The input vector is a one-dimensional array of Single or Double.


---

## Mean Method

*Quelle: `PolyMathLib~Vector~Mean.html` · Polytec PolyMath Type Library · Vector Object : Mean Method*

### Description

Returns the arithmetic mean value of the real vector X.

### Syntax

*Visual Basic:*
```
Public Function Mean( _
   ByVal varInput As Variant _
) As Double
```

### Parameters

varInput

The real vector X.

### Remarks

The input vector is a one-dimensional array of Single or Double.


---

## Min Method

*Quelle: `PolyMathLib~Vector~Min.html` · Polytec PolyMath Type Library · Vector Object : Min Method*

### Description

Returns the minimum value of the real vector X.

### Syntax

*Visual Basic:*
```
Public Function Min( _
   ByVal varInput As Variant _
) As Double
```

### Parameters

varInput

The real vector X.

### Remarks

The input vector is a one-dimensional array of Single or Double.


---

## Mul Method

*Quelle: `PolyMathLib~Vector~Mul.html` · Polytec PolyMath Type Library · Vector Object : Mul Method*

### Description

Product of real vectors or a (real or complex) vector and a scalar.

### Syntax

*Visual Basic:*
```
Public Function Mul( _
   ByVal varInput1 As Variant, _
   ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The real or complex vector X.

varInput2

The real or complex scalar or vector Y.

### Remarks

The input vectors are one-dimensional arrays of Single or Double. Both arrays have to be of the same type and size.

Or, Y can be a scalar value such as Single, Double, Integer or Long.

Or, if X is of even size, Y can be a one-dimensional array of size 2 and the same type as X. Then Y is interpreted as complex scalar value.


---

## MulCplx Method

*Quelle: `PolyMathLib~Vector~MulCplx.html` · Polytec PolyMath Type Library · Vector Object : MulCplx Method*

### Description

Product of complex vectors or a complex vector and a scalar.
Returns the product of the complex vectors X and Y.

### Syntax

*Visual Basic:*
```
Public Function MulCplx( _
   ByVal varInput1 As Variant, _
   ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The complex vector X.

varInput2

The complex vector or scalar Y.

### Remarks

The input vectors are one-dimensional arrays of Single or Double. Both arrays have to be of the same type and size. The size must be even.

Or, Y can be a scalar value such as Single, Double, Integer or Long.

Or, Y can be a one-dimensional array of size 2 and the same type as X. Then Y is interpreted as complex scalar value.


---

## PhaseDeg Method

*Quelle: `PolyMathLib~Vector~PhaseDeg.html` · Polytec PolyMath Type Library · Vector Object : PhaseDeg Method*

### Description

Returns the phase (in degree) of a complex vector in a real vector.

### Syntax

*Visual Basic:*
```
Public Function PhaseDeg( _
   ByVal varInput As Variant _
) As Variant
```

### Parameters

varInput

The complex vector X.

### Return Type

Array of the same type and half the size of X.

### Remarks

The input vector is a one-dimensional array of Single or Double of even size.


---

## PhaseRad Method

*Quelle: `PolyMathLib~Vector~PhaseRad.html` · Polytec PolyMath Type Library · Vector Object : PhaseRad Method*

### Description

Returns the phase (in radian) of a complex vector in a real vector.

### Syntax

*Visual Basic:*
```
Public Function PhaseRad( _
   ByVal varInput As Variant _
) As Variant
```

### Parameters

varInput

The complex vector X.

### Return Type

Array of the same type and half the size of X.

### Remarks

The input vector is a one-dimensional array of Single or Double of even size.


---

## Real Method

*Quelle: `PolyMathLib~Vector~Real.html` · Polytec PolyMath Type Library · Vector Object : Real Method*

### Description

Returns the real part of a complex vector in a real vector.

### Syntax

*Visual Basic:*
```
Public Function Real( _
   ByVal varInput As Variant _
) As Variant
```

### Parameters

varInput

The complex vector X.

### Return Type

Array of the same type and half the size of X.

### Remarks

The input vector is a one-dimensional array of Single or Double of even size.


---

## RMS Method

*Quelle: `PolyMathLib~Vector~RMS.html` · Polytec PolyMath Type Library · Vector Object : RMS Method*

### Description

Returns the square root of the mean squared values of the real vector X.

### Syntax

*Visual Basic:*
```
Public Function RMS( _
   ByVal varInput As Variant _
) As Double
```

### Parameters

varInput

The real vector X.

### Remarks

The input vector is a one-dimensional array of Single or Double.


---

## StandardDeviation Method

*Quelle: `PolyMathLib~Vector~StandardDeviation.html` · Polytec PolyMath Type Library · Vector Object : StandardDeviation Method*

### Description

Returns the (N-1) standard deviation of the real vector X.

### Syntax

*Visual Basic:*
```
Public Function StandardDeviation( _
   ByVal varInput As Variant _
) As Double
```

### Parameters

varInput

The real vector X.

### Remarks

The input vector is a one-dimensional array of Single or Double.


---

## Sub Method

*Quelle: `PolyMathLib~Vector~Sub.html` · Polytec PolyMath Type Library · Vector Object : Sub Method*

### Description

Difference of two vectors or a vector and a scalar.

### Syntax

*Visual Basic:*
```
Public Function Sub( _
   ByVal varInput1 As Variant, _
   ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The real or complex vector X.

varInput2

The real or complex vector or scalar Y.

### Remarks

The input vectors are one-dimensional arrays of Single or Double. Both arrays have to be of the same type and size.

Or, Y can be a scalar value such as Single, Double, Integer or Long.

Or, if X is of even size, Y can be a one-dimensional array of size 2 and the same type as X. Then Y is interpreted as complex scalar value.
