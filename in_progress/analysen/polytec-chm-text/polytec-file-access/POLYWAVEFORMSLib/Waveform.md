# POLYWAVEFORMSLib – Waveform

## Waveform Object

*Quelle: `POLYWAVEFORMSLib~Waveform.html` · Polytec PolyWaveforms Type Library*

### Description

Waveform is the base object of the objects WaveformBurstChirp, WaveformBurstRandom, WaveformMultiCarrierCW, WaveformPeriodicChirp, WaveformPseudoRandom, WaveformRamp, WaveformSimple, WaveformSine, WaveformSquare, WaveformSteppedSineSweep, WaveformSweep, WaveformTriangle, WaveformUserDefined, WaveformWhiteNoise.

### Remarks

You cannot create a waveform object directly. Create an object of one of the derived objects instead. Any of the derived objects can be used instead of a waveform object, e.g. when setting the GeneratorAcqProperties.Waveform property.

### Example

For an example see the GeneratorAcqProperties.Waveform property.


---

## Waveform Object Members

*Quelle: `POLYWAVEFORMSLib~Waveform_members.html` · Polytec PolyWaveforms Type Library*

### Public Properties

| Name | The name of the waveform. |
|---|---|
| Type | The type of the waveform. |


---

## Name Property

*Quelle: `POLYWAVEFORMSLib~Waveform~Name.html` · Polytec PolyWaveforms Type Library · Waveform Object : Name Property*

### Description

The name of the waveform.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `POLYWAVEFORMSLib~Waveform~Type.html` · Polytec PolyWaveforms Type Library · Waveform Object : Type Property*

### Description

The type of the waveform.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCWaveformType
```
