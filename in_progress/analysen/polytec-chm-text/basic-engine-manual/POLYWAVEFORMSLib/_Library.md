# POLYWAVEFORMSLib – _Library

## Project Overview

*Quelle: `POLYWAVEFORMSLib_P.html` · Polytec PolyWaveforms Type Library*

### Description

The Polytec PolyWaveforms type library contains objects describing the waveforms of the generator of a MPV/PSV/VibSoft system. You can find out which waveform with which parameters was used during data acquisition. On MPV/PSV/VibSoft systems you can control the attached generator by selecting a different waveform or changing the parameters of the current waveform.

### Classes

| Class Module | Description |
|---|---|
| Waveform | Waveform is the base object of the objects WaveformBurstChirp , WaveformBurstRandom , WaveformMultiCarrierCW , WaveformPeriodicChirp , WaveformPseudoRandom , WaveformRamp , WaveformSimple , WaveformSine , WaveformSquare , WaveformSteppedSineSweep , WaveformSweep , WaveformTriangle , WaveformUserDefined , WaveformWhiteNoise . |
| WaveformBurstChirp | The burst chirp waveform object. |
| WaveformBurstRandom | The burst random waveform object. |
| WaveformMultiCarrierCW | The multi-carrier-CW waveform of the SMBV100A/B signal generator of PSV-UHF, VibSoft-UHF, MSA-600-U and some MSA-600-S systems. |
| WaveformPeriodicChirp | The periodic chirp waveform object. |
| WaveformPseudoRandom | The pseudo random waveform object. |
| WaveformRamp | The ramp waveform object. |
| WaveformSimple | Waveform simple is the base object of the objects WaveformSine , WaveformSquare , WaveformTriangle, WaveformRamp , WaveformUserDefined Object . |
| WaveformSine | The sine waveform object. |
| WaveformSquare | The square waveform object. |
| WaveformSteppedSineSweep | The stepped sine sweep waveform object. |
| WaveformSweep | The sweep waveform object. |
| WaveformTriangle | The triangle waveform object. |
| WaveformUserDefined | The user-defined waveform. |
| WaveformWhiteNoise | The white noise waveform object. |

### Interfaces

| Class Module | Description |
|---|---|
| IWaveform | Waveform is the base object of the objects WaveformBurstChirp , WaveformBurstRandom , WaveformMultiCarrierCW Object , WaveformPeriodicChirp , WaveformPseudoRandom , WaveformRamp , WaveformSimple , WaveformSine , WaveformSquare , WaveformSteppedSineSweep , WaveformSweep , WaveformTriangle , WaveformUserDefined and WaveformWhiteNoise |

### Public Enumerations

| Enumeration | Description |
|---|---|
| PTCWaveformType | The type of the waveform. |


---

## References

*Quelle: `POLYWAVEFORMSLib_references.html` · Polytec PolyWaveforms Type Library*


