# POLYFILELib – DbReferences

## DbReferences Collection

*Quelle: `POLYFILELib~DbReferences.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection and the Preferences collection. Typed collection of Double. Contains the dB references for the various physical quantities.


---

## DbReferences Collection Members

*Quelle: `POLYFILELib~DbReferences_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Load | Loads the DbReferences collection from the file. |
|---|---|
| Save | Commits the changes to the DbReferences collection to the file. |

### Public Properties

| Count | Number of items of the DbReferences collection. |
|---|---|
| DbRef | Returns an item of the DbReferences collection. |
| Item | Returns an item of the DbReferences collection. |
| Name | Returns "DbReferences. Can be used as index to the Infos and Preferences collection. |
| PrefType | Returns ptcPrefDbReferences. Can be used as index to the Preferences collection . |
| Type | Returns ptcInfoDbReferences. Can be used as index to the Infos collection. |


---

## Load Method

*Quelle: `POLYFILELib~DbReferences~Load.html` · Polytec PolyFile Type Library · DbReferences Collection : Load Method*

### Description

Loads the DbReferences collection from the file.

### Syntax

*Visual Basic:*
```
Public Sub Load()
```

### Remarks

This method can be called after a change to the global dB references by another instance of PolyFile to refresh the values in the collection.


---

## Save Method

*Quelle: `POLYFILELib~DbReferences~Save.html` · Polytec PolyFile Type Library · DbReferences Collection : Save Method*

### Description

Commits the changes to the DbReferences collection to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## Count Property

*Quelle: `POLYFILELib~DbReferences~Count.html` · Polytec PolyFile Type Library · DbReferences Collection : Count Property*

### Description

Number of items of the DbReferences collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## DbRef Property

*Quelle: `POLYFILELib~DbReferences~DbRef.html` · Polytec PolyFile Type Library · DbReferences Collection : DbRef Property*

### Description

Returns an item of the DbReferences collection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DbRef( _
   ByVal Index As PTCPhysicalQuantity _
) As Double
```

### Parameters

Index

| Value | Description |
|---|---|
| ptcPhysicalQuantityAcceleration | Quantity acceleration. |
| ptcPhysicalQuantityAngle | Quantity angle. |
| ptcPhysicalQuantityAngleDegree | Quantity angle in degree. |
| ptcPhysicalQuantityAngularAcceleration | Quantity angular acceleration. |
| ptcPhysicalQuantityAngularAccelerationDegree | Quantity angular acceleration in degree. |
| ptcPhysicalQuantityAngularVelocity | Quantity angular velocity. |
| ptcPhysicalQuantityAngularVelocityDegree | Quantity angular velocity in degree. |
| ptcPhysicalQuantityCounts | Quantity counts. |
| ptcPhysicalQuantityDisplacement | Quantity displacement. |
| ptcPhysicalQuantityElectricalCurrent | Quantity electrical current. |
| ptcPhysicalQuantityForce | Quantity force. |
| ptcPhysicalQuantityFrequency | Quantity frequency. |
| ptcPhysicalQuantityGravitationalAcceleration | Quantity gravitational acceleration. |
| ptcPhysicalQuantityPower | Quantity power. |
| ptcPhysicalQuantityPressure | Quantity pressure. |
| ptcPhysicalQuantityRevolution | Quantity revolution. |
| ptcPhysicalQuantityRPM | Quantity RPM. |
| ptcPhysicalQuantitySoundPressure | Quantity sound pressure. |
| ptcPhysicalQuantityStrain | Quantity strain. |
| ptcPhysicalQuantityStress | Quantity stress. |
| ptcPhysicalQuantityTime | Quantity time. |
| ptcPhysicalQuantityTorque | Quantity torque. |
| ptcPhysicalQuantityVelocity | Quantity velocity. |
| ptcPhysicalQuantityVoltage | Quantity voltage. |
| ptcPhysicalQuantityVolume | Quantity volume. |
| ptcPhysicalQuantityVolumeAcceleration | Quantity volume acceleration. |
| ptcPhysicalQuantityVolumeVelocity | Quantity volume velocity. |
The physical quantity to retrieve the dB reference for.


---

## Item Property

*Quelle: `POLYFILELib~DbReferences~Item.html` · Polytec PolyFile Type Library · DbReferences Collection : Item Property*

### Description

Returns an item of the DbReferences collection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Long _
) As Double
```

### Parameters

Index

The index of the item in the DbReferences collection.


---

## Name Property

*Quelle: `POLYFILELib~DbReferences~Name.html` · Polytec PolyFile Type Library · DbReferences Collection : Name Property*

### Description

Returns "DbReferences. Can be used as index to the Infos and Preferences collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "DbReferences".


---

## PrefType Property

*Quelle: `POLYFILELib~DbReferences~PrefType.html` · Polytec PolyFile Type Library · DbReferences Collection : PrefType Property*

### Description

Returns ptcPrefDbReferences. Can be used as index to the Preferences collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PrefType As PTCPrefType
```

### Return Type

PTCPrefType


---

## Type Property

*Quelle: `POLYFILELib~DbReferences~Type.html` · Polytec PolyFile Type Library · DbReferences Collection : Type Property*

### Description

Returns ptcInfoDbReferences. Can be used as index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoDbReferences.
