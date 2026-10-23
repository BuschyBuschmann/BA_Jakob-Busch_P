# POLYFILELib – IHardware3

## IHardware3 Interface

*Quelle: `POLYFILELib~IHardware3.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. The hardware object contains information about the acquisition board and front end of the MPV/PSV/VibSoft system used to create the file.

### Object Model

### Remarks

It is recommended to cast to the Hardware object.


---

## IHardware3 Interface Members

*Quelle: `POLYFILELib~IHardware3_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Save | Commits the changes to the Hardware object to the file. |
|---|---|

### Public Properties

| AcqBoard | Returns the acquisition board used for the measurement. |
|---|---|
| AcqBoardName | Returns the name of the acquisition board used for the measurement. |
| ActiveFrontEnd | Returns the active front end used for the measurement. |
| FrontEnd | Returns the front end type used for the measurement. |
| GeneratorName | The name of the generator used for the measurement. |
| GeneratorType | The type of the generator used for the measurement. |
| Name | Returns "Hardware. Can be used as an index into the Infos collection . |
| Type | Returns ptcInfoHardware. Can be used as an index into the Infos collection . |


---

## Save Method

*Quelle: `POLYFILELib~IHardware3~Save.html` · Polytec PolyFile Type Library · IHardware3 Interface : Save Method*

### Description

Commits the changes to the Hardware object to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## AcqBoard Property

*Quelle: `POLYFILELib~IHardware3~AcqBoard.html` · Polytec PolyFile Type Library · IHardware3 Interface : AcqBoard Property*

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

## AcqBoardName Property

*Quelle: `POLYFILELib~IHardware3~AcqBoardName.html` · Polytec PolyFile Type Library · IHardware3 Interface : AcqBoardName Property*

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

*Quelle: `POLYFILELib~IHardware3~ActiveFrontEnd.html` · Polytec PolyFile Type Library · IHardware3 Interface : ActiveFrontEnd Property*

### Description

Returns the active front end used for the measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ActiveFrontEnd As IFrontEnd
```

### Remarks

This property is only available in MPV/PSV/VibSoft as a member of the HardwareAcq object.


---

## FrontEnd Property

*Quelle: `POLYFILELib~IHardware3~FrontEnd.html` · Polytec PolyFile Type Library · IHardware3 Interface : FrontEnd Property*

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

## GeneratorName Property

*Quelle: `POLYFILELib~IHardware3~GeneratorName.html` · Polytec PolyFile Type Library · IHardware3 Interface : GeneratorName Property*

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

*Quelle: `POLYFILELib~IHardware3~GeneratorType.html` · Polytec PolyFile Type Library · IHardware3 Interface : GeneratorType Property*

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

*Quelle: `POLYFILELib~IHardware3~Name.html` · Polytec PolyFile Type Library · IHardware3 Interface : Name Property*

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

## Type Property

*Quelle: `POLYFILELib~IHardware3~Type.html` · Polytec PolyFile Type Library · IHardware3 Interface : Type Property*

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
