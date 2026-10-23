# POLYPROPERTIESLib – AnalyzerPinSettings

## AnalyzerPinSettings Object

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings for pinning analyzer view settings to other open analyzer views.

### Object Model


---

## AnalyzerPinSettings Object Members

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| Abscissa | Specifies the abscissa pin state. |
|---|---|
| Axes | Specifies whether the axes settings of the analyzer should be pinned to other analyzers. |
| Cursor | Specifies whether the cursor settings of the analyzer should be pinned to other analyzers. |
| General | Specifies whether the general settings of the analyzer should be pinned to other analyzers. |
| Lines | Specifies whether the lines settings of the analyzer should be pinned to other analyzers. |
| Modified | Returns whether the settings object has been modified. |
| Ordinate | Specifies the ordinate pin state. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Signal | Specifies whether the signal settings of the analyzer should be pinned to other analyzers. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Clone.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Copy.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Equal.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Equal Method*

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

## Abscissa Property

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Abscissa.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Abscissa Property*

### Description

Specifies the abscissa pin state.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Abscissa As Boolean
```


---

## Axes Property

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Axes.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Axes Property*

### Description

Specifies whether the axes settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Axes As Boolean
```


---

## Cursor Property

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Cursor.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Cursor Property*

### Description

Specifies whether the cursor settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Cursor As Boolean
```


---

## General Property

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~General.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : General Property*

### Description

Specifies whether the general settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property General As Boolean
```


---

## Lines Property

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Lines.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Lines Property*

### Description

Specifies whether the lines settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Lines As Boolean
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Modified.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Modified Property*

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

## Ordinate Property

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Ordinate.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Ordinate Property*

### Description

Specifies the ordinate pin state.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Ordinate As Boolean
```


---

## Parent Property

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Parent.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Parent Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerPinSettings~Signal.html` · Polytec PolyProperties Type Library · AnalyzerPinSettings Object : Signal Property*

### Description

Specifies whether the signal settings of the analyzer should be pinned to other analyzers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Signal As Boolean
```
