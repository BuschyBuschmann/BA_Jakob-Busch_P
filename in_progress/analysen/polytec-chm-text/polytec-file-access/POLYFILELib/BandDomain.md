# POLYFILELib – BandDomain

## BandDomain Object

*Quelle: `POLYFILELib~BandDomain.html` · Polytec PolyFile Type Library*

### Description

Item of the BandDomains collection.

### Object Model


---

## BandDomain Object Members

*Quelle: `POLYFILELib~BandDomain_members.html` · Polytec PolyFile Type Library*

### Public Methods

| GetDataBands | Gets the DataBands Collection for the given signal. |
|---|---|

### Public Properties

| Channels | Returns the Channels collection. |
|---|---|
| DataBands | property DataBands |
| Name | Returns the name of the BandDomain. Can be used as an index to the BandDomains collection . |
| Type | Returns the type of the BandDomain. Can be used as an index to the BandDomains collection . |


---

## GetDataBands Method

*Quelle: `POLYFILELib~BandDomain~GetDataBands.html` · Polytec PolyFile Type Library · BandDomain Object : GetDataBands Method*

### Description

Gets the DataBands Collection for the given signal.

### Syntax

*Visual Basic:*
```
Public Function GetDataBands( _
   ByVal pISignal As ISignal5 _
) As DataBands
```

### Parameters

pISignal

The signal to get the DataBands Collection for.

### Return Type

The DataBands Collection.


---

## Channels Property

*Quelle: `POLYFILELib~BandDomain~Channels.html` · Polytec PolyFile Type Library · BandDomain Object : Channels Property*

### Description

Returns the Channels collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Channels As IChannels2
```


---

## DataBands Property

*Quelle: `POLYFILELib~BandDomain~DataBands.html` · Polytec PolyFile Type Library · BandDomain Object : DataBands Property*

### Description

property DataBands

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DataBands As IDataBands
```


---

## Name Property

*Quelle: `POLYFILELib~BandDomain~Name.html` · Polytec PolyFile Type Library · BandDomain Object : Name Property*

### Description

Returns the name of the BandDomain. Can be used as an index to the BandDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `POLYFILELib~BandDomain~Type.html` · Polytec PolyFile Type Library · BandDomain Object : Type Property*

### Description

Returns the type of the BandDomain. Can be used as an index to the BandDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCDomainType
```
