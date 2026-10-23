# POLYSIGNALLib – PTCSignalBuildFlags

## PTCSignalBuildFlags Enumeration

*Quelle: `POLYSIGNALLib~PTCSignalBuildFlags.html` · Polytec PolySignal Type Library*

### Description

The build flags for the signal list. Specify these flags as parameters for the GetPointDomains Method, the GetPointAverageDomains Method or the GetBandDomains Method, respectively.

### Members

| Member | Value | Description |
|---|---|---|
| ptcBuildBandData3d | 591679 | Combination of build flags for band data and 3d channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannel3d Or ptcBuildDisplayComplex Or ptcBuildDisplayPhase |
| ptcBuildBandDataXYZ | 592703 | Combination of build flags for band data and x,y,z channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannelXYZ Or ptcBuildDisplayComplex Or ptcBuildDisplayPhase |
| ptcBuildChannel3d | 1024 | Build the 3d channels (Usr 3D and/or Vib 3D). |
| ptcBuildChannelOriginal | 256 | Build the channels with the original signals. |
| ptcBuildChannelUser | 512 | Build the channel Usr. |
| ptcBuildChannelXYZ | 2048 | Build the x,y,z channels (Usr X, Usr Y, Usr Z and/or Vib X, Vib Y, Vib Z). |
| ptcBuildDisplayComplex | 65536 | Build complex displays (e.g. Real & Imag., Mag. & Phase). |
| ptcBuildDisplayInstVal | 262144 | Build display Inst. Val. |
| ptcBuildDisplayNyquist | 131072 | Build display Nyquist. |
| ptcBuildDisplayPhase | 524288 | Build display phase. |
| ptcBuildDomain3rdOctave | 32 | Build domain 3rd Octave. |
| ptcBuildDomainAll | 63 | Build all domains. |
| ptcBuildDomainAngleSync | 8 | Build domain Angle Sync. |
| ptcBuildDomainOrderSpectrum | 16 | Build domain Order Spectrum. |
| ptcBuildDomainRms | 4 | Build domain RMS. |
| ptcBuildDomainSpectrum | 2 | Build domain Spectrum. |
| ptcBuildDomainTime | 1 | Build domain Time. |
| ptcBuildNothing | 0 | No build flags set. |
| ptcBuildPointData3d | 722751 | Combination of build flags for point data or point average data and 3d channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannel3d Or ptcBuildDisplayComplex Or ptcBuildDisplayNyquist Or ptcBuildDisplayPhase |
| ptcBuildPointDataXYZ | 723775 | Combination of build flags for point data or point average data and x,y,z channels: ptcBuildDomainAll Or ptcBuildChannelOriginal Or ptcBuildChannelUser Or ptcBuildChannelXYZ Or ptcBuildDisplayComplex Or ptcBuildDisplayNyquist Or ptcBuildDisplayPhase |

### Remarks

To add user-defined signals, you should use either ptcBuildPointData3d or ptcBuildBandData3d because user-defined 3d signals can only be added to the Usr 3D channel. In any case you have to specify either ptcBuildChannel3d or ptcBuildPointDataXYZ but not both or none of these two flags.

### Example
