# POLYSIGNALLib – DegreeOfFreedomID

## DegreeOfFreedomID Object

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID.html` · Polytec PolySignal Type Library*

### Description

Item of the DegreeOfFreedomIDs Collection describing a response or reference degree of freedom identifier.

### Object Model


---

## DegreeOfFreedomID Object Members

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID_members.html` · Polytec PolySignal Type Library*

### Public Methods

| Clone | Creates and returns a copy of the DegreeOfFreedomID object. |
|---|---|
| Copy | Copies the properties of another DegreeOfFreedomID object to this object. |

### Public Properties

| ChannelName | The channel name of the degree of freedom identifier. |
|---|---|
| Direction | The direction of the degree of freedom identifier. |
| Node | The node number of the degree of freedom identifier. |
| NodeDescription | The description for the node of the degree of freedom identifier. |
| Quantity | The quantity of the channel of the degree of freedom identifier. |
| Unit | The unit of the channel of the degree of freedom identifier. |


---

## Clone Method

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID~Clone.html` · Polytec PolySignal Type Library · DegreeOfFreedomID Object : Clone Method*

### Description

Creates and returns a copy of the DegreeOfFreedomID object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As DegreeOfFreedomID
```


---

## Copy Method

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID~Copy.html` · Polytec PolySignal Type Library · DegreeOfFreedomID Object : Copy Method*

### Description

Copies the properties of another DegreeOfFreedomID object to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIDegreeOfFreedomID As DegreeOfFreedomID _
)
```

### Parameters

pIDegreeOfFreedomID

The other DegreeOfFreedomID object.


---

## ChannelName Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID~ChannelName.html` · Polytec PolySignal Type Library · DegreeOfFreedomID Object : ChannelName Property*

### Description

The channel name of the degree of freedom identifier.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ChannelName As String
```


---

## Direction Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID~Direction.html` · Polytec PolySignal Type Library · DegreeOfFreedomID Object : Direction Property*

### Description

The direction of the degree of freedom identifier.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Direction As PTCFunctionAtNodeDirection
```


---

## Node Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID~Node.html` · Polytec PolySignal Type Library · DegreeOfFreedomID Object : Node Property*

### Description

The node number of the degree of freedom identifier.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Node As Long
```

### Remarks

It is recommended to use -1 for roving response degree of freedom identifiers, e.g. for signals that are measured at every scan point. For reference degree of freedom identifiers set this property to the index (i.e. label) of the scan point where the reference was measured.


---

## NodeDescription Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID~NodeDescription.html` · Polytec PolySignal Type Library · DegreeOfFreedomID Object : NodeDescription Property*

### Description

The description for the node of the degree of freedom identifier.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property NodeDescription As String
```


---

## Quantity Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID~Quantity.html` · Polytec PolySignal Type Library · DegreeOfFreedomID Object : Quantity Property*

### Description

The quantity of the channel of the degree of freedom identifier.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Quantity As String
```


---

## Unit Property

*Quelle: `POLYSIGNALLib~DegreeOfFreedomID~Unit.html` · Polytec PolySignal Type Library · DegreeOfFreedomID Object : Unit Property*

### Description

The unit of the channel of the degree of freedom identifier.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Unit As String
```
