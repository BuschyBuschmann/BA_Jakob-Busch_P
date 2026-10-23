# Polytec_IO_VibInterfaces – IQuantityCollection

## IQuantityCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~IQuantityCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of quantities of the controller.

### Object Model


---

## IQuantityCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~IQuantityCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| ByKey | Returns the item of the collection with the given quantity. |
|---|---|
| Contains | Returns true, if the collection contains the item with the given quantity type or name. |
| IndexOf | Returns the 0-based index of the given item. |
| IsEqual | Returns true if the given quantity collection is equal to this collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item of the collection with the given index or name. |


---

## ByKey Method

*Quelle: `Polytec_IO_VibInterfaces~IQuantityCollection~ByKey.html` · Polytec IO VibInterfaces Type Library · IQuantityCollection Collection : ByKey Method*

### Description

Returns the item of the collection with the given quantity.

### Syntax

*Visual Basic:*
```
Public Function ByKey( _
   ByVal QuantityType As QuantityType _
) As IQuantity
```

### Parameters

QuantityType

| Value | Description |
|---|---|
| QuantityType_Acceleration | Quantity acceleration. |
| QuantityType_Angle | Quantity angle. |
| QuantityType_AngleDegree | Quantity angle in degree. |
| QuantityType_AngularAcceleration | Quantity angular acceleration. |
| QuantityType_AngularAccelerationDegree | Quantity angular acceleration in degree. |
| QuantityType_AngularVelocity | Quantity angular velocity. |
| QuantityType_AngularVelocityDegree | Quantity angular velocity in degree. |
| QuantityType_Charge | Quantity charge. |
| QuantityType_Counts | Quantity counts. |
| QuantityType_Current | Quantity current. |
| QuantityType_Displacement | Quantity displacement. |
| QuantityType_Force | Quantity force. |
| QuantityType_Frequency | Quantity frequency. |
| QuantityType_GravitationalAcceleration | Quantity gravitational acceleration. |
| QuantityType_LuminousIntensity | Quantity luminous intensity. |
| QuantityType_Mass | Quantity mass. |
| QuantityType_None | No quantity. |
| QuantityType_Order | Quantity order. |
| QuantityType_Power | Quantity power. |
| QuantityType_Pressure | Quantity pressure. |
| QuantityType_Resistance | Quantity resistance. |
| QuantityType_Revolution | Quantity revolution. |
| QuantityType_Rpm | Quantity RPM. |
| QuantityType_SoundPressure | Quantity sound pressure. |
| QuantityType_Strain | Quantity strain. |
| QuantityType_Stress | Quantity stress. |
| QuantityType_Substance | Quantity substance. |
| QuantityType_Temperature | Quantity temperature. |
| QuantityType_Time | Quantity time. |
| QuantityType_Torque | Quantity torque. |
| QuantityType_User | Quantity user. |
| QuantityType_Velocity | Quantity velocity. |
| QuantityType_Voltage | Quantity voltage. |
| QuantityType_Volume | Quantity volume. |
| QuantityType_VolumeAcceleration | Quantity volume acceleration. |
| QuantityType_VolumeVelocity | Quantity volume velocity. |
| QuantityType_Work | Quantity work. |
The type of the quantity.


---

## Contains Method

*Quelle: `Polytec_IO_VibInterfaces~IQuantityCollection~Contains.html` · Polytec IO VibInterfaces Type Library · IQuantityCollection Collection : Contains Method*

### Description

Returns true, if the collection contains the item with the given quantity type or name.

### Syntax

*Visual Basic:*
```
Public Function Contains( _
   ByVal index As Variant _
) As Boolean
```

### Parameters

index

The quantity type or name of the item.


---

## IndexOf Method

*Quelle: `Polytec_IO_VibInterfaces~IQuantityCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · IQuantityCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal quantity As IQuantity _
) As Long
```

### Parameters

quantity

The quantity to get the index for.

### Remarks

Returns -1 if the item is not contained in the collection.


---

## IsEqual Method

*Quelle: `Polytec_IO_VibInterfaces~IQuantityCollection~IsEqual.html` · Polytec IO VibInterfaces Type Library · IQuantityCollection Collection : IsEqual Method*

### Description

Returns true if the given quantity collection is equal to this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal quantityCongeries As IQuantityCollection _
) As Boolean
```

### Parameters

quantityCongeries

The other quantities collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantityCollection~Count.html` · Polytec IO VibInterfaces Type Library · IQuantityCollection Collection : Count Property*

### Description

The number of items in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantityCollection~Item.html` · Polytec IO VibInterfaces Type Library · IQuantityCollection Collection : Item Property*

### Description

Returns the item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As IQuantity
```

### Parameters

index

The 0-based index or name of the item.
