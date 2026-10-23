# Polytec_IO_VibInterfaces – IControllerSettings

## IControllerSettings Interface

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings.html` · Polytec IO VibInterfaces Type Library*

### Description

The settings of the vibrometer controller.

### Object Model

### Remarks

It is recommended to cast to the ControllerSettings object.


---

## IControllerSettings Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Clone | Creates and returns a copy of the settings object. |
|---|---|
| Copy | Copies all properties of the given settings object to this object. |
| Equals | Checks if the properties of the given settings object are equal to the properties of this object. |
| Load | Loads the state of this object and all of its children from the specified XML fragment. |
| Save | Returns an XML fragment representing the state of this object and all of its children. |

### Public Properties

| ControllerInfo | The information about the controller. |
|---|---|
| DecoderClearMode | The decoder clear mode. |
| FilterSettingsCollection | The settings of the filters. |
| QuantitySettingsCollection | The settings of the quantities. |
| SensorHeadSettingsCollection | The settings of the sensor heads. |


---

## Clone Method

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~Clone.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : Clone Method*

### Description

Creates and returns a copy of the settings object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Variant
```


---

## Copy Method

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~Copy.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : Copy Method*

### Description

Copies all properties of the given settings object to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal ControllerSettings As ControllerSettings _
)
```

### Parameters

ControllerSettings

The settings object to copy the properties from.


---

## Equals Method

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~Equals.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : Equals Method*

### Description

Checks if the properties of the given settings object are equal to the properties of this object.

### Syntax

*Visual Basic:*
```
Public Function Equals( _
   ByVal value As Variant _
) As Boolean
```

### Parameters

value

The other settings object to compare the properties with.

### Return Type

True, if all properties of both objects are the same.


---

## Load Method

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~Load.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : Load Method*

### Description

Loads the state of this object and all of its children from the specified XML fragment.

### Syntax

*Visual Basic:*
```
Public Sub Load( _
   ByVal content As String _
)
```

### Parameters

content

The XML fragment.

### Remarks

The format of the XML fragment is not documented. Use the Save Method to get an XML fragment for the current state of the object.


---

## Save Method

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~Save.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : Save Method*

### Description

Returns an XML fragment representing the state of this object and all of its children.

### Syntax

*Visual Basic:*
```
Public Function Save() As String
```

### Return Type

The XML fragment.

### Remarks

The format of the XML fragment is not documented. You can use the Load Method to restore the state of this object at a later time using the returned XML fragment.

### Example


---

## ControllerInfo Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~ControllerInfo.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : ControllerInfo Property*

### Description

The information about the controller.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ControllerInfo As ControllerInfo
```


---

## DecoderClearMode Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~DecoderClearMode.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : DecoderClearMode Property*

### Description

The decoder clear mode.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DecoderClearMode As String
```


---

## FilterSettingsCollection Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~FilterSettingsCollection.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : FilterSettingsCollection Property*

### Description

The settings of the filters.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FilterSettingsCollection As FilterSettingsCollection
```


---

## QuantitySettingsCollection Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~QuantitySettingsCollection.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : QuantitySettingsCollection Property*

### Description

The settings of the quantities.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property QuantitySettingsCollection As QuantitySettingsCollection
```


---

## SensorHeadSettingsCollection Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerSettings~SensorHeadSettingsCollection.html` · Polytec IO VibInterfaces Type Library · IControllerSettings Interface : SensorHeadSettingsCollection Property*

### Description

The settings of the sensor heads.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SensorHeadSettingsCollection As SensorHeadSettingsCollection
```
