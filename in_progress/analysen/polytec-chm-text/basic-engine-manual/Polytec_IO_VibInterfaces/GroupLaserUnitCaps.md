# Polytec_IO_VibInterfaces – GroupLaserUnitCaps

## GroupLaserUnitCaps Enumeration

*Quelle: `Polytec_IO_VibInterfaces~GroupLaserUnitCaps.html` · Polytec IO VibInterfaces Type Library*

### Description

This enumeration is provided for the MPV system , e.g. for the case where one laser unit is used for all sensor heads/sondes of the controller group. Thus, some capabilities are only available for such unit and are not supported for the individual controller units.

### Members

| Member | Value | Description |
|---|---|---|
| GroupLaserUnitCaps_LaserOperationPoint | 1 | The capability that the laser operation point can be changed. |
| GroupLaserUnitCaps_LaserShutter | 2 | The capability that the laser unit can be switched on and off. |
| GroupLaserUnitCaps_LaserTemperature | 32 | The capability that the laser temperature can be queried. |
| GroupLaserUnitCaps_LaserTemperatureOutOfRange | 64 | The capability that it can be queried whether the laser temperature is out of range. |
| GroupLaserUnitCaps_LaserWavelengthStabilization | 16 | The capability that it can be queried whether the laser wavelength is stable or still stabilizing. |
| GroupLaserUnitCaps_None | 0 | None of the capabilities is available. |
| GroupLaserUnitCaps_PilotLaserModulation | 8 | The capability that the pilot laser modulation can be switched on and off. |
| GroupLaserUnitCaps_PilotLaserShutter | 4 | The capability that the pilot laser unit can be switched on and off. |
| GroupLaserUnitCaps_ShifterFrequency | 512 | The capability that the shifter frequency can be queried. |
| GroupLaserUnitCaps_ShifterOperatingTemperature | 128 | The capability that the shifter operating temperature can be queried. |
| GroupLaserUnitCaps_ShifterRFLevel | 256 | The capability that the shifter RF level can be queried. |
