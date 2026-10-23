# PolyMathLib – SignalProcessing

## SignalProcessing Object

*Quelle: `PolyMathLib~SignalProcessing.html` · Polytec PolyMath Type Library*

### Description

SignalProcessing contains methods performing signal processing operations on one dimensional arrays of Single or Double, interpreted as real or complex vectors.


---

## SignalProcessing Object Members

*Quelle: `PolyMathLib~SignalProcessing_members.html` · Polytec PolyMath Type Library*

### Public Methods

| Autopower | Returns the auto power function from a complex spectrum in a real array. |
|---|---|
| AutopowerFromTimeSignal | Calculates an averaged autopower spectrum from the specified time signal. |
| AverageFFTFromTimeSignal | Calculates an averaged FFT from the specified time signal. |
| CoherenceFromTimeSignal | Calculates a coherence from the specified time signal. |
| Convolution | Calculates the convolution of the given real vectors. |
| Crosspower | Returns the cross power function from two complex spectra in a complex array. |
| CrosspowerFromTimeSignal | Calculates an averaged crosspower spectrum from the specified time signal. |
| DifferentiateTime | Returns the differentiated time signal. |
| FFT | Returns the complex spectrum from a real time signal. |
| FFTEx | Returns the complex spectrum from a real time signal. |
| FilterCoefficients | Calculates the coefficients for the specified filter. Use Convolution to apply the filter to time data. |
| FilterCoefficientsDouble | Calculates the coefficients for the specified filter. Use Convolution to apply the filter to time data. This method provides a functionality analogous to the method FilterCoefficients(...) except for that it returns the computed filter coefficients with a higher precision, as an array of type Double. |
| FRFFromTimeSignal | Calculates the frequency response function from the specified time and reference signal. |
| H1FromTimeSignal | Calculates FRF H1 from the specified time and reference signal. |
| H2FromTimeSignal | Calculates FRF H2 from the specified time and reference signal. |
| IntegrateTime | Returns the integrated time signal. |
| InverseFFT | Returns the real time signal from a complex spectrum. |
| ResampleTime | Returns the time signal sampled with a different sample frequency. |
| SavGolFilter | Applies a Savitzky-Golay differentiation filter to the specified data. |
| Transmission | Calculates (the real part of) the transmission function of the filter with the given coefficients. Note that in order for the transmission function to be real, the filter kernel must be symmetric. |
| WindowFunction | Calculates the window function of the specified type. |
| WindowFunctionDouble | Calculates the window function of the specified type. This method provides a functionality analogous to the method WindowFunction(...) except for that it returns the computed window function samples with a higher precision, as an array of type Double. |


---

## Autopower Method

*Quelle: `PolyMathLib~SignalProcessing~Autopower.html` · Polytec PolyMath Type Library · SignalProcessing Object : Autopower Method*

### Description

Returns the auto power function from a complex spectrum in a real array.

### Syntax

*Visual Basic:*
```
Public Function Autopower( _
   ByVal varInput As Variant _
) As Variant
```

### Parameters

varInput

The complex vector X.

### Return Type

Array of the same type and half the size of X.

### Remarks

X is a one-dimensional array of type Single or Double and with even size.


---

## AutopowerFromTimeSignal Method

*Quelle: `PolyMathLib~SignalProcessing~AutopowerFromTimeSignal.html` · Polytec PolyMath Type Library · SignalProcessing Object : AutopowerFromTimeSignal Method*

### Description

Calculates an averaged autopower spectrum from the specified time signal.

### Syntax

*Visual Basic:*
```
Public Function AutopowerFromTimeSignal( _
   ByVal varInput As Variant, _
   Optional ByVal samplerateBandwidthRatio As Double = 2,5, _
   Optional ByVal lines As Long = 25, _
   Optional ByVal averageCount As Long = 0, _
   Optional ByVal overlap As Double = 0, _
   Optional ByVal varWindow As Variant _
) As Variant
```

### Parameters

varInput

One-dimensional array of Single or Double with the time signal.

samplerateBandwidthRatio

Optional ratio of the samplerate divided by the bandwidth, e.g. 2.5 (default, most systems), 2.56 for PSV-500-M and 2.4 for VibSoft-20.

lines

Optional number of FFT lines.

averageCount

Optional number of averages.

overlap

Optional overlap in percent.

varWindow

Optional one-dimensional array of Single or Double containing the window function. The size of the array must be the number of FFT lines times the samplerate / bandwidth ratio.

### Return Type

One-dimensional array of Single or Double containing the averaged autopower spectrum.

### Remarks

The function takes blocks of samples from the specified time signal, calculates FFTs, calculates the autopower sepctrum from the FFT and averages the autopower spectra. The number of samples for a single FFT is calculated from the number of FFT lines times the samplerate / bandwidth / ratio. If overlap is specified, samples of the previous FFT are reused for the next FFT. If the specified average count is 0, the function calculates the maximum number of possible averages.


---

## AverageFFTFromTimeSignal Method

*Quelle: `PolyMathLib~SignalProcessing~AverageFFTFromTimeSignal.html` · Polytec PolyMath Type Library · SignalProcessing Object : AverageFFTFromTimeSignal Method*

### Description

Calculates an averaged FFT from the specified time signal.

### Syntax

*Visual Basic:*
```
Public Function AverageFFTFromTimeSignal( _
   ByVal timeSignal As Variant, _
   Optional ByVal refSignal As Variant, _
   Optional ByVal samplerateBandwidthRatio As Double = 2,5, _
   Optional ByVal lines As Long = 25, _
   Optional ByVal averageCount As Long = 0, _
   Optional ByVal complexAverage As Boolean = False, _
   Optional ByVal overlap As Double = 0, _
   Optional ByVal varWindow As Variant _
) As Variant
```

### Parameters

timeSignal

One-dimensional array of Single or Double with the time signal.

refSignal

Optional one-dimensional array of Single or Double with the reference signal.

samplerateBandwidthRatio

Optional ratio of the samplerate divided by the bandwidth, e.g. 2.5 (default, most systems), 2.56 for PSV-500-M and 2.4 for VibSoft-20..

lines

Optional number of FFT lines.

averageCount

Optional number of averages.

complexAverage

Optional flag whether complex averages are calculated.

overlap

Optional overlap in percent.

varWindow

Optional one-dimensional array of Single or Double containing the window function. The size of the array must be the number of FFT lines times the samplerate / bandwidth ratio.

### Return Type

One-dimensional array of Single or Double containing the averaged FFT.

### Remarks

The function takes blocks of samples from the specified time signal and optional reference signal, calculates FFTs, and averages the FFTs. If complex averaging and a reference signal are specified, the phase of the resulting FFTs is calculated from the phase difference between the time signal and reference signal. The number of samples for a single FFT is calculated from the number of FFT lines times the samplerate bandwidth / ratio. If overlap is specified, samples of the previous FFT are reused for the next FFT. If the specified average count is 0, the function calculates the maximum number of possible averages.


---

## CoherenceFromTimeSignal Method

*Quelle: `PolyMathLib~SignalProcessing~CoherenceFromTimeSignal.html` · Polytec PolyMath Type Library · SignalProcessing Object : CoherenceFromTimeSignal Method*

### Description

Calculates a coherence from the specified time signal.

### Syntax

*Visual Basic:*
```
Public Function CoherenceFromTimeSignal( _
   ByVal timeSignal As Variant, _
   ByVal refSignal As Variant, _
   Optional ByVal samplerateBandwidthRatio As Double = 2,5, _
   Optional ByVal lines As Long = 25, _
   Optional ByVal averageCount As Long = 0, _
   Optional ByVal overlap As Double = 0, _
   Optional ByVal varWindow As Variant _
) As Variant
```

### Parameters

timeSignal

One-dimensional array of Single or Double with the time signal.

refSignal

One-dimensional array of Single or Double with the reference signal.

samplerateBandwidthRatio

Optional ratio of the samplerate divided by the bandwidth, e.g. 2.5 (default, most systems), 2.56 for PSV-500-M and 2.4 for VibSoft-20.

lines

Optional number of FFT lines.

averageCount

Optional number of averages.

overlap

Optional overlap in percent.

varWindow

Optional one-dimensional array of Single or Double containing the window function. The size of the array must be the number of FFT lines times the samplerate / bandwidth ratio.

### Return Type

One-dimensional array of Single or Double containing the coherence.

### Remarks

The function takes blocks of samples from the specified time signal and reference signal, calculates FFTs, autopowers and crosspowers, averages the the autopowers and crosspowers, and calculates the coherence. The phase of the resulting crosspowers is calculated from the phase difference between the time signal and reference signal. The number of samples for a single FFT is calculated from the number of FFT lines times the samplerate bandwidth / ratio. If overlap is specified, samples of the previous FFT are reused for the next FFT. If the specified average count is 0, the function calculates the maximum number of possible averages.


---

## Convolution Method

*Quelle: `PolyMathLib~SignalProcessing~Convolution.html` · Polytec PolyMath Type Library · SignalProcessing Object : Convolution Method*

### Description

Calculates the convolution of the given real vectors.

### Syntax

*Visual Basic:*
```
Public Function Convolution( _
   ByVal varInput1 As Variant, _
   ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The real input vector X.

varInput2

The real input vector Y.

### Return Type

Array of the same type as X and Y. The size of the array is 1 + abs(size1 - size2).

### Remarks

X and Y are of type Single or Double and of the same type.


---

## Crosspower Method

*Quelle: `PolyMathLib~SignalProcessing~Crosspower.html` · Polytec PolyMath Type Library · SignalProcessing Object : Crosspower Method*

### Description

Returns the cross power function from two complex spectra in a complex array.

### Syntax

*Visual Basic:*
```
Public Function Crosspower( _
   ByVal varInput1 As Variant, _
   ByVal varInput2 As Variant _
) As Variant
```

### Parameters

varInput1

The complex vector X.

varInput2

The complex vector Y.

### Return Type

One-dimensional array of the same type and size as X.

### Remarks

X and Y are one-dimensional arrays of type Single or Double of even size, same size and same type.


---

## CrosspowerFromTimeSignal Method

*Quelle: `PolyMathLib~SignalProcessing~CrosspowerFromTimeSignal.html` · Polytec PolyMath Type Library · SignalProcessing Object : CrosspowerFromTimeSignal Method*

### Description

Calculates an averaged crosspower spectrum from the specified time signal.

### Syntax

*Visual Basic:*
```
Public Function CrosspowerFromTimeSignal( _
   ByVal varInput As Variant, _
   ByVal varInputRef As Variant, _
   Optional ByVal samplerateBandwidthRatio As Double = 2,5, _
   Optional ByVal lines As Long = 25, _
   Optional ByVal averageCount As Long = 0, _
   Optional ByVal overlap As Double = 0, _
   Optional ByVal varWindow As Variant _
) As Variant
```

### Parameters

varInput

One-dimensional array of Single or Double with the time signal.

varInputRef

One-dimensional array of Single or Double with the reference signal.

samplerateBandwidthRatio

Optional ratio of the samplerate divided by the bandwidth, e.g. 2.5 (default, most systems), 2.56 for PSV-500-M and 2.4 for VibSoft-20.

lines

Optional number of FFT lines.

averageCount

Optional number of averages.

overlap

Optional overlap in percent.

varWindow

Optional one-dimensional array of Single or Double containing the window function. The size of the array must be the number of FFT lines times the samplerate / bandwidth ratio.

### Return Type

One-dimensional array of Single or Double containing the averaged crosspower.

### Remarks

The function takes blocks of samples from the specified time signal and reference signal, calculates FFTs, crosspowers, and averages the crosspowers. The phase of the resulting crosspowers is calculated from the phase difference between the time signal and reference signal. The number of samples for a single FFT is calculated from the number of FFT lines times the samplerate bandwidth / ratio. If overlap is specified, samples of the previous FFT are reused for the next FFT. If the specified average count is 0, the function calculates the maximum number of possible averages.


---

## DifferentiateTime Method

*Quelle: `PolyMathLib~SignalProcessing~DifferentiateTime.html` · Polytec PolyMath Type Library · SignalProcessing Object : DifferentiateTime Method*

### Description

Returns the differentiated time signal.

### Syntax

*Visual Basic:*
```
Public Function DifferentiateTime( _
   ByVal varInput As Variant, _
   ByVal dFrequency As Double _
) As Variant
```

### Parameters

varInput

One-dimensional array of Single or Double containing the time signal.

dFrequency

The sampling frequency in Hz.

### Remarks

The FIR filter as described in section 10.2.1 of the Theory Manual is not applied.


---

## FFT Method

*Quelle: `PolyMathLib~SignalProcessing~FFT.html` · Polytec PolyMath Type Library · SignalProcessing Object : FFT Method*

### Description

Returns the complex spectrum from a real time signal.

### Syntax

*Visual Basic:*
```
Public Function FFT( _
   ByVal varTimeSignal As Variant, _
   ByVal lLines As Long, _
   Optional ByVal varWindow As Variant _
) As Variant
```

### Parameters

varTimeSignal

One-dimensional array of Single or Double with the time signal. The size of the array must be at least 2*lLines rounded up to the next power of 2.

lLines

Desired number of lines in the spectrum. (25 to 262144000)

varWindow

Optional one-dimensional array of Single or Double containing the window function. The size of the array must be 2*lLines rounded up to the next power of 2.

### Return Type

The complex spectrum of the real time signal.

### Remarks

Specifying a window function is equivalent to:

 TimeData = Mul( TimeData, Window)
 TimeData = Sub( TimeData, Mul(Window,Mean(TimeData)))
 FreqData = FFT( TimeData, lLines)

 This is done to reduce the leakage into the first bin in the presence of a dominant signal of non-integer frequency.

 In case it is important to correctly detect low frequency signals, it is better to use the following scheme:

 TimeData = Sub( TimeData, Mean(TimeData))
 TimeData = Mul( TimeData, WindowFkt)
 FreqData = FFT( TimeData, lLines)

### Example


---

## FFTEx Method

*Quelle: `PolyMathLib~SignalProcessing~FFTEx.html` · Polytec PolyMath Type Library · SignalProcessing Object : FFTEx Method*

### Description

Returns the complex spectrum from a real time signal.

### Syntax

*Visual Basic:*
```
Public Function FFTEx( _
   ByVal timeSignal As Variant, _
   ByVal fftLines As Long, _
   ByVal samplerateBandwidthRatio As Double, _
   Optional ByVal window As Variant _
) As Variant
```

### Parameters

timeSignal

One-dimensional array of Single or Double with the time signal. The number of samples must be at least the number of FFT lines multiplied with the samplerate to bandwidth ratio.

fftLines

Desired number of lines in the spectrum. (25 to 262144000)

samplerateBandwidthRatio

The factor between the bandwidth and the sample rate. You can choose a factor of 2.0, 2.5, 2.56, 4.0, 5.0, 5.12.

window

Optional one-dimensional array of Single or Double containing the window function. The size of the array must must be the number of FFT lines multiplied with the samplerate to bandwidth ratio.

### Return Type

The complex spectrum of the real time signal.

### Remarks

Specifying a window function is equivalent to:

 TimeData = Mul( TimeData, Window)
 TimeData = Sub( TimeData, Mul(Window,Mean(TimeData)))
 FreqData = FFT( TimeData, lLines)

 This is done to reduce the leakage into the first bin in the presence of a dominant signal of non-integer frequency.

 In case it is important to correctly detect low frequency signals, it is better to use the following scheme:

 TimeData = Sub( TimeData, Mean(TimeData))
 TimeData = Mul( TimeData, WindowFkt)
 FreqData = FFT( TimeData, lLines)


---

## FilterCoefficients Method

*Quelle: `PolyMathLib~SignalProcessing~FilterCoefficients.html` · Polytec PolyMath Type Library · SignalProcessing Object : FilterCoefficients Method*

### Description

Calculates the coefficients for the specified filter. Use Convolution to apply the filter to time data.

### Syntax

*Visual Basic:*
```
Public Function FilterCoefficients( _
   ByVal ptcFilterType As PTCDigitalFilterType, _
   ByVal ptcFilterQuality As PTCDigitalFilterQuality, _
   ByVal sampleFreq As Double, _
   ByVal cutOff1 As Double, _
   Optional ByVal varCutOff2 As Variant _
) As Variant
```

### Parameters

ptcFilterType

| Value | Description |
|---|---|
| ptcDigitalFilterBandpass | Digital filter is band pass. |
| ptcDigitalFilterHighpass | Digital filter is high pass. |
| ptcDigitalFilterLowpass | Digital filter is low pass. |
| ptcDigitalFilterNone | Digital filter is none i.e. , no digital filter is set. |
| ptcDigitalFilterNotch | Digital filter is notch. |
The type of the digital filter.

ptcFilterQuality

| Value | Description |
|---|---|
| ptcDigitalFilterQualityHigh | Quality is high. |
| ptcDigitalFilterQualityLow | Quality is low. |
| ptcDigitalFilterQualityMiddle | Quality is middle. |
| ptcDigitalFilterQualityVeryHigh | Quality is very high, using 101 filter coefficients. |
| ptcDigitalFilterQualityVeryHigh200 | Quality is very high, using 201 filter coefficients. |
| ptcDigitalFilterQualityVeryHigh300 | Quality is very high, using 301 filter coefficients. |
| ptcDigitalFilterQualityVeryHigh400 | Quality is very high, using 401 filter coefficients. |
| ptcDigitalFilterQualityVeryHigh500 | Quality is very high, using 501 filter coefficients. |
| ptcDigitalFilterQualityVeryLow | Quality is very low. |
The quality of the digital filter.

sampleFreq

The sample frequency.

cutOff1

The (lower) cutoff frequency for all filter types.

varCutOff2

For the filter types bandpass and notch you have to specify a second cutoff frequency.

### Return Type

One-dimensional array of type Single. The size of the array, i.e. the number of the filter coefficients, is determined by the parameter ptcFilterQuality.

### Remarks

The returned array is symmetric and of odd size.


---

## FilterCoefficientsDouble Method

*Quelle: `PolyMathLib~SignalProcessing~FilterCoefficientsDouble.html` · Polytec PolyMath Type Library · SignalProcessing Object : FilterCoefficientsDouble Method*

### Description

Calculates the coefficients for the specified filter. Use Convolution to apply the filter to time data.

This method provides a functionality analogous to the method FilterCoefficients(...) except for that it returns the computed filter coefficients with a higher precision, as an array of type Double.

### Syntax

*Visual Basic:*
```
Public Function FilterCoefficientsDouble( _
   ByVal ptcFilterType As PTCDigitalFilterType, _
   ByVal ptcFilterQuality As PTCDigitalFilterQuality, _
   ByVal sampleFreq As Double, _
   ByVal cutOff1 As Double, _
   Optional ByVal varCutOff2 As Variant _
) As Variant
```

### Parameters

ptcFilterType

| Value | Description |
|---|---|
| ptcDigitalFilterBandpass | Digital filter is band pass. |
| ptcDigitalFilterHighpass | Digital filter is high pass. |
| ptcDigitalFilterLowpass | Digital filter is low pass. |
| ptcDigitalFilterNone | Digital filter is none i.e. , no digital filter is set. |
| ptcDigitalFilterNotch | Digital filter is notch. |
The type of the digital filter.

ptcFilterQuality

| Value | Description |
|---|---|
| ptcDigitalFilterQualityHigh | Quality is high. |
| ptcDigitalFilterQualityLow | Quality is low. |
| ptcDigitalFilterQualityMiddle | Quality is middle. |
| ptcDigitalFilterQualityVeryHigh | Quality is very high, using 101 filter coefficients. |
| ptcDigitalFilterQualityVeryHigh200 | Quality is very high, using 201 filter coefficients. |
| ptcDigitalFilterQualityVeryHigh300 | Quality is very high, using 301 filter coefficients. |
| ptcDigitalFilterQualityVeryHigh400 | Quality is very high, using 401 filter coefficients. |
| ptcDigitalFilterQualityVeryHigh500 | Quality is very high, using 501 filter coefficients. |
| ptcDigitalFilterQualityVeryLow | Quality is very low. |
The quality of the digital filter.

sampleFreq

The sample frequency.

cutOff1

The (lower) cutoff frequency for all filter types.

varCutOff2

For the filter types bandpass and notch you have to specify a second cutoff frequency.

### Return Type

One-dimensional array of type Double. The size of the array, i.e. the number of the filter coefficients, is determined by the parameter ptcFilterQuality.

### Remarks

The returned array is symmetric and of odd size.


---

## FRFFromTimeSignal Method

*Quelle: `PolyMathLib~SignalProcessing~FRFFromTimeSignal.html` · Polytec PolyMath Type Library · SignalProcessing Object : FRFFromTimeSignal Method*

### Description

Calculates the frequency response function from the specified time and reference signal.

### Syntax

*Visual Basic:*
```
Public Function FRFFromTimeSignal( _
   ByVal varInput As Variant, _
   ByVal varInputRef As Variant, _
   Optional ByVal samplerateBandwidthRatio As Double = 2,5, _
   Optional ByVal lines As Long = 25, _
   Optional ByVal varWindow As Variant _
) As Variant
```

### Parameters

varInput

One-dimensional array of Single or Double with the time signal.

varInputRef

One-dimensional array of Single or Double with the reference signal.

samplerateBandwidthRatio

Optional ratio of the samplerate divided by the bandwidth, e.g. 2.5 (default, most systems), 2.56 for PSV-500-M and 2.4 for VibSoft-20.

lines

Optional number of FFT lines.

varWindow

Optional one-dimensional array of Single or Double containing the window function. The size of the array must be the number of FFT lines times the samplerate / bandwidth ratio.

### Return Type

One-dimensional array of Single or Double containing the FRF.

### Remarks

The function takes blocks of samples from the specified time signal and reference signal, calculates FFTs, calculates autopowers and crosspowers, and the FRF. The phase of the resulting FRF is calculated from the phase difference between the time signal and reference signal. The number of samples for a single FFT is calculated from the number of FFT lines times the samplerate bandwidth / ratio.


---

## H1FromTimeSignal Method

*Quelle: `PolyMathLib~SignalProcessing~H1FromTimeSignal.html` · Polytec PolyMath Type Library · SignalProcessing Object : H1FromTimeSignal Method*

### Description

Calculates FRF H1 from the specified time and reference signal.

### Syntax

*Visual Basic:*
```
Public Function H1FromTimeSignal( _
   ByVal timeSignal As Variant, _
   ByVal refSignal As Variant, _
   Optional ByVal samplerateBandwidthRatio As Double = 2,5, _
   Optional ByVal lines As Long = 25, _
   Optional ByVal averageCount As Long = 0, _
   Optional ByVal overlap As Double = 0, _
   Optional ByVal varWindow As Variant _
) As Variant
```

### Parameters

timeSignal

One-dimensional array of Single or Double with the time signal.

refSignal

One-dimensional array of Single or Double with the reference signal.

samplerateBandwidthRatio

Optional ratio of the samplerate divided by the bandwidth, e.g. 2.5 (default, most systems), 2.56 for PSV-500-M and 2.4 for VibSoft-20.

lines

Optional number of FFT lines.

averageCount

Optional number of averages.

overlap

Optional overlap in percent.

varWindow

Optional one-dimensional array of Single or Double containing the window function. The size of the array must be the number of FFT lines times the samplerate / bandwidth ratio.

### Return Type

One-dimensional array of Single or Double containing the FRF H1.

### Remarks

The function takes blocks of samples from the specified time signal and reference signal, calculates FFTs, calculates autopowers and crosspowers, averages the the autopowers and crosspowers, and calculates the FRF H1. The phase of the resulting crosspowers is calculated from the phase difference between the time signal and reference signal. The number of samples for a single FFT is calculated from the number of FFT lines times the samplerate bandwidth / ratio. If overlap is specified, samples of the previous FFT are reused for the next FFT. If the specified average count is 0, the function calculates the maximum number of possible averages.


---

## H2FromTimeSignal Method

*Quelle: `PolyMathLib~SignalProcessing~H2FromTimeSignal.html` · Polytec PolyMath Type Library · SignalProcessing Object : H2FromTimeSignal Method*

### Description

Calculates FRF H2 from the specified time and reference signal.

### Syntax

*Visual Basic:*
```
Public Function H2FromTimeSignal( _
   ByVal timeSignal As Variant, _
   ByVal refSignal As Variant, _
   Optional ByVal samplerateBandwidthRatio As Double = 2,5, _
   Optional ByVal lines As Long = 25, _
   Optional ByVal averageCount As Long = 0, _
   Optional ByVal overlap As Double = 0, _
   Optional ByVal varWindow As Variant _
) As Variant
```

### Parameters

timeSignal

One-dimensional array of Single or Double with the time signal.

refSignal

One-dimensional array of Single or Double with the reference signal.

samplerateBandwidthRatio

Optional ratio of the samplerate divided by the bandwidth, e.g. 2.5 (default, most systems), 2.56 for PSV-500-M and 2.4 for VibSoft-20.

lines

Optional number of FFT lines.

averageCount

Optional number of averages.

overlap

Optional overlap in percent.

varWindow

Optional one-dimensional array of Single or Double containing the window function. The size of the array must be the number of FFT lines times the samplerate / bandwidth ratio.

### Return Type

One-dimensional array of Single or Double containing the FRF H2.

### Remarks

The function takes blocks of samples from the specified time signal and reference signal, calculates FFTs, calculates autopowers and crosspowers, averages the the autopowers and crosspowers, and calculates the FRF H2. The phase of the resulting crosspowers is calculated from the phase difference between the time signal and reference signal. The number of samples for a single FFT is calculated from the number of FFT lines times the samplerate bandwidth / ratio. If overlap is specified, samples of the previous FFT are reused for the next FFT. If the specified average count is 0, the function calculates the maximum number of possible averages.


---

## IntegrateTime Method

*Quelle: `PolyMathLib~SignalProcessing~IntegrateTime.html` · Polytec PolyMath Type Library · SignalProcessing Object : IntegrateTime Method*

### Description

Returns the integrated time signal.

### Syntax

*Visual Basic:*
```
Public Function IntegrateTime( _
   ByVal varInput As Variant, _
   ByVal dFrequency As Double _
) As Variant
```

### Parameters

varInput

One-dimensional array of Single or Double containing the time signal.

dFrequency

The sampling frequency in Hz.

### Remarks

The FIR filter as described in section 9.2.1 of the Theory Manual is not applied.


---

## InverseFFT Method

*Quelle: `PolyMathLib~SignalProcessing~InverseFFT.html` · Polytec PolyMath Type Library · SignalProcessing Object : InverseFFT Method*

### Description

Returns the real time signal from a complex spectrum.

### Syntax

*Visual Basic:*
```
Public Function InverseFFT( _
   ByVal varSpectrum As Variant _
) As Variant
```

### Parameters

varSpectrum

One-dimensional array of Single or Double of even size containing the complex spectrum.

### Return Type

One-dimensional array of the same type as varSpectrum.

### Remarks

If no trigger is used during measurement the phase of the Vib channel is replaced by the phase relative to the Ref channel. Calculating the inverse FFT of such a spectrum may lead to unexpected results. The same is true when the setting to copy the phase of the vibrometer channel from the frequency response function of the first reference channel is active.

### Example


---

## ResampleTime Method

*Quelle: `PolyMathLib~SignalProcessing~ResampleTime.html` · Polytec PolyMath Type Library · SignalProcessing Object : ResampleTime Method*

### Description

Returns the time signal sampled with a different sample frequency.

### Syntax

*Visual Basic:*
```
Public Function ResampleTime( _
   ByVal varInput As Variant, _
   ByVal dFrequencyOld As Double, _
   ByVal dFrequencyNew As Double _
) As Variant
```

### Parameters

varInput

One-dimensional array of Single or Double containing the time signal.

dFrequencyOld

Original sampling frequency.

dFrequencyNew

New sampling frequency.

### Return Type

Due to the anti-aliasing filter, the size of the returned array is roughly dFrequencyNew / dFrequencyOld * size of input array  25*max( 1, dFrequencyNew/dFrequencyOld). If the size of input array is smaller than the width of the required filter, an error is generated.


---

## SavGolFilter Method

*Quelle: `PolyMathLib~SignalProcessing~SavGolFilter.html` · Polytec PolyMath Type Library · SignalProcessing Object : SavGolFilter Method*

### Description

Applies a Savitzky-Golay differentiation filter to the specified data.

### Syntax

*Visual Basic:*
```
Public Function SavGolFilter( _
   ByVal input As Variant, _
   ByVal size As Long, _
   ByVal order As Long _
) As Variant
```

### Parameters

input

One-dimensional array of Single or Double containing the signal.

size

The size of the filter window, i.e., how many data points are used at the same time for the local polynomial regression. The window size must always be an odd positive integer.

order

The order of the polynomial filter coefficients (polynomial degree). The order must always be smaller than the size.

### Remarks

By applying the Savitzky-Golay filter, you smooth the signal of noise and outliers without distorting the general trend of the signal. In the filter window, a smoothed value is determined using a polynomial function.


---

## Transmission Method

*Quelle: `PolyMathLib~SignalProcessing~Transmission.html` · Polytec PolyMath Type Library · SignalProcessing Object : Transmission Method*

### Description

Calculates (the real part of) the transmission function of the filter with the given coefficients. Note that in order for the transmission function to be real, the filter kernel must be symmetric.

### Syntax

*Visual Basic:*
```
Public Function Transmission( _
   ByVal varInput As Variant, _
   ByVal lCount As Long _
) As Variant
```

### Parameters

varInput

Array of type Single or Double containing the symmetric filter kernel.

lCount

The desired number of sampling points for the transmission function.

### Return Type

One-dimensional array of the same type as varInput and size lCount. The index i corresponds to frequency i / lCount * fsampling / 2. Here fsampling is the sampling frequency.

### Example


---

## WindowFunction Method

*Quelle: `PolyMathLib~SignalProcessing~WindowFunction.html` · Polytec PolyMath Type Library · SignalProcessing Object : WindowFunction Method*

### Description

Calculates the window function of the specified type.

### Syntax

*Visual Basic:*
```
Public Function WindowFunction( _
   ByVal PTCWindowFunction As PTCWindowFunction, _
   ByVal windowCoeffsCount As Long, _
   ByVal params() As Double, _
   ByRef rmsCorrection As Double _
) As Variant
```

### Parameters

PTCWindowFunction

| Value | Description |
|---|---|
| ptcWindowFctBartlett | The window function is Bartlett. |
| ptcWindowFctBlackmanHarris | The window function is Blackman Harris. |
| ptcWindowFctExponential | The window function is exponential. |
| ptcWindowFctFlatTop | The window function is flat top. |
| ptcWindowFctForce | The window function is force. |
| ptcWindowFctHamming | The window function is Hamming. |
| ptcWindowFctHanning | The window function is Hanning. |
| ptcWindowFctRectangle | The window function is rectangle. |
| ptcWindowFctTaperedHanning | The window function is tapered Hanning. |
The type of the window function.

windowCoeffsCount

The number of the window function samples to compute.

params

Additional parameters for some window types.

rmsCorrection

The output parameter for the computed RMS correction factor.

### Return Type

One-dimensional array of type Single containing the samples of the normalized window function (mean value of 1).


---

## WindowFunctionDouble Method

*Quelle: `PolyMathLib~SignalProcessing~WindowFunctionDouble.html` · Polytec PolyMath Type Library · SignalProcessing Object : WindowFunctionDouble Method*

### Description

Calculates the window function of the specified type.

This method provides a functionality analogous to the method WindowFunction(...) except for that it returns the computed window function samples with a higher precision, as an array of type Double.

### Syntax

*Visual Basic:*
```
Public Function WindowFunctionDouble( _
   ByVal PTCWindowFunction As PTCWindowFunction, _
   ByVal windowCoeffsCount As Long, _
   ByVal params() As Double, _
   ByRef rmsCorrection As Double _
) As Variant
```

### Parameters

PTCWindowFunction

| Value | Description |
|---|---|
| ptcWindowFctBartlett | The window function is Bartlett. |
| ptcWindowFctBlackmanHarris | The window function is Blackman Harris. |
| ptcWindowFctExponential | The window function is exponential. |
| ptcWindowFctFlatTop | The window function is flat top. |
| ptcWindowFctForce | The window function is force. |
| ptcWindowFctHamming | The window function is Hamming. |
| ptcWindowFctHanning | The window function is Hanning. |
| ptcWindowFctRectangle | The window function is rectangle. |
| ptcWindowFctTaperedHanning | The window function is tapered Hanning. |
The type of the window function.

windowCoeffsCount

The number of the window function samples to compute.

params

Additional parameters for some window types.

rmsCorrection

The output parameter for the computed RMS correction factor.

### Return Type

One-dimensional array of type Double containing the samples of the normalized window function (mean value of 1).
