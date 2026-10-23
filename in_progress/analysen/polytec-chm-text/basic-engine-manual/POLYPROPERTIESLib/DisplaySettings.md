# POLYPROPERTIESLib – DisplaySettings

## DisplaySettings Object

*Quelle: `POLYPROPERTIESLib~DisplaySettings.html` · Polytec PolyProperties Type Library*

### Description

User interface settings for the kind of data to display in an AnalyzerView or AreaView.

### Object Model


---

## DisplaySettings Object Members

*Quelle: `POLYPROPERTIESLib~DisplaySettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Channel | Specifies the name of the channel. |
|---|---|
| Display | Specifies the type of the display. |
| Domain | Specifies the domain type. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Signal | Specifies the name of the signal. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~DisplaySettings~Clone.html` · Polytec PolyProperties Type Library · DisplaySettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```

### Remarks

This object can either be attached to a parent object or not. If it is attached, the Parent property returns the attached parent. In this case, changes to the object are directly applied to the user interface. You can create settings objects that are not attached to a parent by calling Clone() on a settings object or by creating a new settings object. Assigning such an object to a suitable Settings property of a parent object applies all properties to the user interface at the time of the assignment. Assignment of a settings object copies all properties to the settings object attached to its parent. The detached settings object will be still detached after the assignment.

You can quickly copy settings e.g. between different windows by directly assigning the settings object of one window to the settings property of the other.


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~DisplaySettings~Copy.html` · Polytec PolyProperties Type Library · DisplaySettings Object : Copy Method*

### Description

Copies the properties of the given settings object to this settings object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal UISettings As IUISettings _
)
```

### Parameters

UISettings

The other settings object.


---

## Equal Method

*Quelle: `POLYPROPERTIESLib~DisplaySettings~Equal.html` · Polytec PolyProperties Type Library · DisplaySettings Object : Equal Method*

### Description

Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values.

### Syntax

*Visual Basic:*
```
Public Function Equal( _
   ByVal UISettings As IUISettings _
) As Boolean
```

### Parameters

UISettings

The other settings object.

### Return Type

True if all properties are equal.


---

## Channel Property

*Quelle: `POLYPROPERTIESLib~DisplaySettings~Channel.html` · Polytec PolyProperties Type Library · DisplaySettings Object : Channel Property*

### Description

Specifies the name of the channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Channel As String
```


---

## Display Property

*Quelle: `POLYPROPERTIESLib~DisplaySettings~Display.html` · Polytec PolyProperties Type Library · DisplaySettings Object : Display Property*

### Description

Specifies the type of the display.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Display As PTCDisplayType
```


---

## Domain Property

*Quelle: `POLYPROPERTIESLib~DisplaySettings~Domain.html` · Polytec PolyProperties Type Library · DisplaySettings Object : Domain Property*

### Description

Specifies the domain type.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Domain As PTCDomainType
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~DisplaySettings~Modified.html` · Polytec PolyProperties Type Library · DisplaySettings Object : Modified Property*

### Description

Returns whether the settings object has been modified.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Modified As Boolean
```


---

## Parent Property

*Quelle: `POLYPROPERTIESLib~DisplaySettings~Parent.html` · Polytec PolyProperties Type Library · DisplaySettings Object : Parent Property*

### Description

The parent of the settings object, if the object is attached, or nothing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Parent As Object
```


---

## Signal Property

*Quelle: `POLYPROPERTIESLib~DisplaySettings~Signal.html` · Polytec PolyProperties Type Library · DisplaySettings Object : Signal Property*

### Description

Specifies the name of the signal.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Signal As String
```
