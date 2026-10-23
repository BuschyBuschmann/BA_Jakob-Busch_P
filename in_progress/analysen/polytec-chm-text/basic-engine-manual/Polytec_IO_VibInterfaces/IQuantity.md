# Polytec_IO_VibInterfaces – IQuantity

## IQuantity Interface

*Quelle: `Polytec_IO_VibInterfaces~IQuantity.html` · Polytec IO VibInterfaces Type Library*

### Description

The quantity of the decoder. Item of the IQuantityCollection.

### Object Model


---

## IQuantity Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IQuantity_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| HasCap | Returns true if the quantity has the given capability. |
|---|---|

### Public Properties

| BandwidthRanges | The bandwidth ranges of the quantity. |
|---|---|
| Caps | The capabilities of the quantity. |
| Key | The type of the quantity. |
| MaxReadout | The maximum of the range of the readout. |
| MaxVelocityRanges | The maximum velocity ranges of the quantity. |
| MinReadout | The minimum of the range of the readout. |
| Name | The name of the quantity. |
| Overrange | True, if the there is an overrange for this quantity. |
| OverrunModes | The overrun modes of the quantity. |
| Ranges | The ranges of the quantity. |
| Readout | The current readout value of the quantity. |


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~HasCap.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : HasCap Method*

### Description

Returns true if the quantity has the given capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As QuantityCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| QuantityCaps_Bandwidth | The quantity has bandwidth ranges. |
| QuantityCaps_MaxVelocity | The quantity supports maximum velocity, e.g. for the VFX-F-110 system. |
| QuantityCaps_None | The quantity has no capability. |
| QuantityCaps_OutputActive | The quantity supports (decoder) output active status (e.g. IVS-500, VGO). |
| QuantityCaps_Overrun | The quantity supports overrun. |
| QuantityCaps_ReadoutValue | A readout value is available for the quantity. |
| QuantityCaps_VibAnalogOut | The quantity supports vibrometer analog out (e.g. VibroScan). |
The capability of the quantity.


---

## BandwidthRanges Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~BandwidthRanges.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : BandwidthRanges Property*

### Description

The bandwidth ranges of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BandwidthRanges As IBandwidthRangeCollection
```

### Remarks

The bandwidth ranges are a combination of the bandwidth ranges of all decoders of this quantity.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~Caps.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : Caps Property*

### Description

The capabilities of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As QuantityCaps
```


---

## Key Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~Key.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : Key Property*

### Description

The type of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Key As QuantityType
```

### Remarks

The quantity type can be used as a parameter to the ByKey method and Contains method.


---

## MaxReadout Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~MaxReadout.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : MaxReadout Property*

### Description

The maximum of the range of the readout.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxReadout As Double
```

### Remarks

This value is only available, when the quantity has the readout value capability.


---

## MaxVelocityRanges Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~MaxVelocityRanges.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : MaxVelocityRanges Property*

### Description

The maximum velocity ranges of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxVelocityRanges As IMaxVelocityRangeCollection
```


---

## MinReadout Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~MinReadout.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : MinReadout Property*

### Description

The minimum of the range of the readout.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinReadout As Double
```

### Remarks

This value is only available, when the quantity has the readout value capability.


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~Name.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : Name Property*

### Description

The name of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Remarks

The name can be used as a parameter to the Contains method and Item property.


---

## Overrange Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~Overrange.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : Overrange Property*

### Description

True, if the there is an overrange for this quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Overrange As Boolean
```


---

## OverrunModes Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~OverrunModes.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : OverrunModes Property*

### Description

The overrun modes of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property OverrunModes As OverrunModeCollection
```


---

## Ranges Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~Ranges.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : Ranges Property*

### Description

The ranges of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Ranges As IDecoderRangeCollection
```

### Remarks

The ranges are a combination of the ranges of all decoders of this quantity.


---

## Readout Property

*Quelle: `Polytec_IO_VibInterfaces~IQuantity~Readout.html` · Polytec IO VibInterfaces Type Library · IQuantity Interface : Readout Property*

### Description

The current readout value of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Readout As Double
```

### Remarks

This value is only available, when the quantity has the readout value capability.
