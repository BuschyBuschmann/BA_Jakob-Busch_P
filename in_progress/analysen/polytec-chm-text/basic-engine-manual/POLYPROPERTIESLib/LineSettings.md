# POLYPROPERTIESLib – LineSettings

## LineSettings Object

*Quelle: `POLYPROPERTIESLib~LineSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings of a line of a graph of an AnalyzerView. Member of the LineSettingsCollection.

### Object Model


---

## LineSettings Object Members

*Quelle: `POLYPROPERTIESLib~LineSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Color | Specifies the color of the line. |
|---|---|
| Marker | Specifies the marker style of the line. |
| Modified | Returns whether the settings object has been modified. |
| Name | The name of the line. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Style | Specifies the line style. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~LineSettings~Clone.html` · Polytec PolyProperties Type Library · LineSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~LineSettings~Copy.html` · Polytec PolyProperties Type Library · LineSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~LineSettings~Equal.html` · Polytec PolyProperties Type Library · LineSettings Object : Equal Method*

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

## Color Property

*Quelle: `POLYPROPERTIESLib~LineSettings~Color.html` · Polytec PolyProperties Type Library · LineSettings Object : Color Property*

### Description

Specifies the color of the line.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Color As PTCColor
```


---

## Marker Property

*Quelle: `POLYPROPERTIESLib~LineSettings~Marker.html` · Polytec PolyProperties Type Library · LineSettings Object : Marker Property*

### Description

Specifies the marker style of the line.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Marker As PTCMarkerStyle
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~LineSettings~Modified.html` · Polytec PolyProperties Type Library · LineSettings Object : Modified Property*

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

## Name Property

*Quelle: `POLYPROPERTIESLib~LineSettings~Name.html` · Polytec PolyProperties Type Library · LineSettings Object : Name Property*

### Description

The name of the line.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Parent Property

*Quelle: `POLYPROPERTIESLib~LineSettings~Parent.html` · Polytec PolyProperties Type Library · LineSettings Object : Parent Property*

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

## Style Property

*Quelle: `POLYPROPERTIESLib~LineSettings~Style.html` · Polytec PolyProperties Type Library · LineSettings Object : Style Property*

### Description

Specifies the line style.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Style As PTCLineStyle
```
