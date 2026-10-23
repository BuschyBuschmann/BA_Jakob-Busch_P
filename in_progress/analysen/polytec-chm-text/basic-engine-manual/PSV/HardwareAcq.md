# PSV – HardwareAcq

## HardwareAcq Object

*Quelle: `PSV~HardwareAcq.html` · Polytec PSV Type Library*

### Description

Item of the InfosAcq collection describing the hardware of the system.

### Object Model


---

## HardwareAcq Object Members

*Quelle: `PSV~HardwareAcq_members.html` · Polytec PSV Type Library*

### Public Methods

| Save | Commits the changes to the Hardware object to the file. |
|---|---|

### Public Properties

| AcqBoard | The type of the acquisition board used for the measurement. |
|---|---|
| AcqBoardChannelCount | Returns the number of channels of the acquisition board used for the measurement. |
| AcqBoardFirmwareVersion | Returns the firmware version of the acquisition board used for the measurement. |
| AcqBoardMaxFrequency | Returns the maximum frequency of the acquisition board used for the measurement. |
| AcqBoardName | The name of the acquisition board used for the measurement. |
| ActiveFrontEnd | The front end used for the measurement. |
| CoherenceOptimizerVersions | Returns the versions of the CoherenceOptimizers of the system. |
| FrontEnd | The type of the front end used for the measurement. |
| FrontEndFirmwareVersion | Returns the firmware version of the front end used for the measurement. |
| GeneratorChannelCount | Returns the number of channels of the signal generator used for the measurement. |
| GeneratorFirmwareVersion | Returns the firmware version of the signal generator used for the measurement. |
| GeneratorName | The name of the generator used for the measurement. |
| GeneratorType | The type of the generator used for the measurement. |
| Name | Returns "Hardware. Can be used as an index into the InfosAcq Collection . |
| ScanHeadType | The type of the scanning head used for the measurement. |
| SensorHeadNames | Returns the names of the sensor heads used for the measurement. |
| SensorHeadSerialNumbers | Gets the sensor head serial numbers. |
| SensorHeadVersions | Returns the versions of the sensor heads used for the measurement. |
| TedsSensors | Returns information about the TEDS sensors connected to the system. |
| Type | Returns ptcInfoHardware. Can be used as an index into the InfosAcq collection . |


---

## Save Method

*Quelle: `PSV~HardwareAcq~Save.html` · Polytec PSV Type Library · HardwareAcq Object : Save Method*

### Description

Commits the changes to the Hardware object to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## AcqBoard Property

*Quelle: `PSV~HardwareAcq~AcqBoard.html` · Polytec PSV Type Library · HardwareAcq Object : AcqBoard Property*

### Description

The type of the acquisition board used for the measurement.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AcqBoard As PTCAcqBoardType
```


---

## AcqBoardChannelCount Property

*Quelle: `PSV~HardwareAcq~AcqBoardChannelCount.html` · Polytec PSV Type Library · HardwareAcq Object : AcqBoardChannelCount Property*

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

*Quelle: `PSV~HardwareAcq~AcqBoardFirmwareVersion.html` · Polytec PSV Type Library · HardwareAcq Object : AcqBoardFirmwareVersion Property*

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

*Quelle: `PSV~HardwareAcq~AcqBoardMaxFrequency.html` · Polytec PSV Type Library · HardwareAcq Object : AcqBoardMaxFrequency Property*

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

*Quelle: `PSV~HardwareAcq~AcqBoardName.html` · Polytec PSV Type Library · HardwareAcq Object : AcqBoardName Property*

### Description

The name of the acquisition board used for the measurement.

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

*Quelle: `PSV~HardwareAcq~ActiveFrontEnd.html` · Polytec PSV Type Library · HardwareAcq Object : ActiveFrontEnd Property*

### Description

The front end used for the measurement.

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

*Quelle: `PSV~HardwareAcq~CoherenceOptimizerVersions.html` · Polytec PSV Type Library · HardwareAcq Object : CoherenceOptimizerVersions Property*

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

*Quelle: `PSV~HardwareAcq~FrontEnd.html` · Polytec PSV Type Library · HardwareAcq Object : FrontEnd Property*

### Description

The type of the front end used for the measurement.

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

*Quelle: `PSV~HardwareAcq~FrontEndFirmwareVersion.html` · Polytec PSV Type Library · HardwareAcq Object : FrontEndFirmwareVersion Property*

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

*Quelle: `PSV~HardwareAcq~GeneratorChannelCount.html` · Polytec PSV Type Library · HardwareAcq Object : GeneratorChannelCount Property*

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

*Quelle: `PSV~HardwareAcq~GeneratorFirmwareVersion.html` · Polytec PSV Type Library · HardwareAcq Object : GeneratorFirmwareVersion Property*

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

*Quelle: `PSV~HardwareAcq~GeneratorName.html` · Polytec PSV Type Library · HardwareAcq Object : GeneratorName Property*

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

*Quelle: `PSV~HardwareAcq~GeneratorType.html` · Polytec PSV Type Library · HardwareAcq Object : GeneratorType Property*

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

*Quelle: `PSV~HardwareAcq~Name.html` · Polytec PSV Type Library · HardwareAcq Object : Name Property*

### Description

Returns "Hardware. Can be used as an index into the InfosAcq Collection.

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

*Quelle: `PSV~HardwareAcq~ScanHeadType.html` · Polytec PSV Type Library · HardwareAcq Object : ScanHeadType Property*

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

The scan head type is available on all systems with scanning heads. On all other systems the return value is ptcScanHeadTypeNone.


---

## SensorHeadNames Property

*Quelle: `PSV~HardwareAcq~SensorHeadNames.html` · Polytec PSV Type Library · HardwareAcq Object : SensorHeadNames Property*

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

## SensorHeadSerialNumbers Property

*Quelle: `PSV~HardwareAcq~SensorHeadSerialNumbers.html` · Polytec PSV Type Library · HardwareAcq Object : SensorHeadSerialNumbers Property*

### Description

Gets the sensor head serial numbers.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SensorHeadSerialNumbers As String()
```

### Return Type

The sensor head serial numbers.


---

## SensorHeadVersions Property

*Quelle: `PSV~HardwareAcq~SensorHeadVersions.html` · Polytec PSV Type Library · HardwareAcq Object : SensorHeadVersions Property*

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

*Quelle: `PSV~HardwareAcq~TedsSensors.html` · Polytec PSV Type Library · HardwareAcq Object : TedsSensors Property*

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

*Quelle: `PSV~HardwareAcq~Type.html` · Polytec PSV Type Library · HardwareAcq Object : Type Property*

### Description

Returns ptcInfoHardware. Can be used as an index into the InfosAcq collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoHardware.
