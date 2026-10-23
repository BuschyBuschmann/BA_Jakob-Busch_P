# POLYFILELib – PTCFocusStatus

## PTCFocusStatus Enumeration

*Quelle: `POLYFILELib~PTCFocusStatus.html` · Polytec PolyFile Type Library*

### Description

Focus status of a scan point. The status can be a combination of several bit constants defined in the enumeration.

### Members

| Member | Value | Description |
|---|---|---|
| ptcFocusStatusAuto | 128 | Laser focus was automatically assigned. |
| ptcFocusStatusBest | 8 | Laser focus was assigned best. |
| ptcFocusStatusCalculated | 64 | Laser focus was calculated. |
| ptcFocusStatusFailed | 32 | Laser focus measurement failed. |
| ptcFocusStatusFast | 4 | Laser focus was assigned fast. |
| ptcFocusStatusInterpolated | 16 | Laser focus was interpolated by valid neighbors. |
| ptcFocusStatusManual | 2 | Laser focus was assigned manually. |
| ptcFocusStatusNone | 0 | Point has no laser focus. |
| ptcFocusStatusValid | 1 | Point has a valid laser focus. |
