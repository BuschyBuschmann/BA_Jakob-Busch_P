# POLYSIGNALLib – PTCSignalListBuildFlags

## PTCSignalListBuildFlags Enumeration

*Quelle: `POLYSIGNALLib~PTCSignalListBuildFlags.html` · Polytec PolySignal Type Library*

### Description

The build flags for the signal list.

### Members

| Member | Value | Description |
|---|---|---|
| ptcBuild3d | 32 | The 3D signals will be listed under 3D channels. 3D user signals are listed under Usr 3D channel and 1D user signal are listed under Usr channel. |
| ptcBuild3rdOctaveDomain | 1 | If it exists, the third octave domain will be added. |
| ptcBuildComplexDisplay | 2 | Complex displays will be added. |
| ptcBuildDefault | 23 | A combination of ptcBuild3rdOctaveDomain ptcBuildComplexDisplay, ptcBuildNyquistDisplay, ptcBuildPhaseDisplay serves for the most purposes. |
| ptcBuildInstValDisplay | 8 | The instantaneous value display will be added. |
| ptcBuildNone | 0 | No build flags. |
| ptcBuildNyquistDisplay | 4 | The Nyquist display will be added. |
| ptcBuildPhaseDisplay | 16 | The phase display will be added. |
| ptcBuildUser | 64 | The Usr channel will be added. All 3D and 1D user signals are listed under Usr channel. |
| ptcBuildUserSpectrum | 256 | An empty FFT domain will be added, if it does not already exist, to be used to add user signals. |
| ptcBuildUserTime | 512 | An empty time domain will be added, if it does not already exist, to be used to add user signals. |
| ptcBuildXYZ | 128 | Add 1D signals. 3D user signals will be added under Usr X, Usr Y and Usr Z channels. |

### Remarks

The flag ptcBuildXYZ can't be combined with ptcBuild3d.
