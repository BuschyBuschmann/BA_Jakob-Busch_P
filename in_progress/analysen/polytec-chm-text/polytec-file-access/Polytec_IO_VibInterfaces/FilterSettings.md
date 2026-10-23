# Polytec_IO_VibInterfaces – FilterSettings

## FilterSettings Object

*Quelle: `Polytec_IO_VibInterfaces~FilterSettings.html` · Polytec IO VibInterfaces Type Library*

### Description

The settings of a filter. Item of the FilterSettingsCollection.


---

## FilterSettings Object Members

*Quelle: `Polytec_IO_VibInterfaces~FilterSettings_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Clone | Creates and returns a copy of the settings object. |
|---|---|

### Public Properties

| Key | The type of the filter. |
|---|---|
| Name | The name of the filter. |
| Range | The range of the filter. |


---

## Clone Method

*Quelle: `Polytec_IO_VibInterfaces~FilterSettings~Clone.html` · Polytec IO VibInterfaces Type Library · FilterSettings Object : Clone Method*

### Description

Creates and returns a copy of the settings object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Variant
```


---

## Key Property

*Quelle: `Polytec_IO_VibInterfaces~FilterSettings~Key.html` · Polytec IO VibInterfaces Type Library · FilterSettings Object : Key Property*

### Description

The type of the filter.

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

*Quelle: `Polytec_IO_VibInterfaces~FilterSettings~Name.html` · Polytec IO VibInterfaces Type Library · FilterSettings Object : Name Property*

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

The name can be used as a parameter to the Contains method and the Item property.


---

## Range Property

*Quelle: `Polytec_IO_VibInterfaces~FilterSettings~Range.html` · Polytec IO VibInterfaces Type Library · FilterSettings Object : Range Property*

### Description

The range of the filter.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Range As String
```
