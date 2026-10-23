# PolyMathLib – PeakFit

## PeakFit Object

*Quelle: `PolyMathLib~PeakFit.html` · Polytec PolyMath Type Library*

### Description

PeakFit allows to fit the frequency response of a one-dimensional harmonic oscillator to a real or complex spectrum.


---

## PeakFit Object Members

*Quelle: `PolyMathLib~PeakFit_members.html` · Polytec PolyMath Type Library*

### Public Methods

| Fit | Fits the frequency response of an one-dimensional harmonic oscillator to the given spectrum. |
|---|---|
| FitXY | Fits the frequency response of an one-dimensional harmonic oscillator to the given spectrum. |
| GetFunction | Gets the fitted frequency response of the one-dimensional harmonic oscillator. |
| GetFunctionXY | Gets the fitted frequency response of the one-dimensional harmonic oscillator. |
| GetPeak | Gets the frequency and the amplitude of the maximum of the frequency response. |
| GetWidth | Retrieves the width of the fitted frequency response at the given height. |


---

## Fit Method

*Quelle: `PolyMathLib~PeakFit~Fit.html` · Polytec PolyMath Type Library · PeakFit Object : Fit Method*

### Description

Fits the frequency response of an one-dimensional harmonic oscillator to the given spectrum.

### Syntax

*Visual Basic:*
```
Public Sub Fit( _
   ByVal dXMin As Double, _
   ByVal dXMax As Double, _
   ByVal vY As Variant, _
   ByVal vbComplex As Boolean, _
   ByVal vbPower As Boolean _
)
```

### Parameters

dXMin

The minimum frequency of the spectrum in Hz.

dXMax

The maximum frequency of the spectrum in Hz.

vY

One-dimensional array of type Single or Double containing the real or complex linear spectrum. If the spectrum is complex the size of the array must be even. Real parts are at the even places and imaginary parts at the odd places of the array.

vbComplex

Specifies whether the spectrum is complex.

vbPower

Specifies whether the spectrum is a power spectrum (auto power, cross power).

### Remarks

The method does not support logarithmic spectra (dB-values).


---

## FitXY Method

*Quelle: `PolyMathLib~PeakFit~FitXY.html` · Polytec PolyMath Type Library · PeakFit Object : FitXY Method*

### Description

Fits the frequency response of an one-dimensional harmonic oscillator to the given spectrum.

### Syntax

*Visual Basic:*
```
Public Sub FitXY( _
   ByVal vX As Variant, _
   ByVal vY As Variant, _
   ByVal vbComplex As Boolean, _
   ByVal vbPower As Boolean _
)
```

### Parameters

vX

One-dimensional array of type Single or Double containing the frequencies of the corresponding amplitude values of the given spectrum.

vY

One-dimensional array of type Single or Double containing the real or complex linear spectrum. If the spectrum is complex, the size of the array must be even. Real parts are at the even places and imaginary parts at the odd places of the array.

vbComplex

Specifies whether the spectrum is complex.

vbPower

Specifies whether the spectrum is a power spectrum (auto power, cross power).

### Remarks

If the spectrum is complex, Y must have the double size of X. Otherwise X and Y must be of the same size. The method does not support logarithmic spectra (dB-values).


---

## GetFunction Method

*Quelle: `PolyMathLib~PeakFit~GetFunction.html` · Polytec PolyMath Type Library · PeakFit Object : GetFunction Method*

### Description

Gets the fitted frequency response of the one-dimensional harmonic oscillator.

### Syntax

*Visual Basic:*
```
Public Function GetFunction( _
   ByVal dXMin As Double, _
   ByVal dXMax As Double, _
   ByVal lCount As Long _
) As Double()
```

### Parameters

dXMin

The minimum frequency of the response in Hz.

dXMax

The maximum frequency of the response in Hz.

lCount

The number of points in the returned function.

### Return Type

One-dimensional array of type Double containing the complex frequency response. The array contains the y-values of the peak function with alternating real and imaginary parts at equidistant frequencies from dXMin to dXMax.


---

## GetFunctionXY Method

*Quelle: `PolyMathLib~PeakFit~GetFunctionXY.html` · Polytec PolyMath Type Library · PeakFit Object : GetFunctionXY Method*

### Description

Gets the fitted frequency response of the one-dimensional harmonic oscillator.

### Syntax

*Visual Basic:*
```
Public Function GetFunctionXY( _
   ByVal vX As Variant _
) As Double()
```

### Parameters

vX

One-dimensional array of type Single or Double containing the frequencies for the y-values of the peak function.

### Return Type

One-dimensional array of type Double containing the complex frequency response. The array contains the y-values of the peak function with alternating real and imaginary parts at the frequencies specified in vX.

### Remarks

The size of the returned array is of double size as vX.


---

## GetPeak Method

*Quelle: `PolyMathLib~PeakFit~GetPeak.html` · Polytec PolyMath Type Library · PeakFit Object : GetPeak Method*

### Description

Gets the frequency and the amplitude of the maximum of the frequency response.

### Syntax

*Visual Basic:*
```
Public Function GetPeak( _
   ByVal vbDbA As Boolean, _
   ByRef pdFrequency As Double _
) As Double
```

### Parameters

vbDbA

Specifies, whether dB(A) acoustic weighting shall be used.

pdFrequency

The frequency of the maximum of the response.

### Return Type

The amplitude of the maximum of the response.


---

## GetWidth Method

*Quelle: `PolyMathLib~PeakFit~GetWidth.html` · Polytec PolyMath Type Library · PeakFit Object : GetWidth Method*

### Description

Retrieves the width of the fitted frequency response at the given height.

### Syntax

*Visual Basic:*
```
Public Function GetWidth( _
   ByVal dHeightDb As Double, _
   ByVal vbDbA As Boolean _
) As Double
```

### Parameters

dHeightDb

The height in dB measured from the peak height where the width shall be returned. Always negative.

vbDbA

True if dB(A) acoustic weighting shall be used.

### Return Type

The width of the frequency response at the specified height, in Hz.
