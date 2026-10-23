# Polytec_IO_VibInterfaces – QuantityCaps

## QuantityCaps Enumeration

*Quelle: `Polytec_IO_VibInterfaces~QuantityCaps.html` · Polytec IO VibInterfaces Type Library*

### Description

The capabilities of the quantity.

### Members

| Member | Value | Description |
|---|---|---|
| QuantityCaps_Bandwidth | 2 | The quantity has bandwidth ranges. |
| QuantityCaps_MaxVelocity | 4 | The quantity supports maximum velocity, e.g. for the VFX-F-110 system. |
| QuantityCaps_None | 0 | The quantity has no capability. |
| QuantityCaps_OutputActive | 16 | The quantity supports (decoder) output active status (e.g. IVS-500, VGO). |
| QuantityCaps_Overrun | 8 | The quantity supports overrun. |
| QuantityCaps_ReadoutValue | 1 | A readout value is available for the quantity. |
| QuantityCaps_VibAnalogOut | 32 | The quantity supports vibrometer analog out (e.g. VibroScan). |

### Remarks

The RPM value of RPM decoder of the RLV-5000 controller can be readout directly.
