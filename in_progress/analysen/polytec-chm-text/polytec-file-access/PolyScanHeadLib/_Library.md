# PolyScanHeadLib – _Library

## Project Overview

*Quelle: `PolyScanHeadLib_P.html` · Polytec PolyScanHead Type Library*

### Description

The Polytec PolyScanHead type library contains objects describing the scanning heads that are part of a PSV system. Using the objects you can access information about the available scanning heads and the scanning head that is part of the system. You can control the attached scanning head and e.g. move the laser beam by changing the values for the scanners.

### Object Model

### Classes

| Class Module | Description |
|---|---|
| DistanceSensorControl | Controls the distance sensor (geometry scan unit, PSV-A-420, PSV-G-500). |
| ScanHeadControl | Controls the scanning head. |
| ScanHeadDevice | The scanning head device. Item of the ScanHeadDevices collection . |
| ScanHeadDevices | Collection of the scanning head devices of a PSV system. |
| ScanHeadLaserFocus | Controls the focusing of the laser. |
| ScanHeadScanner | Controls the scanner of the scanning head. |
| ScanHeadType | The type of the scanning head. Item of the ScanHeadTypes collection . |
| ScanHeadTypes | The named and typed collection of the available scanning head types. |
| ScanHeadVideo | Controls the video of the scanning head. |
| ScannerControl | Controls the scanners of the scanning head. |
| ZStageControl | This object controls the z-stage of the MSA-500 system used for focusing the laser beam and measuring distances. |
| ZStageMoveLinearSettings | The settings for the movement of the z-stage with simultaneous generation of trigger pulses. |
| ZStageSettings | The properties of the z-stage of the MSA-500 system used for focusing the laser beam and measuring distances. |

### Interfaces

| Class Module | Description |
|---|---|
| IComContinuation | The base interface for a continuation of a task implementing the interface IComTask . |
| IComFunction | The base interface of a function that can be scheduled and executed by a scheduler implementing the IComScheduler interface . |
| IComScheduler | The base interface of a scheduler that executes functions implementing the IComFunction interface . |
| IComTask | The base interface for a task representing an asynchronous operation. |
| IDistanceSensorControl | Controls the distance sensor (geometry scan unit, PSV-A-420, PSV-G-500). |
| IScanHeadControl3 | Controls the scanning head. |
| IScanHeadDevice | The scanning head device. Item of the ScanHeadDevices collection . |
| IScanHeadDevices | Collection of the scanning head devices of a PSV system. |
| IScanHeadLaserFocus | Controls the focusing of the laser. |
| IScanHeadScanner | Controls the scanner of the scanning head. |
| IScannerControl | Controls the scanners of the scanning head. |
| IZStageControl | This object controls the z-stage of the MSA-500 system used for focusing the laser beam and measuring distances. |

### Public Enumerations

| Enumeration | Description |
|---|---|
| PTCComTaskStatus | Represents the status of a task implementing the interface IComTask . |
| PTCDistanceSensorControlCaps |  |
| PTCDistanceSensorMeasStatus | The status of the distance measurement. |
| PTCDistanceSensorMeasStatusEx | The status of the distance measurement. |
| PTCDistanceSensorType | The type of the distance sensor. |
| PTCPreferredScanDirection | The preferred scan direction. |
| PTCScanHeadCapsType | The scanning head capabilities. |
| PTCScanHeadSimulationCaps | The capabilities of the scanning head simulation. |
| PTCScanHeadType | The scanning head type. |
| PTCScanHeadVideoType | The type of the scanning head video. |
| PTCZStageFocusType | The type of the z-stage focus. |
| PTCZStageType | The type of the z-stage. |


---

## References

*Quelle: `PolyScanHeadLib_references.html` · Polytec PolyScanHead Type Library*


