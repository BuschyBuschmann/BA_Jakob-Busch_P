# POLYFILELib – PTCScanStatus

## PTCScanStatus Enumeration

*Quelle: `POLYFILELib~PTCScanStatus.html` · Polytec PolyFile Type Library*

### Description

Scan status of a scan point. The status can be a combination of several bit constants defined in the enumeration.

### Members

| Member | Value | Description |
|---|---|---|
| ptcScanStatusAssignedChannel1D | 2048 | Point mapped to a 1D channel, usable only with MPV files. |
| ptcScanStatusAssignedChannel3D | 4096 | Point mapped to a 3D channel, usable only with MPV files. |
| ptcScanStatusAssignedSensor | 8192 | Point mapped to a sensor, usable only with MPV files. |
| ptcScanStatusDisabled | 16 | Point is disabled for scan. |
| ptcScanStatusHidden | 128 | Point is hidden by the 3D geometry. |
| ptcScanStatusInterpolate | 512 | The data at the point shall be interpolated from the data of its neighbors. |
| ptcScanStatusInterpolationFailed | 1024 | The interpolation of the data of this point failed. |
| ptcScanStatusInvalidated | 8 | Point is invalidated. |
| ptcScanStatusInvalidFrames | 32 | Point has invalid frames (MultiFrame only). |
| ptcScanStatusNone | 0 | Point is not measured. |
| ptcScanStatusNotReachable | 64 | Point was not reachable by the scanner. |
| ptcScanStatusOptimal | 2 | Point is optimal (Signal Enhancement only). |
| ptcScanStatusOverrange | 4 | Point has overrange status. |
| ptcScanStatusValid | 1 | Point is valid. |
| ptcScanStatusVideoTriangulationFailed | 256 | The video-triangulation failed for this point. |
