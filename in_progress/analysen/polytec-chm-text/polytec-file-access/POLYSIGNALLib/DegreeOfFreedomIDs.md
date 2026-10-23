# POLYSIGNALLib – DegreeOfFreedomIDs

## DegreeOfFreedomIDs Collection

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs.html` · Polytec PolySignal Type Library*

### Description

The collection of the degree of freedom identifiers of responses or references.

### Object Model

### Remarks

The reference and response degree of freedom identifiers describe the source channels of the signal. For signals of the vibrometer channels (Vib, Vib 3D, Vib X, Vib Y, Vib Z) there are one or three (for 3D signals) response channels but no reference channel. For combined signals like FRF, H1 or H2 there are one or three (for 3D signals) response channels and a single reference channel. For virtual coherences (ptcFunctionPCAVirtualCoherenceType) there is a response channel and several reference channels. For reference signals, there are one or more (only for function type ptcFunctionPCAPrincipalInputsType) reference channels and no response channels.

The recommended way to initialize this collection is by using the Assign Method.


---

## DegreeOfFreedomIDs Collection Members

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs_members.html` · Polytec PolySignal Type Library*

### Public Methods

| Add | Adds a new degree of freedom identifier to the collection. |
|---|---|
| Assign | Clears the collection and assigns new degree of freedom identifiers to the collection. The properties of the created objects are initialized with the parameters passed to assign. See the remarks section for more details. |
| Clear | Clears the collection by removing all items in the collection. |
| Clone | Creates a copy of the collection. |
| Copy | Clears the collection and then copies all properties and items of the given collection. |
| IsEqual | Returns true when the properties and items of the collection are equal to the properties and items of the given collection. |

### Public Properties

| ChannelName | The name of the channel of the degree of freedom identifiers. |
|---|---|
| Count | The number of degree of freedom identifiers in the collection. |
| Direction | The direction of the degree of freedom identifiers. |
| Item | Returns the item of the collection with the given index. |


---

## Add Method

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~Add.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : Add Method*

### Description

Adds a new degree of freedom identifier to the collection.

### Syntax

*Visual Basic:*
```
Public Function Add() As DegreeOfFreedomID
```

### Return Type

The newly created degree of freedom identifier.


---

## Assign Method

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~Assign.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : Assign Method*

### Description

Clears the collection and assigns new degree of freedom identifiers to the collection. The properties of the created objects are initialized with the parameters passed to assign. See the remarks section for more details.

### Syntax

*Visual Basic:*
```
Public Sub Assign( _
   ByVal lNode As Long, _
   ByVal ptcDirection As PTCFunctionAtNodeDirection, _
   ByVal bstrChannelName As String, _
   ByVal bstrQuantity As String, _
   ByVal bstrUnit As String _
)
```

### Parameters

lNode

The node number of the degree of freedom identifiers that are created.

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
The direction of the degree of freedom identifiers that are created. For ptcVector please see the remarks section.

bstrChannelName

The channel name of the degree of freedom identifiers. The channel name is also assigned to the ChannelName Property of the DegreeOfFreedomIDs Object. For ptcVector please see the remarks section.

bstrQuantity

The quantity of the degree of freedom identifiers.

bstrUnit

The unit of the degree of freedom identifiers.

### Remarks

When ptcVector is passed as the direction parameter of Assign, three DegreeOfFreedomID Objects are created. The direction of the first object is set to ptcPlusXTranslation, the direction of the second object is set to ptcPlusYTranslation and the direction of the third object is set to ptcPlusZTranslation. The channel names of the objects are set to the channel name passed to Assign appended by "X", "Y" and "Z" respectively. The channel name of the DegreeOfFreedomIDs Collection is set to the channel name passed to Assign appended by "3D".


---

## Clear Method

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~Clear.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : Clear Method*

### Description

Clears the collection by removing all items in the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Clone Method

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~Clone.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : Clone Method*

### Description

Creates a copy of the collection.

### Syntax

*Visual Basic:*
```
Public Function Clone() As DegreeOfFreedomIDs
```

### Return Type

The copy of the collection.


---

## Copy Method

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~Copy.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : Copy Method*

### Description

Clears the collection and then copies all properties and items of the given collection.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIDegreeOfFreedomIDs As DegreeOfFreedomIDs _
)
```

### Parameters

pIDegreeOfFreedomIDs

The collection to copy the properties and items from.


---

## IsEqual Method

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~IsEqual.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : IsEqual Method*

### Description

Returns true when the properties and items of the collection are equal to the properties and items of the given collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIDegreeOfFreedomIDs As DegreeOfFreedomIDs _
) As Boolean
```

### Parameters

pIDegreeOfFreedomIDs

The collection to compare the properties and items with.

### Return Type

True when the collection is equal to the given collection.


---

## ChannelName Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~ChannelName.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : ChannelName Property*

### Description

The name of the channel of the degree of freedom identifiers.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ChannelName As String
```

### Remarks

When the collection contains a single degree of freedom identifier, the channel name should be set to the channel name of this identifier. Consider to use the Assign Method to fill the collection, which sets this property automatically.


---

## Count Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~Count.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : Count Property*

### Description

The number of degree of freedom identifiers in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Direction Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~Direction.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : Direction Property*

### Description

The direction of the degree of freedom identifiers.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Direction As PTCFunctionAtNodeDirection
```

### Return Type

Returns ptcVector when the number of degree of freedom identifiers in the collection is three and the direction of the identifiers is ptcPlusXTranslation, ptcPlusYTranslation and ptcPlusZTranslation, respectively. Otherwise, the direction of the first identifier is returned. When the collection is empty, an error occurs when accessing the property.


---

## Item Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomIDs~Item.html` · Polytec PolySignal Type Library · DegreeOfFreedomIDs Collection : Item Property*

### Description

Returns the item of the collection with the given index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal lIndex As Long _
) As DegreeOfFreedomID
```

### Parameters

lIndex

The one-based index of the item of the collection.

### Return Type

The degree of freedom identifier with the given index.
