# PSV – PTCGeometryScanCaps

## PTCGeometryScanCaps Enumeration

*Quelle: `PSV~PTCGeometryScanCaps.html` · Polytec PSV Type Library*

### Description

Specifies how the software performs a geometry scan.

### Members

| Member | Value | Description |
|---|---|---|
| ptcGeometryScanCapsNone | 0 | The geometry scan is performed for all scan points and without refining the measured distances using the focusing unit. |
| ptcGeometryScanCapsRefineWithAutoFocus | 2 | Uses the focusing unit of the scanning head after measuring the distances to refine the measured distances. |
| ptcGeometryScanCapsSelected | 1 | Performs the geometry scan for the selected scan points, only. |
