# POLYSIGNALLib – FunctionAtNodeDirections

## FunctionAtNodeDirections Object

*Quelle: `POLYSIGNALLib~FunctionAtNodeDirections.html` · Polytec PolySignal Type Library*

### Description

The FunctionAtNodeDirections object provides a list of all PTCFunctionAtNodeDirection enumerator values and their string representations. You can use the object e.g. to create a user interface to let the user select a value.

### Remarks

Supported languages are English (US) and German (Germany). All other system languages default to English (US).

### Example

The following example lists all PTCFunctionAtNodeDirection enumerator values and their string representations in the current system language and in German.

- List FunctionAtNodeDirections (Visual Basic)

```
Option Explicit

Sub Main
    Debug.Clear

    Dim oFunctionAtNodeDirections As New FunctionAtNodeDirections
    Dim index As Long
    For index = 0 To oFunctionAtNodeDirections.Count-1
        Dim ptcDirection As PTCFunctionAtNodeDirection
        ptcDirection = oFunctionAtNodeDirections.GetEnumItem(index)
        Dim strGerman As String
        strGerman = oFunctionAtNodeDirections.GetLocaleString(ptcDirection, &H407)
        Dim strDefault As String
        strDefault = oFunctionAtNodeDirections.GetString(ptcDirection)
        Debug.Print "Index: ";index;" Enum: ";ptcDirection;" German: ";strGerman; " Default: ";strDefault
    Next
End Sub
```


---

## FunctionAtNodeDirections Object Members

*Quelle: `POLYSIGNALLib~FunctionAtNodeDirections_members.html` · Polytec PolySignal Type Library*

### Public Methods

| GetEnumItem | Gets the enumerator value for the given index. |
|---|---|
| GetIndex | Gets the index for the given enumerator value. |
| GetLocaleString | Gets the string representation for the given enumerator value in the given locale. |
| GetString | Gets the string representation for the given enumerator value in the current system locale. |

### Public Properties

| Count | The number of enumerator values. |
|---|---|


---

## GetEnumItem Method

*Quelle: `POLYSIGNALLib~FunctionAtNodeDirections~GetEnumItem.html` · Polytec PolySignal Type Library · FunctionAtNodeDirections Object : GetEnumItem Method*

### Description

Gets the enumerator value for the given index.

### Syntax

*Visual Basic:*
```
Public Function GetEnumItem( _
   ByVal lIndex As Long _
) As PTCFunctionAtNodeDirection
```

### Parameters

lIndex

The 0-based index of the enumerator value.


---

## GetIndex Method

*Quelle: `POLYSIGNALLib~FunctionAtNodeDirections~GetIndex.html` · Polytec PolySignal Type Library · FunctionAtNodeDirections Object : GetIndex Method*

### Description

Gets the index for the given enumerator value.

### Syntax

*Visual Basic:*
```
Public Function GetIndex( _
   ByVal ptcDirection As PTCFunctionAtNodeDirection _
) As Long
```

### Parameters

ptcDirection

| Value | Description |
|---|---|
| ptcMinusXRotation | Negative rotation X direction |
| ptcMinusXTranslation | Negative translation X direction |
| ptcMinusYRotation | Negative rotation Y direction |
| ptcMinusYTranslation | Negative translation Y direction |
| ptcMinusZRotation | Negative rotation Z direction |
| ptcMinusZTranslation | Negative translation Z direction |
| ptcPlusXRotation | Positive rotation X direction |
| ptcPlusXTranslation | Positive translation X direction |
| ptcPlusYRotation | Positive rotation Y direction |
| ptcPlusYTranslation | Positive translation Y direction |
| ptcPlusZRotation | Positive rotation Z direction |
| ptcPlusZTranslation | Positive translation Z direction |
| ptcScalarDir | Signal is scalar, no direction |
| ptcVector | Signal is vector (3D) |
The direction enumerator value.

### Return Type

The 0-based index for the given enumerator value.


---

## GetLocaleString Method

*Quelle: `POLYSIGNALLib~FunctionAtNodeDirections~GetLocaleString.html` · Polytec PolySignal Type Library · FunctionAtNodeDirections Object : GetLocaleString Method*

### Description

Gets the string representation for the given enumerator value in the given locale.

### Syntax

*Visual Basic:*
```
Public Function GetLocaleString( _
   ByVal ptcDirection As PTCFunctionAtNodeDirection, _
   ByVal lLocaleID As Long _
) As String
```

### Parameters

ptcDirection

| Value | Description |
|---|---|
| ptcMinusXRotation | Negative rotation X direction |
| ptcMinusXTranslation | Negative translation X direction |
| ptcMinusYRotation | Negative rotation Y direction |
| ptcMinusYTranslation | Negative translation Y direction |
| ptcMinusZRotation | Negative rotation Z direction |
| ptcMinusZTranslation | Negative translation Z direction |
| ptcPlusXRotation | Positive rotation X direction |
| ptcPlusXTranslation | Positive translation X direction |
| ptcPlusYRotation | Positive rotation Y direction |
| ptcPlusYTranslation | Positive translation Y direction |
| ptcPlusZRotation | Positive rotation Z direction |
| ptcPlusZTranslation | Positive translation Z direction |
| ptcScalarDir | Signal is scalar, no direction |
| ptcVector | Signal is vector (3D) |
The direction enumerator value.

lLocaleID

The locale identifier.

### Remarks

Supported values are &H0407 for German (Germany) and &H0409 for English (US).


---

## GetString Method

*Quelle: `POLYSIGNALLib~FunctionAtNodeDirections~GetString.html` · Polytec PolySignal Type Library · FunctionAtNodeDirections Object : GetString Method*

### Description

Gets the string representation for the given enumerator value in the current system locale.

### Syntax

*Visual Basic:*
```
Public Function GetString( _
   ByVal ptcDirection As PTCFunctionAtNodeDirection _
) As String
```

### Parameters

ptcDirection

| Value | Description |
|---|---|
| ptcMinusXRotation | Negative rotation X direction |
| ptcMinusXTranslation | Negative translation X direction |
| ptcMinusYRotation | Negative rotation Y direction |
| ptcMinusYTranslation | Negative translation Y direction |
| ptcMinusZRotation | Negative rotation Z direction |
| ptcMinusZTranslation | Negative translation Z direction |
| ptcPlusXRotation | Positive rotation X direction |
| ptcPlusXTranslation | Positive translation X direction |
| ptcPlusYRotation | Positive rotation Y direction |
| ptcPlusYTranslation | Positive translation Y direction |
| ptcPlusZRotation | Positive rotation Z direction |
| ptcPlusZTranslation | Positive translation Z direction |
| ptcScalarDir | Signal is scalar, no direction |
| ptcVector | Signal is vector (3D) |
The direction enumerator value.

### Remarks

Supported languages are English (US) and German (Germany). All other system languages default to English (US).


---

## Count Property

*Quelle: `POLYSIGNALLib~FunctionAtNodeDirections~Count.html` · Polytec PolySignal Type Library · FunctionAtNodeDirections Object : Count Property*

### Description

The number of enumerator values.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```
