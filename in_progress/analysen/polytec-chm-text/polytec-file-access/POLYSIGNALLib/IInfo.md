# POLYSIGNALLib – IInfo

## IInfo Interface

*Quelle: `POLYSIGNALLib~IInfo.html` · Polytec PolySignal Type Library*

### Description

Info is the base object of all objects returned by the Infos collection. This object is not directly accessible.

### Remarks

It is recommended to cast to the Info Object


---

## IInfo Interface Members

*Quelle: `POLYSIGNALLib~IInfo_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Name | Returns the name of the Info object. This name can be used as an index to the Item and Exists properties of the Infos collection. |
|---|---|
| Type | Returns the type of the Info object. This type can be used as an parameter for the Type property of the Infos collection. |


---

## Name Property

*Quelle: `POLYSIGNALLib~IInfo~Name.html` · Polytec PolySignal Type Library · IInfo Interface : Name Property*

### Description

Returns the name of the Info object. This name can be used as an index to the Item and Exists properties of the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `POLYSIGNALLib~IInfo~Type.html` · Polytec PolySignal Type Library · IInfo Interface : Type Property*

### Description

 Returns the type of the Info object. This type can be used as an parameter for the Type property of the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

PTCInfoType
