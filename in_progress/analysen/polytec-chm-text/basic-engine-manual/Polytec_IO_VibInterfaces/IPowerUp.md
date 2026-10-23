# Polytec_IO_VibInterfaces – IPowerUp

## IPowerUp Interface

*Quelle: `Polytec_IO_VibInterfaces~IPowerUp.html` · Polytec IO VibInterfaces Type Library*

### Description

The IPowerUp object provides access to the power up functionality of the vibrometer controller.


---

## IPowerUp Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IPowerUp_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| GetName | Gets the string representation of the given power up mode. |
|---|---|
| HasCap | Checks, if the controller has the given capability. |
| SetMode | Sets the given power up mode of the controller. |

### Public Properties

| Caps | The capabilities of the power up object. |
|---|---|
| Mode | The current power up mode of the controller. |


---

## GetName Method

*Quelle: `Polytec_IO_VibInterfaces~IPowerUp~GetName.html` · Polytec IO VibInterfaces Type Library · IPowerUp Interface : GetName Method*

### Description

Gets the string representation of the given power up mode.

### Syntax

*Visual Basic:*
```
Public Function GetName( _
   ByVal parameter As PowerUPMode _
) As String
```

### Parameters

parameter

| Value | Description |
|---|---|
| PowerUPMode_Default | The controller starts with the default settings. |
| PowerUPMode_Last | The controller starts with the last settings used. |
| PowerUPMode_LloMode | The controller starts in Local Lock Out mode and is controllable by software only. |
| PowerUPMode_User | The controller starts with the user-defined settings. |
| PowerUPMode_User1 | The controller starts with the user-defined settings 1. |
| PowerUPMode_User2 | The controller starts with the user-defined settings 2. |
| PowerUPMode_User3 | The controller starts with the user-defined settings 3. |
The power up mode.


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~IPowerUp~HasCap.html` · Polytec IO VibInterfaces Type Library · IPowerUp Interface : HasCap Method*

### Description

Checks, if the controller has the given capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As PowerUpCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| PowerUpCaps_Default | The controller can start with default settings. |
| PowerUpCaps_Last | The controller can start with the last settings used. |
| PowerUpCaps_Llo | The controller can start in Local Lock Out mode. |
| PowerUpCaps_None | No power up capability. |
| PowerUpCaps_User | The controller can start with user-defined settings. |
| PowerUpCaps_User1 | The controller can start with user-defined settings 1. |
| PowerUpCaps_User2 | The controller can start with user-defined settings 2. |
| PowerUpCaps_User3 | The controller can start with user-defined settings 3. |
The power up capability.

### Return Type

True, if the controller has the given capability.


---

## SetMode Method

*Quelle: `Polytec_IO_VibInterfaces~IPowerUp~SetMode.html` · Polytec IO VibInterfaces Type Library · IPowerUp Interface : SetMode Method*

### Description

Sets the given power up mode of the controller.

### Syntax

*Visual Basic:*
```
Public Sub SetMode( _
   ByVal parameter As PowerUPMode _
)
```

### Parameters

parameter

| Value | Description |
|---|---|
| PowerUPMode_Default | The controller starts with the default settings. |
| PowerUPMode_Last | The controller starts with the last settings used. |
| PowerUPMode_LloMode | The controller starts in Local Lock Out mode and is controllable by software only. |
| PowerUPMode_User | The controller starts with the user-defined settings. |
| PowerUPMode_User1 | The controller starts with the user-defined settings 1. |
| PowerUPMode_User2 | The controller starts with the user-defined settings 2. |
| PowerUPMode_User3 | The controller starts with the user-defined settings 3. |
The power up mode.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~IPowerUp~Caps.html` · Polytec IO VibInterfaces Type Library · IPowerUp Interface : Caps Property*

### Description

The capabilities of the power up object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As PowerUpCaps
```


---

## Mode Property

*Quelle: `Polytec_IO_VibInterfaces~IPowerUp~Mode.html` · Polytec IO VibInterfaces Type Library · IPowerUp Interface : Mode Property*

### Description

The current power up mode of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Mode As PowerUPMode
```
