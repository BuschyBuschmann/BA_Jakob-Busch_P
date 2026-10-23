# Polytec_IO_VibInterfaces – ControllerCaps

## ControllerCaps Enumeration

*Quelle: `Polytec_IO_VibInterfaces~ControllerCaps.html` · Polytec IO VibInterfaces Type Library*

### Description

The capabilities of the controller.

### Members

| Member | Value | Description |
|---|---|---|
| ControllerCaps_DecoderClearMode | 2048 | The controller supports decoder clear modes. |
| ControllerCaps_DigitalDemodulation | 8 | The controller has digital demodulation. |
| ControllerCaps_FieldUpdate | 65536 | The controller supports field updates. |
| ControllerCaps_IsPhysicalUnit | 4096 | If set, the controller unit itself (not necessarily its sensor head or decoder) is physical, i.e. not logical. E.g. the controller number zero of a PSV-500-3D, the first and only controller of a PSV-500-1D or all three controllers of a PSV-400-3D (because this system is build in hardware of three independent controller units, instead of one controller unit (PSV-500-3D) with three connected sensor heads, decoders etc.). |
| ControllerCaps_MeasurementMode | 64 | The controller supports different measurement modes. |
| ControllerCaps_MultipleOverrange | 16 | The controller has multiple overrange indicators. |
| ControllerCaps_MultipleSensorHeads | 128 | The controller has multiple sensor heads. |
| ControllerCaps_NoDecoder | 1024 | The controller has no decoder, i.e. no data acquisition, e.g. that of the MPV system. |
| ControllerCaps_None | 0 | No capabilities. |
| ControllerCaps_Overrange | 256 | The controller has at least one overrange indicator. |
| ControllerCaps_PowerUP | 1 | The controller has power up. |
| ControllerCaps_PSV500Behaviour | 512 | The controller behaves like a controller of the PSV-500 system. |
| ControllerCaps_Recorder | 16384 | The controller has a recorder for vibration data e.g., VGO-200. |
| ControllerCaps_SensorHead | 2 | The controller has a sensor head. |
| ControllerCaps_ServiceMode | 4 | The controller has a service mode. |
| ControllerCaps_SignalEnhancement | 32 | The controller has signal enhancement. |
| ControllerCaps_WebServer | 32768 | The controller has a web server. |
| ControllerCaps_WriteLock | 8192 | The controller supports a write lock. |
