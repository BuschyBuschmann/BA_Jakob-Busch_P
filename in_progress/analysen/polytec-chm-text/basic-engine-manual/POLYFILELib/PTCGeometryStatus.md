# POLYFILELib – PTCGeometryStatus

## PTCGeometryStatus Enumeration

*Quelle: `POLYFILELib~PTCGeometryStatus.html` · Polytec PolyFile Type Library*

### Description

Geometry status of a scan point. The status can be a combination of several bit constants defined in the enumeration.

### Members

| Member | Value | Description |
|---|---|---|
| ptcGeoStatusCalculated2dFrom3d | 4096 | 2D coordinate (video coordinate) was calculated from the 3D coordinate using the 2D alignment. |
| ptcGeoStatusCalculated3dFrom2d | 2048 | 3D coordinate was calculated from the 2D coordinate (video coordinate), e.g. when using PSV-UHF. |
| ptcGeoStatusCalculated3dFrom2dAndDistance | 16384 | 3D coordinate was calculated from the 2D coordinate (video coordinate), the corresponding scanner angles and the distance to the measurement object. |
| ptcGeoStatusFailed | 512 | Measurement of 3D coordinate has failed. |
| ptcGeoStatusImported | 8 | 3D coordinate was imported (UFF or MEScope). |
| ptcGeoStatusInterpolated | 32 | 3D coordinate was interpolated by valid neighbors. |
| ptcGeoStatusMeasured | 4 | 3D coordinate was measured with the geometry scan unit (PSV-A-420). |
| ptcGeoStatusModified | 64 | 3D coordinate was modified by user. |
| ptcGeoStatusNone | 0 | Point has no 3D coordinate. |
| ptcGeoStatusOptimalMeasured | 1024 | 3D coordinate was measured with the geometry scan unit (PSV-A-420) with optimal signal level. |
| ptcGeoStatusTooBright | 128 | No valid 3D coordinate. Too much light (PSV-A-420). |
| ptcGeoStatusTooDark | 256 | No valid 3D coordinate. Too little light (PSV-A-420). |
| ptcGeoStatusTriangulation | 16 | 3D coordinate was calculated by PSV-3D triangulation (PSV-3D only). |
| ptcGeoStatusValid | 1 | Point has a valid 3D coordinate. |
| ptcGeoStatusVideoTriangulated | 8192 | 3D coordinate was calculated by video-triangulation. |
