# POLYFILELib – IHardware7

## IHardware7 Interface

*Quelle: `POLYFILELib~IHardware7.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. The hardware object contains information about the acquisition board and front end of the MPV/PSV/VibSoft system used to create the file.

### Object Model

### Remarks

It is recommended to cast to the Hardware Object.


---

## IHardware7 Interface Members

*Quelle: `POLYFILELib~IHardware7_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Save | Commits the changes to the Hardware object to the file. |
|---|---|

### Public Properties

| AcqBoard | Returns the acquisition board used for the measurement. |
|---|---|
| AcqBoardChannelCount | Returns the number of channels of the acquisition board used for the measurement. |
| AcqBoardFirmwareVersion | Returns the firmware version of the acquisition board used for the measurement. |
| AcqBoardMaxFrequency | Returns the maximum frequency of the acquisition board used for the measurement. |
| AcqBoardName | Returns the name of the acquisition board used for the measurement. |
| ActiveFrontEnd | Returns the active front end used for the measurement. |
| CoherenceOptimizerVersions | Returns the versions of the CoherenceOptimizers of the system. |
| FrontEnd | Returns the front end type used for the measurement. |
| FrontEndFirmwareVersion | Returns the firmware version of the front end used for the measurement. |
| GeneratorChannelCount | Returns the number of channels of the signal generator used for the measurement. |
| GeneratorFirmwareVersion | Returns the firmware version of the signal generator used for the measurement. |
| GeneratorName | The name of the generator used for the measurement. |
| GeneratorType | The type of the generator used for the measurement. |
| Name | Returns "Hardware. Can be used as an index into the Infos collection . |
| ScanHeadType | The type of the scanning head used for the measurement. |
| SensorHeadNames | Returns the names of the sensor heads used for the measurement. |
| SensorHeadVersions | Returns the versions of the sensor heads used for the measurement. |
| TedsSensors | Returns information about the TEDS sensors connected to the system. |
| Type | Returns ptcInfoHardware. Can be used as an index into the Infos collection . |


---

## Save Method

*Quelle: `POLYFILELib~IHardware7~Save.html` · Polytec PolyFile Type Library · IHardware7 Interface : Save Method*

### Description

Commits the changes to the Hardware object to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## AcqBoard Property

*Quelle: `POLYFILELib~IHardware7~AcqBoard.html` · Polytec PolyFile Type Library · IHardware7 Interface : AcqBoard Property*

### Description

Returns the acquisition board used for the measurement.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AcqBoard As PTCAcqBoardType
```


---

## AcqBoardChannelCount Property

*Quelle: `POLYFILELib~IHardware7~AcqBoardChannelCount.html` · Polytec PolyFile Type Library · IHardware7 Interface : AcqBoardChannelCount Property*

### Description

Returns the number of channels of the acquisition board used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AcqBoardChannelCount As Integer
```


---

## AcqBoardFirmwareVersion Property

*Quelle: `POLYFILELib~IHardware7~AcqBoardFirmwareVersion.html` · Polytec PolyFile Type Library · IHardware7 Interface : AcqBoardFirmwareVersion Property*

### Description

Returns the firmware version of the acquisition board used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AcqBoardFirmwareVersion As String
```


---

## AcqBoardMaxFrequency Property

*Quelle: `POLYFILELib~IHardware7~AcqBoardMaxFrequency.html` · Polytec PolyFile Type Library · IHardware7 Interface : AcqBoardMaxFrequency Property*

### Description

Returns the maximum frequency of the acquisition board used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AcqBoardMaxFrequency As Double
```


---

## AcqBoardName Property

*Quelle: `POLYFILELib~IHardware7~AcqBoardName.html` · Polytec PolyFile Type Library · IHardware7 Interface : AcqBoardName Property*

### Description

Returns the name of the acquisition board used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AcqBoardName As String
```

### Remarks

This property is only available in MPV/PSV/VibSoft as a member of the HardwareAcq object.


---

## ActiveFrontEnd Property

*Quelle: `POLYFILELib~IHardware7~ActiveFrontEnd.html` · Polytec PolyFile Type Library · IHardware7 Interface : ActiveFrontEnd Property*

### Description

Returns the active front end used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ActiveFrontEnd As IFrontEnd2
```

### Remarks

This property is only available in MPV/PSV/VibSoft as a member of the HardwareAcq object.


---

## CoherenceOptimizerVersions Property

*Quelle: `POLYFILELib~IHardware7~CoherenceOptimizerVersions.html` · Polytec PolyFile Type Library · IHardware7 Interface : CoherenceOptimizerVersions Property*

### Description

Returns the versions of the CoherenceOptimizers of the system.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CoherenceOptimizerVersions As String()
```

### Return Type

Zero-based array with the versions of the CoherenceOptimizers.

### Remarks

For 1D-systems an array with a single element is returned, for 3D-systems an array with three elements for the sensor heads top, left and right is returned.


---

## FrontEnd Property

*Quelle: `POLYFILELib~IHardware7~FrontEnd.html` · Polytec PolyFile Type Library · IHardware7 Interface : FrontEnd Property*

### Description

Returns the front end type used for the measurement.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FrontEnd As PTCFrontEndType
```

### Return Type

PTCFrontEndType


---

## FrontEndFirmwareVersion Property

*Quelle: `POLYFILELib~IHardware7~FrontEndFirmwareVersion.html` · Polytec PolyFile Type Library · IHardware7 Interface : FrontEndFirmwareVersion Property*

### Description

Returns the firmware version of the front end used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrontEndFirmwareVersion As String
```


---

## GeneratorChannelCount Property

*Quelle: `POLYFILELib~IHardware7~GeneratorChannelCount.html` · Polytec PolyFile Type Library · IHardware7 Interface : GeneratorChannelCount Property*

### Description

Returns the number of channels of the signal generator used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GeneratorChannelCount As Integer
```


---

## GeneratorFirmwareVersion Property

*Quelle: `POLYFILELib~IHardware7~GeneratorFirmwareVersion.html` · Polytec PolyFile Type Library · IHardware7 Interface : GeneratorFirmwareVersion Property*

### Description

Returns the firmware version of the signal generator used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GeneratorFirmwareVersion As String
```


---

## GeneratorName Property

*Quelle: `POLYFILELib~IHardware7~GeneratorName.html` · Polytec PolyFile Type Library · IHardware7 Interface : GeneratorName Property*

### Description

The name of the generator used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GeneratorName As String
```

### Remarks

This property is only available in MPV/PSV/VibSoft as a member of the HardwareAcq object.


---

## GeneratorType Property

*Quelle: `POLYFILELib~IHardware7~GeneratorType.html` · Polytec PolyFile Type Library · IHardware7 Interface : GeneratorType Property*

### Description

The type of the generator used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GeneratorType As PTCGeneratorType
```

### Remarks

This property is only available in MPV/PSV/VibSoft as a member of the HardwareAcq object.


---

## Name Property

*Quelle: `POLYFILELib~IHardware7~Name.html` · Polytec PolyFile Type Library · IHardware7 Interface : Name Property*

### Description

Returns "Hardware. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "Hardware".


---

## ScanHeadType Property

*Quelle: `POLYFILELib~IHardware7~ScanHeadType.html` · Polytec PolyFile Type Library · IHardware7 Interface : ScanHeadType Property*

### Description

The type of the scanning head used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadType As PTCScanHeadType
```

### Remarks

Currently the scanning head type is only available on MSA-600 X/U systems and in measurement files created on these systems. On all other systems the return value is ptcScanHeadTypeNone.


---

## SensorHeadNames Property

*Quelle: `POLYFILELib~IHardware7~SensorHeadNames.html` · Polytec PolyFile Type Library · IHardware7 Interface : SensorHeadNames Property*

### Description

Returns the names of the sensor heads used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SensorHeadNames As String()
```

### Return Type

Zero-based array with the sensor head names.

### Remarks

For 1D-systems an array with a single element is returned, otherwise an array with three elements for the sensor heads top, left and right.


---

## SensorHeadVersions Property

*Quelle: `POLYFILELib~IHardware7~SensorHeadVersions.html` · Polytec PolyFile Type Library · IHardware7 Interface : SensorHeadVersions Property*

### Description

Returns the versions of the sensor heads used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SensorHeadVersions As String()
```

### Return Type

Zero-based array with the sensor head versions.

### Remarks

For 1D-systems an array with a single element is returned, otherwise an array with three elements for the sensor heads top, left and right.


---

## TedsSensors Property

*Quelle: `POLYFILELib~IHardware7~TedsSensors.html` · Polytec PolyFile Type Library · IHardware7 Interface : TedsSensors Property*

### Description

Returns information about the TEDS sensors connected to the system.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TedsSensors As String()
```

### Return Type

An array of XML-formatted strings containing the serial numbers of the sensors.

### Example


---

## Type Property

*Quelle: `POLYFILELib~IHardware7~Type.html` · Polytec PolyFile Type Library · IHardware7 Interface : Type Property*

### Description

Returns ptcInfoHardware. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoHardware.
