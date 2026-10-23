# Polytec_IO_VibInterfaces – IFilter

## IFilter Interface

*Quelle: `Polytec_IO_VibInterfaces~IFilter.html` · Polytec IO VibInterfaces Type Library*

### Description

One of the filters of the vibrometer controller. Item of the IFilterCollection.

### Object Model


---

## IFilter Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IFilter_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| HasCap | Returns true, if the filter has the given capability. |
|---|---|

### Public Properties

| Caps | The caps of the filter. |
|---|---|
| Key | The filter type. |
| Name | The name of the filter. |
| Ranges | The ranges of the filter. |


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~IFilter~HasCap.html` · Polytec IO VibInterfaces Type Library · IFilter Interface : HasCap Method*

### Description

Returns true, if the filter has the given capability.

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
The capability of the filter.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~IFilter~Caps.html` · Polytec IO VibInterfaces Type Library · IFilter Interface : Caps Property*

### Description

The caps of the filter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As FilterCaps
```


---

## Key Property

*Quelle: `Polytec_IO_VibInterfaces~IFilter~Key.html` · Polytec IO VibInterfaces Type Library · IFilter Interface : Key Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IFilter~Name.html` · Polytec IO VibInterfaces Type Library · IFilter Interface : Name Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IFilter~Ranges.html` · Polytec IO VibInterfaces Type Library · IFilter Interface : Ranges Property*

### Description

The ranges of the filter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Ranges As IBaseFilterRangeCollection
```
