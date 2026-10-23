# PSV – GeneratorAcqProperties

## GeneratorAcqProperties Object

*Quelle: `PSV~GeneratorAcqProperties.html` · Polytec PSV Type Library*

### Description

The generator acquisition properties. Item of the GeneratorsAcquisitonProperties collection.

### Object Model


---

## GeneratorAcqProperties Object Members

*Quelle: `PSV~GeneratorAcqProperties_members.html` · Polytec PSV Type Library*

### Public Methods

| LoadAmplitudeCorrectionData | Loads the amplitude correction data from the specified file. |
|---|---|

### Public Properties

| Active | Specifies, whether the generator is active. |
|---|---|
| ActiveChannels | Specifies which channels of the signal generator are active. |
| Amplitude | The amplitude of the generator signal in Volt. |
| AmplitudeCorrectionData | The amplitude correction data of the generator signal. |
| MultipleChannels | Specifies, whether the generator uses multiple channels for output. |
| Offset | Specifies the offset of the generator signal in Volt. |
| SteadyStateTime | Specifies the waiting time for steady state conditions in second. |
| SupportsMultipleChannels | Returns true, if the generator supports multiple channels. |
| UseAmplitudeCorrection | Specifies, whether the amplitude correction data is used. |
| Waveform | Specifies the waveform of the generator. |


---

## LoadAmplitudeCorrectionData Method

*Quelle: `PSV~GeneratorAcqProperties~LoadAmplitudeCorrectionData.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : LoadAmplitudeCorrectionData Method*

### Description

Loads the amplitude correction data from the specified file.

### Syntax

*Visual Basic:*
```
Public Sub LoadAmplitudeCorrectionData( _
   ByVal bstrFileName As String _
)
```

### Parameters

bstrFileName

The file name.


---

## Active Property

*Quelle: `PSV~GeneratorAcqProperties~Active.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : Active Property*

### Description

Specifies, whether the generator is active.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Active As Boolean
```


---

## ActiveChannels Property

*Quelle: `PSV~GeneratorAcqProperties~ActiveChannels.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : ActiveChannels Property*

### Description

Specifies which channels of the signal generator are active.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ActiveChannels As PTCGeneratorActiveChannelType
```

### Return Type

A combination of the flags defined by the PTCGeneratorActiveChannelType Enumeration.

### Remarks

The user interface of the software supports only the values for channel 1 and all channels.


---

## Amplitude Property

*Quelle: `PSV~GeneratorAcqProperties~Amplitude.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : Amplitude Property*

### Description

The amplitude of the generator signal in Volt.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Amplitude As Double
```


---

## AmplitudeCorrectionData Property

*Quelle: `PSV~GeneratorAcqProperties~AmplitudeCorrectionData.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : AmplitudeCorrectionData Property*

### Description

The amplitude correction data of the generator signal.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AmplitudeCorrectionData As Double()
```


---

## MultipleChannels Property

*Quelle: `PSV~GeneratorAcqProperties~MultipleChannels.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : MultipleChannels Property*

### Description

Specifies, whether the generator uses multiple channels for output.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MultipleChannels As Boolean
```

### Remarks

This property is not available on VibroScan systems. On these systems use the ActiveChannels Property instead.


---

## Offset Property

*Quelle: `PSV~GeneratorAcqProperties~Offset.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : Offset Property*

### Description

Specifies the offset of the generator signal in Volt.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Offset As Double
```


---

## SteadyStateTime Property

*Quelle: `PSV~GeneratorAcqProperties~SteadyStateTime.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : SteadyStateTime Property*

### Description

Specifies the waiting time for steady state conditions in second.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SteadyStateTime As Double
```


---

## SupportsMultipleChannels Property

*Quelle: `PSV~GeneratorAcqProperties~SupportsMultipleChannels.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : SupportsMultipleChannels Property*

### Description

Returns true, if the generator supports multiple channels.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SupportsMultipleChannels As Boolean
```


---

## UseAmplitudeCorrection Property

*Quelle: `PSV~GeneratorAcqProperties~UseAmplitudeCorrection.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : UseAmplitudeCorrection Property*

### Description

Specifies, whether the amplitude correction data is used.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property UseAmplitudeCorrection As Boolean
```


---

## Waveform Property

*Quelle: `PSV~GeneratorAcqProperties~Waveform.html` · Polytec PSV Type Library · GeneratorAcqProperties Object : Waveform Property*

### Description

Specifies the waveform of the generator.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Waveform As IWaveform
```

### Remarks

The property returns an object that is the base object of various objects describing different waveforms. You have to cast to the specific waveform to retrieve the specific information about this waveform.
