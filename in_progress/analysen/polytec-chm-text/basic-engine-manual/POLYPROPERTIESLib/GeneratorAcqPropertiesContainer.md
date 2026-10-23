# POLYPROPERTIESLib – GeneratorAcqPropertiesContainer

## GeneratorAcqPropertiesContainer Object

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer.html` · Polytec PolyProperties Type Library*

### Description

The generator acquisition properties. Item of the GeneratorsAcquisitonProperties collection.

### Object Model


---

## GeneratorAcqPropertiesContainer Object Members

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer_members.html` · Polytec PolyProperties Type Library*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~LoadAmplitudeCorrectionData.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : LoadAmplitudeCorrectionData Method*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~Active.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : Active Property*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~ActiveChannels.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : ActiveChannels Property*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~Amplitude.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : Amplitude Property*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~AmplitudeCorrectionData.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : AmplitudeCorrectionData Property*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~MultipleChannels.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : MultipleChannels Property*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~Offset.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : Offset Property*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~SteadyStateTime.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : SteadyStateTime Property*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~SupportsMultipleChannels.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : SupportsMultipleChannels Property*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~UseAmplitudeCorrection.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : UseAmplitudeCorrection Property*

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

*Quelle: `POLYPROPERTIESLib~GeneratorAcqPropertiesContainer~Waveform.html` · Polytec PolyProperties Type Library · GeneratorAcqPropertiesContainer Object : Waveform Property*

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

### Example

The example shows how to retrieve information about the generator waveform that was active when the measurement of the given file was made.

- Retrieve Generator Waveform Info (Visual Basic)

```
'#Language "WWB.NET"

Option Explicit

Sub Main
    Dim oFile As New PolyFile
    oFile.Open("C:\ProgramData\Polytec\PSV\10.4\Examples\Data\Example.svd")

    Dim oAcqInfos As AcquisitionInfoModes
    oAcqInfos = oFile.Infos.Type(PTCInfoType.ptcInfoAcquisition)

    Dim oAcqProps As AcquisitionPropertiesContainer
    oAcqProps = oAcqInfos.ActiveProperties

    Dim oGeneratorsAcqProps As GeneratorsAcqPropertiesContainer
    oGeneratorsAcqProps = oAcqProps(PTCAcqPropertiesType.ptcAcqPropertiesTypeGenerators)

    Dim oGeneratorAcqProps As GeneratorAcqProperties
    oGeneratorAcqProps = oGeneratorsAcqProps(1)

    Dim oWaveform As Waveform
    oWaveform = oGeneratorAcqProps.Waveform

    Debug.Print "Waveform Name: ";oWaveform.Name

    Select Case oWaveform.type
    Case PTCWaveformType.ptcWaveformSine
        Dim oSine As WaveformSine = oWaveform
        Debug.Print "Sine Frequency: ";oSine.Frequency
    Case PTCWaveformType.ptcWaveformSquare
        Dim oSquare As WaveformSquare = oWaveform
        Debug.Print "Square Frequency: ";oSquare.Frequency
    Case PTCWaveformType.ptcWaveformTriangle
        Dim oTriangle As WaveformTriangle = oWaveform
        Debug.Print "Triangle Frequency: ";oTriangle.Frequency
    Case PTCWaveformType.ptcWaveformRamp
        Dim oRamp As WaveformRamp = oWaveform
        Debug.Print "Ramp Frequency: ";oRamp.Frequency
    Case PTCWaveformType.ptcWaveformSweep
        Dim oSweep As WaveformSweep = oWaveform
        Debug.Print "Sweep StartFrequency: ";oSweep.StartFrequency
        Debug.Print "Sweep EndFrequency: ";oSweep.EndFrequency
        Debug.Print "Sweep SweepTime: ";oSweep.SweepTime
    Case PTCWaveformType.ptcWaveformBurstChirp
        Dim oBurstChirp As WaveformBurstChirp = oWaveform
        Debug.Print "BurstChirp StartFrequency: ";oBurstChirp.StartFrequency
        Debug.Print "BurstChirp EndFrequency: ";oBurstChirp.EndFrequency
        Debug.Print "BurstChirp BurstStart: ";oBurstChirp.BurstStart
        Debug.Print "BurstChirp BurstLength: ";oBurstChirp.BurstLength
    Case PTCWaveformType.ptcWaveformBurstRandom
        Dim oBurstRandom As WaveformBurstRandom = oWaveform
        Debug.Print "BurstRandom BurstStart: ";oBurstRandom.BurstStart
        Debug.Print "BurstRandom BurstLength: ";oBurstRandom.BurstLength
    Case PTCWaveformType.ptcWaveformPeriodicChirp
        Dim oPeriodicChirp As WaveformPeriodicChirp = oWaveform
        ' Periodic Chirp has no additional properties
    Case PTCWaveformType.ptcWaveformPseudoRandom
        Dim oPseudoRandom As WaveformPseudoRandom = oWaveform
        ' Pseudo Random has no additional properties
    Case PTCWaveformType.ptcWaveformWhiteNoise
        Dim oWhiteNoise As WaveformWhiteNoise = oWaveform
        ' White Noise has no additional properties
    Case PTCWaveformType.ptcWaveformMultiCarrierCW
        Dim oMultiCarrierCW As WaveformMultiCarrierCW = oWaveform
        Debug.Print "MultiCarrierCW StartFrequency: ";oMultiCarrierCW.StartFrequency
        Debug.Print "MultiCarrierCW EndFrequency: "; oMultiCarrierCW.EndFrequency
    Case PTCWaveformType.ptcWaveformSteppedSineSweep
		Dim oSteppedSineSwee As WaveformSteppedSineSweep = oWaveform
        Debug.Print "SteppedSineSweep StartFrequency: "; oSteppedSineSwee.StartFrequency
        Debug.Print "SteppedSineSweep FrequencyStep: "; oSteppedSineSwee.FrequencyStep
        Debug.Print "SteppedSineSweep EndFrequency: "; oSteppedSineSwee.EndFrequency
    Case PTCWaveformType.ptcWaveformUserDefined
        Dim oUserDefined As WaveformWhiteNoise = oWaveform
        ' User-defined has no additional properties
    End Select

    oFile.Close()
End Sub
```
