# Polytec_IO_VibInterfaces – QuantitySettingsCollection

## QuantitySettingsCollection Collection

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettingsCollection.html` · Polytec IO VibInterfaces Type Library*

### Description

The collection of the quantity settings.

### Object Model


---

## QuantitySettingsCollection Collection Members

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettingsCollection_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| ByKey | Returns an item of the collection with the given quantity type. |
|---|---|
| Contains | Returns true, if the item with the given name or quantity type is contained in the collection. |
| IndexOf | Returns the 0-based index of the given item of the collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item of the collection with the given index or name. |


---

## ByKey Method

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettingsCollection~ByKey.html` · Polytec IO VibInterfaces Type Library · QuantitySettingsCollection Collection : ByKey Method*

### Description

Returns an item of the collection with the given quantity type.

### Syntax

*Visual Basic:*
```
Public Function ByKey( _
   ByVal QuantityType As QuantityType _
) As QuantitySettings
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

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettingsCollection~Contains.html` · Polytec IO VibInterfaces Type Library · QuantitySettingsCollection Collection : Contains Method*

### Description

Returns true, if the item with the given name or quantity type is contained in the collection.

### Syntax

*Visual Basic:*
```
Public Function Contains( _
   ByVal index As Variant _
) As Boolean
```

### Parameters

index

The name or quantity type of the item.


---

## IndexOf Method

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettingsCollection~IndexOf.html` · Polytec IO VibInterfaces Type Library · QuantitySettingsCollection Collection : IndexOf Method*

### Description

Returns the 0-based index of the given item of the collection.

### Syntax

*Visual Basic:*
```
Public Function IndexOf( _
   ByVal QuantitySettings As QuantitySettings _
) As Long
```

### Parameters

QuantitySettings

The item of the collection.

### Remarks

The method returns -1, if the item is not contained in the collection.


---

## Count Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettingsCollection~Count.html` · Polytec IO VibInterfaces Type Library · QuantitySettingsCollection Collection : Count Property*

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

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettingsCollection~Item.html` · Polytec IO VibInterfaces Type Library · QuantitySettingsCollection Collection : Item Property*

### Description

Returns the item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal index As Variant _
) As QuantitySettings
```

### Parameters

index

The 0-based index or name of the item.
