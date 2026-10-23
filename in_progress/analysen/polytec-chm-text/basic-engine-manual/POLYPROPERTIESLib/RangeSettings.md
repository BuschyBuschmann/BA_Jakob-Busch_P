# POLYPROPERTIESLib – RangeSettings

## RangeSettings Object

*Quelle: `POLYPROPERTIESLib~RangeSettings.html` · Polytec PolyProperties Type Library*

### Description

User interface settings of an axis range of an AnalyzerView or SpectrogramAreaView.

### Object Model


---

## RangeSettings Object Members

*Quelle: `POLYPROPERTIESLib~RangeSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Log | Specifies whether the range is logarithmic. |
|---|---|
| Max | Specifies the end of the range. |
| Min | Specifies the start of the range. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| RoundValues | Specifies whether the range shall be rounded to the next ticks of the axis. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~RangeSettings~Clone.html` · Polytec PolyProperties Type Library · RangeSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~RangeSettings~Copy.html` · Polytec PolyProperties Type Library · RangeSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~RangeSettings~Equal.html` · Polytec PolyProperties Type Library · RangeSettings Object : Equal Method*

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

## Log Property

*Quelle: `POLYPROPERTIESLib~RangeSettings~Log.html` · Polytec PolyProperties Type Library · RangeSettings Object : Log Property*

### Description

Specifies whether the range is logarithmic.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Log As Boolean
```


---

## Max Property

*Quelle: `POLYPROPERTIESLib~RangeSettings~Max.html` · Polytec PolyProperties Type Library · RangeSettings Object : Max Property*

### Description

Specifies the end of the range.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Max As Double
```


---

## Min Property

*Quelle: `POLYPROPERTIESLib~RangeSettings~Min.html` · Polytec PolyProperties Type Library · RangeSettings Object : Min Property*

### Description

Specifies the start of the range.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Min As Double
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~RangeSettings~Modified.html` · Polytec PolyProperties Type Library · RangeSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~RangeSettings~Parent.html` · Polytec PolyProperties Type Library · RangeSettings Object : Parent Property*

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

## RoundValues Property

*Quelle: `POLYPROPERTIESLib~RangeSettings~RoundValues.html` · Polytec PolyProperties Type Library · RangeSettings Object : RoundValues Property*

### Description

Specifies whether the range shall be rounded to the next ticks of the axis.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RoundValues As Boolean
```
