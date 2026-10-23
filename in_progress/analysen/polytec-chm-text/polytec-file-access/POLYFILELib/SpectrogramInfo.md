# POLYFILELib – SpectrogramInfo

## SpectrogramInfo Object

*Quelle: `POLYFILELib~SpectrogramInfo.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos Collection. Contains information about the parameters for a spectrogram or Campbell diagram that can be calculated from time traces.

### Remarks

This item is present in .scd (Spectrogram Campbell Data) files and .scs (Spectrogram Campbell Settings) files.


---

## SpectrogramInfo Object Members

*Quelle: `POLYFILELib~SpectrogramInfo_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Copy | Copies the parameters from the specified spectrogram info object. |
|---|---|

### Public Properties

| Bandwidth | The bandwidth for the calculation of FFTs for the spectrogram or Campbell diagram in Hz. |
|---|---|
| BandwidthFrom | The lower limit for the bandwidth for the calculation of FFTs for the spectrogram or Campbell diagram in Hz. |
| BandwidthTo | The upper limit for the bandwidth for the calculation of FFTs for the spectrogram or Campbell diagram in Hz. |
| EffectiveSampleCount | The effective number of samples that will be used for calculating FFTs. |
| EnforceOrder | Enforces increasing or decreasing order of the RPM values of Campbell diagrams. |
| FFTCount | The number of FFTs in the resulting spectrogram or Campbell diagram. |
| FFTLines | The number of FFT lines. |
| FrequencyResolution | The frequency resolution in Hz. |
| Name | Returns "Spectrogram". This can be used as an index to the Infos collection . |
| Overlap | The overlap of the FFTs in percent. |
| RPMChannel | The name of the channel that is used to extract the RPM signal. |
| SampleCount | The number of samples used to calculate an FFT. |
| SampleRate | The sample rate of the time trace in Hz. |
| SampleRateBandwidthRatio | The ratio between the sample rate and the bandwidth. |
| SignalSmoothing | Set to true to smooth the RPM signal if your data contains too much noise. |
| TimeFrom | The start of the time range taken into account for calculating the spectrogram or Campbell diagram. |
| TimeTo | The end of the time range taken into account for calculating the spectrogram or Campbell diagram. |
| TotalSampleCount | The total number of samples available in the time trace. |
| Type | The spectrogram type. |
| UsedFFTLines | The number of used FFT lines. |
| WindowFunction | The window function applied to the time trace before calculating the FFT. |
| WindowParameter | The parameters of the window function applied to the time trace before calculating the FFT. |


---

## Copy Method

*Quelle: `POLYFILELib~SpectrogramInfo~Copy.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : Copy Method*

### Description

Copies the parameters from the specified spectrogram info object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal srcSpectrogramInfo As SpectrogramInfo _
)
```

### Parameters

srcSpectrogramInfo

The spectrogram info to copy the parameters from.


---

## Bandwidth Property

*Quelle: `POLYFILELib~SpectrogramInfo~Bandwidth.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : Bandwidth Property*

### Description

The bandwidth for the calculation of FFTs for the spectrogram or Campbell diagram in Hz.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Bandwidth As Double
```

### Return Type

The bandwidth in Hz.


---

## BandwidthFrom Property

*Quelle: `POLYFILELib~SpectrogramInfo~BandwidthFrom.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : BandwidthFrom Property*

### Description

The lower limit for the bandwidth for the calculation of FFTs for the spectrogram or Campbell diagram in Hz.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property BandwidthFrom As Double
```

### Return Type

The lower limit for the bandwidth in Hz.

### Remarks

You can limit the frequency range that will be present in the spectrogram or Campbell diagram by specifying limits on the bandwidth. This will reduce the number of FFT lines accordingly.


---

## BandwidthTo Property

*Quelle: `POLYFILELib~SpectrogramInfo~BandwidthTo.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : BandwidthTo Property*

### Description

The upper limit for the bandwidth for the calculation of FFTs for the spectrogram or Campbell diagram in Hz.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property BandwidthTo As Double
```

### Return Type

The upper limit for the bandwidth in Hz.

### Remarks

You can limit the frequency range that will be present in the spectrogram or Campbell diagram by specifying limits on the bandwidth. This will reduce the number of FFT lines accordingly.


---

## EffectiveSampleCount Property

*Quelle: `POLYFILELib~SpectrogramInfo~EffectiveSampleCount.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : EffectiveSampleCount Property*

### Description

The effective number of samples that will be used for calculating FFTs.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property EffectiveSampleCount As Long
```

### Remarks

The overlap is taken into account. If e.g., FFTs with 800 llines are calculated with an overlap of 50% the effective sample count is 400.


---

## EnforceOrder Property

*Quelle: `POLYFILELib~SpectrogramInfo~EnforceOrder.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : EnforceOrder Property*

### Description

Enforces increasing or decreasing order of the RPM values of Campbell diagrams.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property EnforceOrder As Boolean
```

### Return Type

True if the order is enforced.

### Remarks

Note that setting this property to true might result in a change of your measurement data.


---

## FFTCount Property

*Quelle: `POLYFILELib~SpectrogramInfo~FFTCount.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : FFTCount Property*

### Description

The number of FFTs in the resulting spectrogram or Campbell diagram.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FFTCount As Long
```

### Return Type

The number of FFTs.


---

## FFTLines Property

*Quelle: `POLYFILELib~SpectrogramInfo~FFTLines.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : FFTLines Property*

### Description

The number of FFT lines.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FFTLines As Long
```

### Return Type

The number of FFT lines.


---

## FrequencyResolution Property

*Quelle: `POLYFILELib~SpectrogramInfo~FrequencyResolution.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : FrequencyResolution Property*

### Description

The frequency resolution in Hz.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrequencyResolution As Double
```

### Return Type

The frequency resolution in Hz.

### Remarks

The frequency resolution depends on the bandwidth and the number of FFT lines.


---

## Name Property

*Quelle: `POLYFILELib~SpectrogramInfo~Name.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : Name Property*

### Description

Returns "Spectrogram". This can be used as an index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "Spectrogram".


---

## Overlap Property

*Quelle: `POLYFILELib~SpectrogramInfo~Overlap.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : Overlap Property*

### Description

The overlap of the FFTs in percent.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Overlap As Double
```

### Remarks

For a given number of samples the higher the overlap the higher the resulting FFT count.


---

## RPMChannel Property

*Quelle: `POLYFILELib~SpectrogramInfo~RPMChannel.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : RPMChannel Property*

### Description

The name of the channel that is used to extract the RPM signal.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RPMChannel As String
```

### Remarks

Setting the property is mandatory for Campbell diagrams.


---

## SampleCount Property

*Quelle: `POLYFILELib~SpectrogramInfo~SampleCount.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : SampleCount Property*

### Description

The number of samples used to calculate an FFT.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SampleCount As Long
```

### Remarks

The number of samples returned depends on the number of FFT lines and the sample rate to bandwidth ratio.


---

## SampleRate Property

*Quelle: `POLYFILELib~SpectrogramInfo~SampleRate.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : SampleRate Property*

### Description

The sample rate of the time trace in Hz.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SampleRate As Double
```


---

## SampleRateBandwidthRatio Property

*Quelle: `POLYFILELib~SpectrogramInfo~SampleRateBandwidthRatio.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : SampleRateBandwidthRatio Property*

### Description

The ratio between the sample rate and the bandwidth.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SampleRateBandwidthRatio As Double
```

### Remarks

The ratio depends on the data acquisition system used to acquire the time trace. A typical value is 2.5, i.e. a sample rate of 25 kHz results in bandwidth of 10 kHz.


---

## SignalSmoothing Property

*Quelle: `POLYFILELib~SpectrogramInfo~SignalSmoothing.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : SignalSmoothing Property*

### Description

Set to true to smooth the RPM signal if your data contains too much noise.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SignalSmoothing As Boolean
```

### Return Type

True if the RPM signal is smoothed.


---

## TimeFrom Property

*Quelle: `POLYFILELib~SpectrogramInfo~TimeFrom.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : TimeFrom Property*

### Description

The start of the time range taken into account for calculating the spectrogram or Campbell diagram.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property TimeFrom As Double
```

### Return Type

The start of the time range in seconds.


---

## TimeTo Property

*Quelle: `POLYFILELib~SpectrogramInfo~TimeTo.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : TimeTo Property*

### Description

The end of the time range taken into account for calculating the spectrogram or Campbell diagram.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property TimeTo As Double
```

### Return Type

The end of the time range in seconds.


---

## TotalSampleCount Property

*Quelle: `POLYFILELib~SpectrogramInfo~TotalSampleCount.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : TotalSampleCount Property*

### Description

The total number of samples available in the time trace.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property TotalSampleCount As Long
```

### Remarks

The number of samples taken into account for the calculation of the spectrogram or Campbell diagram depends on the time range specified by the TimeFrom Property and TimeTo Property.


---

## Type Property

*Quelle: `POLYFILELib~SpectrogramInfo~Type.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : Type Property*

### Description

The spectrogram type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

ptcInfoSpectrogram


---

## UsedFFTLines Property

*Quelle: `POLYFILELib~SpectrogramInfo~UsedFFTLines.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : UsedFFTLines Property*

### Description

The number of used FFT lines.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property UsedFFTLines As Long
```

### Remarks

The number of FFT lines after applying the limit specified in the BandwidthFrom Property and BandwidthTo Property.


---

## WindowFunction Property

*Quelle: `POLYFILELib~SpectrogramInfo~WindowFunction.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : WindowFunction Property*

### Description

The window function applied to the time trace before calculating the FFT.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property WindowFunction As PTCWindowFunction
```


---

## WindowParameter Property

*Quelle: `POLYFILELib~SpectrogramInfo~WindowParameter.html` · Polytec PolyFile Type Library · SpectrogramInfo Object : WindowParameter Property*

### Description

The parameters of the window function applied to the time trace before calculating the FFT.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property WindowParameter As Double
```
