# Polytec_IO_VibInterfaces – VideoCameraSettings

## VideoCameraSettings Object

*Quelle: `Polytec_IO_VibInterfaces~VideoCameraSettings.html` · Polytec IO VibInterfaces Type Library*

### Description

The settings of the video camera.


---

## VideoCameraSettings Object Members

*Quelle: `Polytec_IO_VibInterfaces~VideoCameraSettings_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Clone | Creates and returns a copy of the video camera settings object. |
|---|---|
| Copy | Copies all properties of the given settings object to this object. |

### Public Properties

| AutomaticGainControl | Specifies, whether automatic gain control is active. |
|---|---|
| Gamma | Specifies the gamma value of the camera. |
| ManualGain | Specifies the manual gain value. |
| Mirror | Specifies the mirror mode. |
| ShutterSpeed | Specifies the shutter speed. |


---

## Clone Method

*Quelle: `Polytec_IO_VibInterfaces~VideoCameraSettings~Clone.html` · Polytec IO VibInterfaces Type Library · VideoCameraSettings Object : Clone Method*

### Description

Creates and returns a copy of the video camera settings object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Variant
```


---

## Copy Method

*Quelle: `Polytec_IO_VibInterfaces~VideoCameraSettings~Copy.html` · Polytec IO VibInterfaces Type Library · VideoCameraSettings Object : Copy Method*

### Description

Copies all properties of the given settings object to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal VideoCameraSettings As VideoCameraSettings _
)
```

### Parameters

VideoCameraSettings

The settings object to copy the properties from.


---

## AutomaticGainControl Property

*Quelle: `Polytec_IO_VibInterfaces~VideoCameraSettings~AutomaticGainControl.html` · Polytec IO VibInterfaces Type Library · VideoCameraSettings Object : AutomaticGainControl Property*

### Description

Specifies, whether automatic gain control is active.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AutomaticGainControl As Boolean
```


---

## Gamma Property

*Quelle: `Polytec_IO_VibInterfaces~VideoCameraSettings~Gamma.html` · Polytec IO VibInterfaces Type Library · VideoCameraSettings Object : Gamma Property*

### Description

Specifies the gamma value of the camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Gamma As Long
```


---

## ManualGain Property

*Quelle: `Polytec_IO_VibInterfaces~VideoCameraSettings~ManualGain.html` · Polytec IO VibInterfaces Type Library · VideoCameraSettings Object : ManualGain Property*

### Description

Specifies the manual gain value.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ManualGain As Long
```

### Remarks

If AutomaticGainControl is true, this value is ignored.


---

## Mirror Property

*Quelle: `Polytec_IO_VibInterfaces~VideoCameraSettings~Mirror.html` · Polytec IO VibInterfaces Type Library · VideoCameraSettings Object : Mirror Property*

### Description

Specifies the mirror mode.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Mirror As Boolean
```


---

## ShutterSpeed Property

*Quelle: `Polytec_IO_VibInterfaces~VideoCameraSettings~ShutterSpeed.html` · Polytec IO VibInterfaces Type Library · VideoCameraSettings Object : ShutterSpeed Property*

### Description

Specifies the shutter speed.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShutterSpeed As String
```
