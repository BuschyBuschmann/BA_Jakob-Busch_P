# Polytec_IO_VibInterfaces – ITrackingFilter

## ITrackingFilter Interface

*Quelle: `Polytec_IO_VibInterfaces~ITrackingFilter.html` · Polytec IO VibInterfaces Type Library*

### Description

The tracking filter. This object is derived from the IFilter Object.

### Object Model


---

## ITrackingFilter Interface Members

*Quelle: `Polytec_IO_VibInterfaces~ITrackingFilter_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| HasCap | Returns true if the filter has the given capability. |
|---|---|
| SetSeekRange | Sets the seek range of the tracking filter. |

### Public Properties

| Caps | The capabilities of the tracking filter. |
|---|---|
| Key | The filter type. |
| Name | The name of the filter. |
| Ranges | The ranges of the filter. |
| SeekRange | The seek range of the tracking filter. |


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~ITrackingFilter~HasCap.html` · Polytec IO VibInterfaces Type Library · ITrackingFilter Interface : HasCap Method*

### Description

Returns true if the filter has the given capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As FilterCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| FilterCaps_None | The filter has no capabilities. |
| FilterCaps_TrackingFilterSeekRange | The seek range of the tracking filter can be specified. |
The filter capability.


---

## SetSeekRange Method

*Quelle: `Polytec_IO_VibInterfaces~ITrackingFilter~SetSeekRange.html` · Polytec IO VibInterfaces Type Library · ITrackingFilter Interface : SetSeekRange Method*

### Description

Sets the seek range of the tracking filter.

### Syntax

*Visual Basic:*
```
Public Sub SetSeekRange( _
   ByVal SeekRange As TrackingFilterSeekRangeMode _
)
```

### Parameters

SeekRange

| Value | Description |
|---|---|
| TrackingFilterSeekRangeMode_Full | The seek range is full. |
| TrackingFilterSeekRangeMode_Reduced | The seek range is reduced. |
The seek range.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~ITrackingFilter~Caps.html` · Polytec IO VibInterfaces Type Library · ITrackingFilter Interface : Caps Property*

### Description

The capabilities of the tracking filter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As FilterCaps
```


---

## Key Property

*Quelle: `Polytec_IO_VibInterfaces~ITrackingFilter~Key.html` · Polytec IO VibInterfaces Type Library · ITrackingFilter Interface : Key Property*

### Description

The filter type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Key As FilterType
```

### Remarks

The filter type can be used as a parameter to the ByKey method and Contains method.


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~ITrackingFilter~Name.html` · Polytec IO VibInterfaces Type Library · ITrackingFilter Interface : Name Property*

### Description

The name of the filter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Remarks

The name of the filter can be used as a parameter to the Contains Method and the Item Property.


---

## Ranges Property

*Quelle: `Polytec_IO_VibInterfaces~ITrackingFilter~Ranges.html` · Polytec IO VibInterfaces Type Library · ITrackingFilter Interface : Ranges Property*

### Description

The ranges of the filter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Ranges As IBaseFilterRangeCollection
```


---

## SeekRange Property

*Quelle: `Polytec_IO_VibInterfaces~ITrackingFilter~SeekRange.html` · Polytec IO VibInterfaces Type Library · ITrackingFilter Interface : SeekRange Property*

### Description

The seek range of the tracking filter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SeekRange As TrackingFilterSeekRangeMode
```
