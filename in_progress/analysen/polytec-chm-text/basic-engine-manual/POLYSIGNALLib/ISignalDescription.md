# POLYSIGNALLib – ISignalDescription

## ISignalDescription Interface

*Quelle: `POLYSIGNALLib~ISignalDescription.html` · Polytec PolySignal Type Library*

### Description

The description of a signal.

### Object Model

### Remarks

It is recommended to cast to the SignalDescription Object.

### Example


---

## ISignalDescription Interface Members

*Quelle: `POLYSIGNALLib~ISignalDescription_members.html` · Polytec PolySignal Type Library*

### Public Methods

| Clone | Creates a copy of the signal description object. |
|---|---|
| Copy | Copies all properties of the given signal description object to this signal description object. |
| IsEqual | Returns true if the properties of the signal description object are equal to the properties of the given signal description object. |
| SetDefaultNames | Sets default names for various properties containing unit and quantity strings in the language with the given locale identifier. Moreover the Name Property is set taking the FunctionType and the unit and quantity of the YAxis into account. |

### Public Properties

| Attributes | Additional, optional values attached to the signal description. |
|---|---|
| Complex | Specifies whether the signal is complex. |
| DataType | Specifies the data type of the signal. |
| DbReference | Specifies the zero dB reference. |
| DomainType | Specifies the domain type of the signal. |
| FunctionType | Specifies the function type of the signal. |
| Name | The name of the signal. |
| PowerSignal | Specifies whether the signal is a power signal. |
| ReferenceDOFs | The collection of the reference degree of freedom identifiers. |
| ResponseDOFs | The collection of the response degree of freedom identifiers. |
| RMSCorrectionFactor | Specifies the RMS correction factor. |
| XAxis | The x-axis of the signal. |
| YAxis | The y-axis of the signal. |


---

## Clone Method

*Quelle: `POLYSIGNALLib~ISignalDescription~Clone.html` · Polytec PolySignal Type Library · ISignalDescription Interface : Clone Method*

### Description

Creates a copy of the signal description object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As SignalDescription
```

### Return Type

The new signal description object which is equal to the given signal description object.


---

## Copy Method

*Quelle: `POLYSIGNALLib~ISignalDescription~Copy.html` · Polytec PolySignal Type Library · ISignalDescription Interface : Copy Method*

### Description

Copies all properties of the given signal description object to this signal description object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pISignalDescription As SignalDescription _
)
```

### Parameters

pISignalDescription

The signal description object to copy the properties from.


---

## IsEqual Method

*Quelle: `POLYSIGNALLib~ISignalDescription~IsEqual.html` · Polytec PolySignal Type Library · ISignalDescription Interface : IsEqual Method*

### Description

Returns true if the properties of the signal description object are equal to the properties of the given signal description object.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pISignalDescription As SignalDescription _
) As Boolean
```

### Parameters

pISignalDescription

The signal description object to compare to.

### Return Type

True if the properties of the signal description object are equal to the properties of the given signal description object.


---

## SetDefaultNames Method

*Quelle: `POLYSIGNALLib~ISignalDescription~SetDefaultNames.html` · Polytec PolySignal Type Library · ISignalDescription Interface : SetDefaultNames Method*

### Description

Sets default names for various properties containing unit and quantity strings in the language with the given locale identifier. Moreover the Name Property is set taking the FunctionType and the unit and quantity of the YAxis into account.

### Syntax

*Visual Basic:*
```
Public Sub SetDefaultNames( _
   ByVal lLocaleID As Long _
)
```

### Parameters

lLocaleID

Supported values are:

-1: the current user interface language of the operating system

1033: for English (US)

1031: for German

### Remarks

The method parses the Quantity and Unit of the DegreeOfFreedomID Objects and, if successful, translates the strings accordingly.

The same is done for the Name and Unit of the XAxis and the Name and Unit of the YAxis.

### Example

This example macro creates a SignalDescription object, sets some properties and then calls SetDefaultNames() to adjust the names to the current user interface language.

- Setting the Default Names (Visual Basic)

```
Sub Main
    Debug.Clear
    Dim oSigDesc As New SignalDescription
    With oSigDesc
        .DataType = ptcDataPoint
        .FunctionType = ptcFunctionSpectrumType
        .DomainType = ptcDomainSpectrum
        .YAxis.Name = "Velocity"
        .YAxis.Unit = "m/s"
        .XAxis.Name = "Frequency"
        .XAxis.Unit = "Hz"
        .ResponseDOFs.Assign(-1, ptcPlusZTranslation, "Usr", "Velocity", "m/s")
        .SetDefaultNames(-1)
        Debug.Print .Name
        Debug.Print .YAxis.Name
        Debug.Print .YAxis.Unit
        Debug.Print .XAxis.Name
        Debug.Print .XAxis.Unit
        Debug.Print .ResponseDOFs(1).Quantity
        Debug.Print .ResponseDOFs(1).Unit
    End With
End Sub
```


---

## Attributes Property

*Quelle: `POLYSIGNALLib~ISignalDescription~Attributes.html` · Polytec PolySignal Type Library · ISignalDescription Interface : Attributes Property*

### Description

Additional, optional values attached to the signal description.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Attributes As Attributes
```

### Remarks

The attributes are persisted together with the signal description.


---

## Complex Property

*Quelle: `POLYSIGNALLib~ISignalDescription~Complex.html` · Polytec PolySignal Type Library · ISignalDescription Interface : Complex Property*

### Description

Specifies whether the signal is complex.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Complex As Boolean
```


---

## DataType Property

*Quelle: `POLYSIGNALLib~ISignalDescription~DataType.html` · Polytec PolySignal Type Library · ISignalDescription Interface : DataType Property*

### Description

Specifies the data type of the signal.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DataType As PTCDataType
```


---

## DbReference Property

*Quelle: `POLYSIGNALLib~ISignalDescription~DbReference.html` · Polytec PolySignal Type Library · ISignalDescription Interface : DbReference Property*

### Description

Specifies the zero dB reference.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DbReference As Double
```


---

## DomainType Property

*Quelle: `POLYSIGNALLib~ISignalDescription~DomainType.html` · Polytec PolySignal Type Library · ISignalDescription Interface : DomainType Property*

### Description

Specifies the domain type of the signal.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DomainType As PTCDomainType
```


---

## FunctionType Property

*Quelle: `POLYSIGNALLib~ISignalDescription~FunctionType.html` · Polytec PolySignal Type Library · ISignalDescription Interface : FunctionType Property*

### Description

Specifies the function type of the signal.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FunctionType As PTCFunctionType
```


---

## Name Property

*Quelle: `POLYSIGNALLib~ISignalDescription~Name.html` · Polytec PolySignal Type Library · ISignalDescription Interface : Name Property*

### Description

The name of the signal.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Remarks

The name of the signal can be used to remove signals from the Usr or Usr 3D channels by the Remove Method of the Signals Object object of these channels. The name must be unique for the channel of the signal.


---

## PowerSignal Property

*Quelle: `POLYSIGNALLib~ISignalDescription~PowerSignal.html` · Polytec PolySignal Type Library · ISignalDescription Interface : PowerSignal Property*

### Description

Specifies whether the signal is a power signal.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PowerSignal As Boolean
```

### Remarks

The flag is used to scale the signal properly for the dB displays.


---

## ReferenceDOFs Property

*Quelle: `POLYSIGNALLib~ISignalDescription~ReferenceDOFs.html` · Polytec PolySignal Type Library · ISignalDescription Interface : ReferenceDOFs Property*

### Description

The collection of the reference degree of freedom identifiers.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ReferenceDOFs As DegreeOfFreedomIDs
```

### Remarks

The collection is empty for response signals. A valid signal description either has to have at least a single response DOF or at least a single reference DOF. Please note that at creation of the signal description both collections are empty. For signals with function types like ptcFunctionPCAPrincipalInputsType or ptcFunctionPCAVirtualCoherencesType the collection contains DOFs for all references that contributed to the signal.


---

## ResponseDOFs Property

*Quelle: `POLYSIGNALLib~ISignalDescription~ResponseDOFs.html` · Polytec PolySignal Type Library · ISignalDescription Interface : ResponseDOFs Property*

### Description

The collection of the response degree of freedom identifiers.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ResponseDOFs As DegreeOfFreedomIDs
```

### Remarks

The collection is empty for reference signals. A valid signal description either has to have at least a single response DOF or at least a single reference DOF. Please note that at creation of the signal description both collections are empty. For 3D signals (signals of channels with the ptcChannelCapsVector flag set) the collection contains three DOFs. In this case the Direction property is set to ptcVector.


---

## RMSCorrectionFactor Property

*Quelle: `POLYSIGNALLib~ISignalDescription~RMSCorrectionFactor.html` · Polytec PolySignal Type Library · ISignalDescription Interface : RMSCorrectionFactor Property*

### Description

Specifies the RMS correction factor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RMSCorrectionFactor As Double
```

### Remarks

The RMS correction factor is used for the calculation of RMS bands and compensates for the window function. You can get the RMS correction factor of the window function from the WindowFunctionRMSCorrection Property of the ChannelAcqPropertiesContainer Object. For power signals the correction factors of the response and reference channels have to be multiplied (or squared for AutoPower signals).


---

## XAxis Property

*Quelle: `POLYSIGNALLib~ISignalDescription~XAxis.html` · Polytec PolySignal Type Library · ISignalDescription Interface : XAxis Property*

### Description

The x-axis of the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property XAxis As SignalXAxis
```


---

## YAxis Property

*Quelle: `POLYSIGNALLib~ISignalDescription~YAxis.html` · Polytec PolySignal Type Library · ISignalDescription Interface : YAxis Property*

### Description

The y-axis of the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property YAxis As SignalYAxis
```
