# Polytec_IO_VibInterfaces – GroupControllerUnitCaps

## GroupControllerUnitCaps Enumeration

*Quelle: `Polytec_IO_VibInterfaces~GroupControllerUnitCaps.html` · Polytec IO VibInterfaces Type Library*

### Description

This enumeration is provided for MPV, e.g. for the case where one hardware controller unit is used for all sensor heads/sondes of the controller group. Thus, some capabilities are only available for such unit and are not supported for a single controller object.

### Members

| Member | Value | Description |
|---|---|---|
| GroupControllerUnitCaps_AutoTuningState | 2 | The capability that the automatic tuning state can be queried. |
| GroupControllerUnitCaps_ClockSync | 8 | The capability that the clock can be synchronized. |
| GroupControllerUnitCaps_HourMeter | 1 | The capability that the hour meter seconds and the power switching on/off counter can be queried. |
| GroupControllerUnitCaps_None | 0 | None of the capabilities is available. |
| GroupControllerUnitCaps_UniqueID | 4 | The capability that the unique identifier can be queried. |
