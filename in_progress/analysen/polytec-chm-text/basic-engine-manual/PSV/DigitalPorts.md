# PSV – DigitalPorts

## DigitalPorts Collection

*Quelle: `PSV~DigitalPorts.html` · Polytec PSV Type Library*

### Description

Collection of the available digital ports of the system.

### Object Model

### Remarks

Please note that on VibroScan systems AuxIn is mapped to the TRIG connector of the scannning head (top for 3D-systems) and AuxOut is mapped to the SYNC connector of the same scanning head. At first access to AuxOut, the output mode of the connector is automatically switched from SYNC to AuxOut. To switch the connector back to SYNC mode you have to set the AuxOutMode Property of the FrontEndControl Object. See the example below on how to do this.

### Example

Tests the Aux In / Aux Out ports of the junction box. To run this test successfully please connect Aux In and Aux Out with a suitable cable.

- Test of Aux In / Aux Out (Visual Basic)

```
Sub Main
     Dim oAuxIn As DigitalPort
     Dim oAuxOut As DigitalPort

     Set oAuxIn = Application.DigitalPorts(ptcDigitalPortIn1)
     Set oAuxOut = Application.DigitalPorts(ptcDigitalPortOut1)

     oAuxOut.Value = True
     If (oAuxIn.Value <> True) Then
          MsgBox "Please connect Aux In and Aux Out!"
          Exit Sub
     End If

     oAuxOut.Value = False
     If (oAuxIn.Value <> False) Then
          MsgBox "Please connect Aux In and Aux Out!"
          Exit Sub
     End If

     MsgBox "AuxIn / AuxOut Test succeeded!"
End Sub
```

On VibroScan systems sets the output mode of the SYNC connector of the scanning head back to SYNC.

- Example (Visual Basic)

```
'#Language "WWB.NET"

Sub Main
    Dim oFrontEnd As FrontEnd = Acquisition.Infos.Hardware.ActiveFrontEnd
    Dim oFrontEndControl As FrontEndControl = oFrontEnd.Control
    oFrontEndControl.AuxOutMode = PTCFrontEndAuxOutModeType.ptcFrontEndAuxOutModeSync
End Sub
```


---

## DigitalPorts Collection Members

*Quelle: `PSV~DigitalPorts_members.html` · Polytec PSV Type Library*

### Public Properties

| Count | The number of digital ports. |
|---|---|
| Item | Returns an item of the collection. |


---

## Count Property

*Quelle: `PSV~DigitalPorts~Count.html` · Polytec PSV Type Library · DigitalPorts Collection : Count Property*

### Description

The number of digital ports.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `PSV~DigitalPorts~Item.html` · Polytec PSV Type Library · DigitalPorts Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal PTCDigitalPort As PTCDigitalPort _
) As DigitalPort
```

### Parameters

PTCDigitalPort

| Value | Description |
|---|---|
| ptcDigitalPortGate | The port representing the Gate connector. |
| ptcDigitalPortIn1 | The port representing the Aux In connector. |
| ptcDigitalPortOut1 | The port representing the Aux Out connector. |
The type of the digital port.
