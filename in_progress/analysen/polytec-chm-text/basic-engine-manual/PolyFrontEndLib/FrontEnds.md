# PolyFrontEndLib – FrontEnds

## FrontEnds Collection

*Quelle: `PolyFrontEndLib~FrontEnds.html` · Polytec PolyFrontEnd Type Library*

### Description

The typed and named collection of available front-end types.

### Object Model


---

## FrontEnds Collection Members

*Quelle: `PolyFrontEndLib~FrontEnds_members.html` · Polytec PolyFrontEnd Type Library*

### Public Methods

| Connect | Connects to the front-end. |
|---|---|
| ConnectByName | Connects to the front-end by specifying the expected identifier string. |
| ConnectEx | Connects to the front-end. |
| ConnectSelectedIOFrontEnd | Connects a front-end described by the specified identifier that was found by FindIOFrontEnds. |
| ConnectToIOFrontEnd | Connects the front-end to the Polytec.IO.FrontEnd software component. |
| ConnectToUSB | Connects to the front-end via a USB connection. |
| Disconnect | Disconnects the front-end. |
| FindIOFrontEnds | Returns all found front-ends that match the search filter. Use ConnectSelectedIOFrontEnd to connect a found front-end. The search filter describes the front-end type, e.g. 'SinglePointFrontEnd'. |
| GetInfo | Retrieves a FrontEnd object for a specific front-end type. |
| GetIOFrontEndFirmwareInfo | Returns the information needed to update the firmware of the front-end. The selected front-end identifier comes from FindIOFrontEnds. |

### Public Properties

| AcqBoard | The acquisition board type of the front-end. |
|---|---|
| AcqBoardName | The name of the acquisition board of the front-end. |
| Connected | True, if the junction box is connected. |
| Count | The number of available front-end types. |
| Exists | Returns true, if the item with the given index or name exists. |
| Item | Returns an item of the FrontEnds collection with the given index. |
| ProgramID | Specifies which application is using the front-end. |
| Type | Returns an item of the collection with the given type. |


---

## Connect Method

*Quelle: `PolyFrontEndLib~FrontEnds~Connect.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : Connect Method*

### Description

Connects to the front-end.

### Syntax

*Visual Basic:*
```
Public Function Connect() As String
```

### Return Type

The identifier string of the front-end.


---

## ConnectByName Method

*Quelle: `PolyFrontEndLib~FrontEnds~ConnectByName.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : ConnectByName Method*

### Description

Connects to the front-end by specifying the expected identifier string.

### Syntax

*Visual Basic:*
```
Public Sub ConnectByName( _
   ByVal bstrIdentifier As String _
)
```

### Parameters

bstrIdentifier

The identifier string.

### Remarks

This method can be used to simulate front-ends with the given identifier string. The method does not connect to hardware.


---

## ConnectEx Method

*Quelle: `PolyFrontEndLib~FrontEnds~ConnectEx.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : ConnectEx Method*

### Description

Connects to the front-end.

### Syntax

*Visual Basic:*
```
Public Function ConnectEx( _
   ByRef pptcConnectState As PTCFrontEndConnectStateType _
) As String
```

### Parameters

pptcConnectState

| Value | Description |
|---|---|
| ptcFrontEndConnectStateConnected | The front-end is connected. |
| ptcFrontEndConnectStateControllable | The front-end is controllable. |
| ptcFrontEndConnectStateIdentifier | The front-end identifier was found. |
| ptcFrontEndConnectStatePort | The port number of the connection. |
| ptcFrontEndConnectStateSuccess | The connection was successful. |
The state of the connection.

### Return Type

The identifier string of the front-end.


---

## ConnectSelectedIOFrontEnd Method

*Quelle: `PolyFrontEndLib~FrontEnds~ConnectSelectedIOFrontEnd.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : ConnectSelectedIOFrontEnd Method*

### Description

Connects a front-end described by the specified identifier that was found by FindIOFrontEnds.

### Syntax

*Visual Basic:*
```
Public Sub ConnectSelectedIOFrontEnd( _
   ByVal selectedFrontEndIdentifier As String _
)
```

### Parameters

selectedFrontEndIdentifier

The selected front-end identifier.


---

## ConnectToIOFrontEnd Method

*Quelle: `PolyFrontEndLib~FrontEnds~ConnectToIOFrontEnd.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : ConnectToIOFrontEnd Method*

### Description

Connects the front-end to the Polytec.IO.FrontEnd software component.

### Syntax

*Visual Basic:*
```
Public Sub ConnectToIOFrontEnd( _
   ByVal bstrIdentifier As String, _
   ByVal vbServiceMode As Boolean _
)
```

### Parameters

bstrIdentifier

The front-end identifier.

vbServiceMode

Specifies, whether the service mode of the front-end is set.


---

## ConnectToUSB Method

*Quelle: `PolyFrontEndLib~FrontEnds~ConnectToUSB.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : ConnectToUSB Method*

### Description

Connects to the front-end via a USB connection.

### Syntax

*Visual Basic:*
```
Public Function ConnectToUSB( _
   ByRef pptcConnectState As PTCFrontEndConnectStateType _
) As String
```

### Parameters

pptcConnectState

| Value | Description |
|---|---|
| ptcFrontEndConnectStateConnected | The front-end is connected. |
| ptcFrontEndConnectStateControllable | The front-end is controllable. |
| ptcFrontEndConnectStateIdentifier | The front-end identifier was found. |
| ptcFrontEndConnectStatePort | The port number of the connection. |
| ptcFrontEndConnectStateSuccess | The connection was successful. |
The connection state.

### Return Type

The identifier of the front-end.


---

## Disconnect Method

*Quelle: `PolyFrontEndLib~FrontEnds~Disconnect.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : Disconnect Method*

### Description

Disconnects the front-end.

### Syntax

*Visual Basic:*
```
Public Sub Disconnect()
```


---

## FindIOFrontEnds Method

*Quelle: `PolyFrontEndLib~FrontEnds~FindIOFrontEnds.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : FindIOFrontEnds Method*

### Description

Returns all found front-ends that match the search filter. Use ConnectSelectedIOFrontEnd to connect a found front-end. The search filter describes the front-end type, e.g. 'SinglePointFrontEnd'.

### Syntax

*Visual Basic:*
```
Public Function FindIOFrontEnds( _
   ByVal frontEndTypeSearchFilter As String _
) As String()
```

### Parameters

frontEndTypeSearchFilter

Search filter that describes the front-end type, e.g. 'SinglePointFrontEnd'.

### Return Type

The names of the found front-ends.


---

## GetInfo Method

*Quelle: `PolyFrontEndLib~FrontEnds~GetInfo.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : GetInfo Method*

### Description

Retrieves a FrontEnd object for a specific front-end type.

### Syntax

*Visual Basic:*
```
Public Function GetInfo( _
   ByVal eType As PTCFrontEndType _
) As FrontEnd
```

### Parameters

eType

| Value | Description |
|---|---|
| ptcFrontEnd_LeCroyWP725Zi | LeCroyWP7xZi |
| ptcFrontEnd_LeCroyWP725Zi_A | LeCroyWP7xZi-A |
| ptcFrontEnd_LeCroyWR204Xi | LeCroyWR204Xi, ID not used anymore |
| ptcFrontEnd_LeCroyWR8254M | LeCroyWR8254M |
| ptcFrontEnd_M4i4450 | M4i4450 |
| ptcFrontEnd_PCI4461 | PCI-4461 |
| ptcFrontEnd_PCI4462 | PCI-4462 |
| ptcFrontEnd_VibSoft_M2_40 | VibSoft-M2-40 |
| ptcFrontEnd_VibSoft_M4_25 | VibSoft-M4-25 |
| ptcFrontEnd_VibSoft_M8_25 | VibSoft-M8-25 |
| ptcFrontEnd_VibSoft_PRO | VibSoft-PRO |
| ptcFrontEnd_VibSoft_PRO_05 | VibSoft-PRO 500 kHz |
| ptcFrontEnd_VibSoft_PRO_05_3D | VibSoft-PRO-3D 500 kHz |
| ptcFrontEnd_VibSoft_PRO_05_3D_1D | VibSoft-PRO-3D (1D) 500 kHz |
| ptcFrontEnd_VibSoft_PRO_24 | VibSoft-PRO 24 MHz |
| ptcFrontEnd_VibSoft_PRO_24_3D | VibSoft-PRO-3D 24 MHz |
| ptcFrontEnd_VibSoft_PRO_24_3D_1D | VibSoft-PRO-3D (1D) 24 MHz |
| ptcFrontEnd_VibSoft_PRO_3 | VibSoft-PRO 3 MHz |
| ptcFrontEnd_VibSoft_PRO_3_3D | VibSoft-PRO-3D 3 MHz |
| ptcFrontEnd_VibSoft_PRO_3_3D_1D | VibSoft-PRO-3D (1D) 3 MHz |
| ptcFrontEnd_VibSoft_PRO_3D | VibSoft-PRO-3D |
| ptcFrontEnd_VibSoft_PRO_3D_1D | VibSoft-PRO-3D (1D) |
| ptcFrontEndBNC2140 | BNC 2140, ID not used anymore |
| ptcFrontEndIVS500 | IVS-500 |
| ptcFrontEndMPV_E_800 | MPV-E-800 |
| ptcFrontEndMSA_E_050_1000 | MSA-E-050-1000 |
| ptcFrontEndMSA_E_050_1004 | MSA-E-050-1004 |
| ptcFrontEndMSA_E_050_1D_1004 | MSA-E-050-1D-1004, ID not used anymore |
| ptcFrontEndMSA_E_050_1D_84 | MSA-E-050-1D-84, ID not used anymore |
| ptcFrontEndMSA_E_050_3D_1004 | MSA-E-050-3D-1004, ID not used anymore |
| ptcFrontEndMSA_E_050_3D_1D_1004 | MSA-E-050-3D-1D-1004, ID not used anymore |
| ptcFrontEndMSA_E_050_3D_1D_84 | MSA-E-050-3D-1D-84, ID not used anymore |
| ptcFrontEndMSA_E_050_3D_84 | MSA-E-050-3D-84, ID not used anymore |
| ptcFrontEndMSA_E_050_80 | MSA-E-050-80 |
| ptcFrontEndMSA_E_050_84 | MSA-E-050-84 |
| ptcFrontEndMSA_E_050_M2_20 | MSA-E-050-M2-20 |
| ptcFrontEndMSA_E_060_PRO | MSA-E-060-PRO |
| ptcFrontEndMSA_E_060_PRO_05 | MSA-E-060-PRO 500 kHz |
| ptcFrontEndMSA_E_060_PRO_24 | MSA-E-060-PRO 24 MHz |
| ptcFrontEndMSA_E_060_PRO_3 | MSA-E-060-PRO 3 MHz |
| ptcFrontEndMSA_E_400_M2 | MSA-E-400-M2, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_400_M2_20 | MSA-E-400-M2-20, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_400_M4 | MSA-E-400-M4, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_400_VDD | MSA-E-400-VDD, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_4_M4 | MSA-E-401-4-M4, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_M2 | MSA-E-401-M2, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_M2_20 | MSA-E-401-M2-20, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_M4 | MSA-E-401-M4, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_VDD | MSA-E-401-VDD, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_500_4_M4 | MSA-E-500-4-M4 |
| ptcFrontEndMSA_E_500_M2 | MSA-E-500-M2 |
| ptcFrontEndMSA_E_500_M2_20 | MSA-E-500-M2-20 |
| ptcFrontEndMSA_E_500_M4 | MSA-E-500-M4 |
| ptcFrontEndMSA_E_500_VDD | MSA-E-500-VDD |
| ptcFrontEndMSA_F_100_1D | MSA-F-100-1D |
| ptcFrontEndMSA_F_100_1D_M | MSA-F-100-1D-M |
| ptcFrontEndMSA_F_100_1D_V | MSA-F-100-1D-V |
| ptcFrontEndMSA_F_100_3D | MSA-F-100-3D |
| ptcFrontEndMSA_F_100_3D_1D | MSA-F-100-3D (1D) |
| ptcFrontEndMSA_F_100_3D_1D_M | MSA-F-100-3D (1D)-M |
| ptcFrontEndMSA_F_100_3D_1D_V | MSA-F-100-3D (1D)-V |
| ptcFrontEndMSA_F_100_3D_M | MSA-F-100-3D-M |
| ptcFrontEndMSA_F_100_3D_V | MSA-F-100-3D-V |
| ptcFrontEndMSA_F_600_M | MSA-F-600-M |
| ptcFrontEndMSA_F_600_V | MSA-F-600-V |
| ptcFrontEndMSA_F_620 | MSA-F-620 |
| ptcFrontEndMSA_F_630 | MSA-F-630 |
| ptcFrontEndMSA_F_650_M | MSA-F-650-M |
| ptcFrontEndMSA_F_650_V | MSA-F-650-V |
| ptcFrontEndMSV_Z_040 | MSV-Z-040, ID not used anymore |
| ptcFrontEndNone | No front-end. |
| ptcFrontEndPSV_E_400_1D | PSV-E-400-1D |
| ptcFrontEndPSV_E_400_1D_M2_20 | PSV-E-400-1D-M2-20 |
| ptcFrontEndPSV_E_400_1D_M4 | PSV-E-400-1D-M4 |
| ptcFrontEndPSV_E_400_3D | PSV-E-400-3D |
| ptcFrontEndPSV_E_400_3D_1D | PSV-E-400-3D (1D) |
| ptcFrontEndPSV_E_400_3D_1D_M4 | PSV-E-400-3D (1D)-M4 |
| ptcFrontEndPSV_E_400_3D_M4 | PSV-E-400-3D-M4 |
| ptcFrontEndPSV_E_400_B | PSV-E-400-B |
| ptcFrontEndPSV_E_400_H4 | PSV-E-400-H4 |
| ptcFrontEndPSV_E_400_M2 | PSV-E-400-M2 |
| ptcFrontEndPSV_E_400_M2_20 | PSV-E-400-M2-20 |
| ptcFrontEndPSV_E_400_M4 | PSV-E-400-M4 |
| ptcFrontEndPSV_E_401_1D | PSV-E-401-1D |
| ptcFrontEndPSV_E_401_1D_M2_20 | PSV-E-401-1D-M2-20 |
| ptcFrontEndPSV_E_401_1D_M4 | PSV-E-401-1D-M4 |
| ptcFrontEndPSV_E_401_2_M4 | PSV-E-401-2-M4 |
| ptcFrontEndPSV_E_401_3D | PSV-E-401-3D |
| ptcFrontEndPSV_E_401_3D_1D | PSV-E-401-3D (1D) |
| ptcFrontEndPSV_E_401_3D_1D_M4 | PSV-E-401-3D (1D)-M4 |
| ptcFrontEndPSV_E_401_3D_M4 | PSV-E-401-3D-M4 |
| ptcFrontEndPSV_E_401_B | PSV-E-401-B |
| ptcFrontEndPSV_E_401_H4 | PSV-E-401-H4 |
| ptcFrontEndPSV_E_401_M2 | PSV-E-401-M2 |
| ptcFrontEndPSV_E_401_M2_20 | PSV-E-401-M2-20 |
| ptcFrontEndPSV_E_401_M4 | PSV-E-401-M4 |
| ptcFrontEndPSV_E_401_VDD | PSV-E-401-VDD |
| ptcFrontEndPSV_F_500 | PSV-F-500 |
| ptcFrontEndPSV_F_500_1D | PSV-F-500-1D |
| ptcFrontEndPSV_F_500_1D_M | PSV-F-500-1D-M |
| ptcFrontEndPSV_F_500_1D_V | PSV-F-500-1D-V |
| ptcFrontEndPSV_F_500_3D | PSV-F-500-3D |
| ptcFrontEndPSV_F_500_3D_1D | PSV-F-500-3D (1D) |
| ptcFrontEndPSV_F_500_3D_1D_M | PSV-F-500-3D (1D)-M |
| ptcFrontEndPSV_F_500_3D_1D_V | PSV-F-500-3D (1D)-V |
| ptcFrontEndPSV_F_500_3D_M | PSV-F-500-3D-M |
| ptcFrontEndPSV_F_500_3D_V | PSV-F-500-3D-V |
| ptcFrontEndPSV_F_500_B | PSV-F-500-B, ID not used anymore |
| ptcFrontEndPSV_F_500_M | PSV-F-500-M |
| ptcFrontEndPSV_F_500_V | PSV-F-500-V |
| ptcFrontEndPSV_F_600 | PSV-F-600 |
| ptcFrontEndPSV_F_600_1D | PSV-F-600-1D |
| ptcFrontEndPSV_F_600_1D_V | PSV-F-600-1D-V |
| ptcFrontEndPSV_F_600_3D | PSV-F-600-3D |
| ptcFrontEndPSV_F_600_3D_1D | PSV-F-600-3D (1D) |
| ptcFrontEndPSV_F_600_3D_1D_V | PSV-F-600-3D (1D)-V |
| ptcFrontEndPSV_F_600_3D_V | PSV-F-500-3D-V |
| ptcFrontEndPSV_F_600_V | PSV-F-600-V |
| ptcFrontEndPSV_F_700 | PSV-F-700 VibroScan front-end |
| ptcFrontEndPSV_F_700_1D | PSV-F-700-1D VibroScan front-end |
| ptcFrontEndPSV_F_700_3D | PSV-F-700-3D VibroScan front-end |
| ptcFrontEndPSV_F_700_3D_1D | PSV-F-700-3D (1D) VibroScan front-end |
| ptcFrontEndPSV_I_730 | PSV-I-730 VibroScan Neo |
| ptcFrontEndPSV_I_780 | PSV-I-780 VibroScan Xtra QTec |
| ptcFrontEndPSV_Z_010 | PSV-Z-010, ID not used anymore |
| ptcFrontEndPSV_Z_040 | PSV-Z-040, ID not used anymore |
| ptcFrontEndPSV_Z_040F | PSV-Z-040F, ID not used anymore |
| ptcFrontEndPSV_Z_040H | PSV-Z-040H, ID not used anymore |
| ptcFrontEndPSV_Z_040U | PSV-Z-040U, ID not used anymore |
| ptcFrontEndPSV_Z_1D_H | PSV-Z-1D-H, ID not used anymore |
| ptcFrontEndPSV_Z_3D_H | PSV-Z-3D-H, ID not used anymore |
| ptcFrontEndTMS_350 | TMS-350 |
| ptcFrontEndUnknown | Unknown front-end. |
| ptcFrontEndVDD_E_600 | VDD-E-600 |
| ptcFrontEndVDD_Z_010 | VDD-Z-010, ID not used anymore |
| ptcFrontEndVDD_Z_011 | VDD-Z-011, ID not used anymore |
| ptcFrontEndVFX | VFX-F-110 |
| ptcFrontEndVFX120 | VFX-F-120 |
| ptcFrontEndVGO200 | VGO-200 |
| ptcFrontEndVGO200_P | VGO-200-P |
| ptcFrontEndVIB_E_220 | VIB-E-220 |
| ptcFrontEndVIB_E_400_1000 | VIB-E-400-1000 |
| ptcFrontEndVIB_E_400_1004 | VIB-E-400-1004 |
| ptcFrontEndVIB_E_400_3D_1004 | VIB-E-400-3D-1004 |
| ptcFrontEndVIB_E_400_3D_84 | VIB-E-400-3D-84 |
| ptcFrontEndVIB_E_400_80 | VIB-E-400-80 |
| ptcFrontEndVIB_E_400_84 | VIB-E-400-84 |
| ptcFrontEndVIB_E_400_VDD | VIB-E-400-VDD |
| ptcFrontEndVIB_Z_010 | VIB-Z-010, ID not used anymore |
| ptcFrontEndVIB_Z_012 | VIB-Z-012, ID not used anymore |
| ptcFrontEndVIB_Z_014 | VIB-Z-014, ID not used anymore |
| ptcFrontEndVIB_Z_015 | VIB-Z-015, ID not used anymore |
| ptcFrontEndVIB_Z_016 | VIB-Z-016, ID not used anymore |
| ptcFrontEndVIB_Z_017 | VIB-Z-017, ID not used anymore |
| ptcFrontEndVIO130 | VIO-130 |
The type of the front-end.

### Remarks

This method can be used to retrieve a front-end object that can be queried for capabilities and properties without having the hardware available.

### Example


---

## GetIOFrontEndFirmwareInfo Method

*Quelle: `PolyFrontEndLib~FrontEnds~GetIOFrontEndFirmwareInfo.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : GetIOFrontEndFirmwareInfo Method*

### Description

Returns the information needed to update the firmware of the front-end. The selected front-end identifier comes from FindIOFrontEnds.

### Syntax

*Visual Basic:*
```
Public Function GetIOFrontEndFirmwareInfo( _
   ByVal selectedFrontEndIdentifier As String _
) As String()
```

### Parameters

selectedFrontEndIdentifier

The selected front-end identifier.

### Return Type

The information needed to update the firmware.


---

## AcqBoard Property

*Quelle: `PolyFrontEndLib~FrontEnds~AcqBoard.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : AcqBoard Property*

### Description

The acquisition board type of the front-end.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AcqBoard As PTCAcqBoardType
```


---

## AcqBoardName Property

*Quelle: `PolyFrontEndLib~FrontEnds~AcqBoardName.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : AcqBoardName Property*

### Description

The name of the acquisition board of the front-end.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AcqBoardName As String
```


---

## Connected Property

*Quelle: `PolyFrontEndLib~FrontEnds~Connected.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : Connected Property*

### Description

True, if the junction box is connected.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Connected As Boolean
```


---

## Count Property

*Quelle: `PolyFrontEndLib~FrontEnds~Count.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : Count Property*

### Description

The number of available front-end types.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `PolyFrontEndLib~FrontEnds~Exists.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : Exists Property*

### Description

Returns true, if the item with the given index or name exists.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal Index As Variant _
) As Boolean
```

### Parameters

Index

The index or name of the item.


---

## Item Property

*Quelle: `PolyFrontEndLib~FrontEnds~Item.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : Item Property*

### Description

Returns an item of the FrontEnds collection with the given index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As FrontEnd
```

### Parameters

Index

The index or name of the item.


---

## ProgramID Property

*Quelle: `PolyFrontEndLib~FrontEnds~ProgramID.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : ProgramID Property*

### Description

Specifies which application is using the front-end.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ProgramID As PTCProgramID
```


---

## Type Property

*Quelle: `PolyFrontEndLib~FrontEnds~Type.html` · Polytec PolyFrontEnd Type Library · FrontEnds Collection : Type Property*

### Description

Returns an item of the collection with the given type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type( _
   ByVal eType As PTCFrontEndType _
) As FrontEnd
```

### Parameters

eType

| Value | Description |
|---|---|
| ptcFrontEnd_LeCroyWP725Zi | LeCroyWP7xZi |
| ptcFrontEnd_LeCroyWP725Zi_A | LeCroyWP7xZi-A |
| ptcFrontEnd_LeCroyWR204Xi | LeCroyWR204Xi, ID not used anymore |
| ptcFrontEnd_LeCroyWR8254M | LeCroyWR8254M |
| ptcFrontEnd_M4i4450 | M4i4450 |
| ptcFrontEnd_PCI4461 | PCI-4461 |
| ptcFrontEnd_PCI4462 | PCI-4462 |
| ptcFrontEnd_VibSoft_M2_40 | VibSoft-M2-40 |
| ptcFrontEnd_VibSoft_M4_25 | VibSoft-M4-25 |
| ptcFrontEnd_VibSoft_M8_25 | VibSoft-M8-25 |
| ptcFrontEnd_VibSoft_PRO | VibSoft-PRO |
| ptcFrontEnd_VibSoft_PRO_05 | VibSoft-PRO 500 kHz |
| ptcFrontEnd_VibSoft_PRO_05_3D | VibSoft-PRO-3D 500 kHz |
| ptcFrontEnd_VibSoft_PRO_05_3D_1D | VibSoft-PRO-3D (1D) 500 kHz |
| ptcFrontEnd_VibSoft_PRO_24 | VibSoft-PRO 24 MHz |
| ptcFrontEnd_VibSoft_PRO_24_3D | VibSoft-PRO-3D 24 MHz |
| ptcFrontEnd_VibSoft_PRO_24_3D_1D | VibSoft-PRO-3D (1D) 24 MHz |
| ptcFrontEnd_VibSoft_PRO_3 | VibSoft-PRO 3 MHz |
| ptcFrontEnd_VibSoft_PRO_3_3D | VibSoft-PRO-3D 3 MHz |
| ptcFrontEnd_VibSoft_PRO_3_3D_1D | VibSoft-PRO-3D (1D) 3 MHz |
| ptcFrontEnd_VibSoft_PRO_3D | VibSoft-PRO-3D |
| ptcFrontEnd_VibSoft_PRO_3D_1D | VibSoft-PRO-3D (1D) |
| ptcFrontEndBNC2140 | BNC 2140, ID not used anymore |
| ptcFrontEndIVS500 | IVS-500 |
| ptcFrontEndMPV_E_800 | MPV-E-800 |
| ptcFrontEndMSA_E_050_1000 | MSA-E-050-1000 |
| ptcFrontEndMSA_E_050_1004 | MSA-E-050-1004 |
| ptcFrontEndMSA_E_050_1D_1004 | MSA-E-050-1D-1004, ID not used anymore |
| ptcFrontEndMSA_E_050_1D_84 | MSA-E-050-1D-84, ID not used anymore |
| ptcFrontEndMSA_E_050_3D_1004 | MSA-E-050-3D-1004, ID not used anymore |
| ptcFrontEndMSA_E_050_3D_1D_1004 | MSA-E-050-3D-1D-1004, ID not used anymore |
| ptcFrontEndMSA_E_050_3D_1D_84 | MSA-E-050-3D-1D-84, ID not used anymore |
| ptcFrontEndMSA_E_050_3D_84 | MSA-E-050-3D-84, ID not used anymore |
| ptcFrontEndMSA_E_050_80 | MSA-E-050-80 |
| ptcFrontEndMSA_E_050_84 | MSA-E-050-84 |
| ptcFrontEndMSA_E_050_M2_20 | MSA-E-050-M2-20 |
| ptcFrontEndMSA_E_060_PRO | MSA-E-060-PRO |
| ptcFrontEndMSA_E_060_PRO_05 | MSA-E-060-PRO 500 kHz |
| ptcFrontEndMSA_E_060_PRO_24 | MSA-E-060-PRO 24 MHz |
| ptcFrontEndMSA_E_060_PRO_3 | MSA-E-060-PRO 3 MHz |
| ptcFrontEndMSA_E_400_M2 | MSA-E-400-M2, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_400_M2_20 | MSA-E-400-M2-20, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_400_M4 | MSA-E-400-M4, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_400_VDD | MSA-E-400-VDD, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_4_M4 | MSA-E-401-4-M4, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_M2 | MSA-E-401-M2, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_M2_20 | MSA-E-401-M2-20, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_M4 | MSA-E-401-M4, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_401_VDD | MSA-E-401-VDD, ID not used for PSV and VibSoft |
| ptcFrontEndMSA_E_500_4_M4 | MSA-E-500-4-M4 |
| ptcFrontEndMSA_E_500_M2 | MSA-E-500-M2 |
| ptcFrontEndMSA_E_500_M2_20 | MSA-E-500-M2-20 |
| ptcFrontEndMSA_E_500_M4 | MSA-E-500-M4 |
| ptcFrontEndMSA_E_500_VDD | MSA-E-500-VDD |
| ptcFrontEndMSA_F_100_1D | MSA-F-100-1D |
| ptcFrontEndMSA_F_100_1D_M | MSA-F-100-1D-M |
| ptcFrontEndMSA_F_100_1D_V | MSA-F-100-1D-V |
| ptcFrontEndMSA_F_100_3D | MSA-F-100-3D |
| ptcFrontEndMSA_F_100_3D_1D | MSA-F-100-3D (1D) |
| ptcFrontEndMSA_F_100_3D_1D_M | MSA-F-100-3D (1D)-M |
| ptcFrontEndMSA_F_100_3D_1D_V | MSA-F-100-3D (1D)-V |
| ptcFrontEndMSA_F_100_3D_M | MSA-F-100-3D-M |
| ptcFrontEndMSA_F_100_3D_V | MSA-F-100-3D-V |
| ptcFrontEndMSA_F_600_M | MSA-F-600-M |
| ptcFrontEndMSA_F_600_V | MSA-F-600-V |
| ptcFrontEndMSA_F_620 | MSA-F-620 |
| ptcFrontEndMSA_F_630 | MSA-F-630 |
| ptcFrontEndMSA_F_650_M | MSA-F-650-M |
| ptcFrontEndMSA_F_650_V | MSA-F-650-V |
| ptcFrontEndMSV_Z_040 | MSV-Z-040, ID not used anymore |
| ptcFrontEndNone | No front-end. |
| ptcFrontEndPSV_E_400_1D | PSV-E-400-1D |
| ptcFrontEndPSV_E_400_1D_M2_20 | PSV-E-400-1D-M2-20 |
| ptcFrontEndPSV_E_400_1D_M4 | PSV-E-400-1D-M4 |
| ptcFrontEndPSV_E_400_3D | PSV-E-400-3D |
| ptcFrontEndPSV_E_400_3D_1D | PSV-E-400-3D (1D) |
| ptcFrontEndPSV_E_400_3D_1D_M4 | PSV-E-400-3D (1D)-M4 |
| ptcFrontEndPSV_E_400_3D_M4 | PSV-E-400-3D-M4 |
| ptcFrontEndPSV_E_400_B | PSV-E-400-B |
| ptcFrontEndPSV_E_400_H4 | PSV-E-400-H4 |
| ptcFrontEndPSV_E_400_M2 | PSV-E-400-M2 |
| ptcFrontEndPSV_E_400_M2_20 | PSV-E-400-M2-20 |
| ptcFrontEndPSV_E_400_M4 | PSV-E-400-M4 |
| ptcFrontEndPSV_E_401_1D | PSV-E-401-1D |
| ptcFrontEndPSV_E_401_1D_M2_20 | PSV-E-401-1D-M2-20 |
| ptcFrontEndPSV_E_401_1D_M4 | PSV-E-401-1D-M4 |
| ptcFrontEndPSV_E_401_2_M4 | PSV-E-401-2-M4 |
| ptcFrontEndPSV_E_401_3D | PSV-E-401-3D |
| ptcFrontEndPSV_E_401_3D_1D | PSV-E-401-3D (1D) |
| ptcFrontEndPSV_E_401_3D_1D_M4 | PSV-E-401-3D (1D)-M4 |
| ptcFrontEndPSV_E_401_3D_M4 | PSV-E-401-3D-M4 |
| ptcFrontEndPSV_E_401_B | PSV-E-401-B |
| ptcFrontEndPSV_E_401_H4 | PSV-E-401-H4 |
| ptcFrontEndPSV_E_401_M2 | PSV-E-401-M2 |
| ptcFrontEndPSV_E_401_M2_20 | PSV-E-401-M2-20 |
| ptcFrontEndPSV_E_401_M4 | PSV-E-401-M4 |
| ptcFrontEndPSV_E_401_VDD | PSV-E-401-VDD |
| ptcFrontEndPSV_F_500 | PSV-F-500 |
| ptcFrontEndPSV_F_500_1D | PSV-F-500-1D |
| ptcFrontEndPSV_F_500_1D_M | PSV-F-500-1D-M |
| ptcFrontEndPSV_F_500_1D_V | PSV-F-500-1D-V |
| ptcFrontEndPSV_F_500_3D | PSV-F-500-3D |
| ptcFrontEndPSV_F_500_3D_1D | PSV-F-500-3D (1D) |
| ptcFrontEndPSV_F_500_3D_1D_M | PSV-F-500-3D (1D)-M |
| ptcFrontEndPSV_F_500_3D_1D_V | PSV-F-500-3D (1D)-V |
| ptcFrontEndPSV_F_500_3D_M | PSV-F-500-3D-M |
| ptcFrontEndPSV_F_500_3D_V | PSV-F-500-3D-V |
| ptcFrontEndPSV_F_500_B | PSV-F-500-B, ID not used anymore |
| ptcFrontEndPSV_F_500_M | PSV-F-500-M |
| ptcFrontEndPSV_F_500_V | PSV-F-500-V |
| ptcFrontEndPSV_F_600 | PSV-F-600 |
| ptcFrontEndPSV_F_600_1D | PSV-F-600-1D |
| ptcFrontEndPSV_F_600_1D_V | PSV-F-600-1D-V |
| ptcFrontEndPSV_F_600_3D | PSV-F-600-3D |
| ptcFrontEndPSV_F_600_3D_1D | PSV-F-600-3D (1D) |
| ptcFrontEndPSV_F_600_3D_1D_V | PSV-F-600-3D (1D)-V |
| ptcFrontEndPSV_F_600_3D_V | PSV-F-500-3D-V |
| ptcFrontEndPSV_F_600_V | PSV-F-600-V |
| ptcFrontEndPSV_F_700 | PSV-F-700 VibroScan front-end |
| ptcFrontEndPSV_F_700_1D | PSV-F-700-1D VibroScan front-end |
| ptcFrontEndPSV_F_700_3D | PSV-F-700-3D VibroScan front-end |
| ptcFrontEndPSV_F_700_3D_1D | PSV-F-700-3D (1D) VibroScan front-end |
| ptcFrontEndPSV_I_730 | PSV-I-730 VibroScan Neo |
| ptcFrontEndPSV_I_780 | PSV-I-780 VibroScan Xtra QTec |
| ptcFrontEndPSV_Z_010 | PSV-Z-010, ID not used anymore |
| ptcFrontEndPSV_Z_040 | PSV-Z-040, ID not used anymore |
| ptcFrontEndPSV_Z_040F | PSV-Z-040F, ID not used anymore |
| ptcFrontEndPSV_Z_040H | PSV-Z-040H, ID not used anymore |
| ptcFrontEndPSV_Z_040U | PSV-Z-040U, ID not used anymore |
| ptcFrontEndPSV_Z_1D_H | PSV-Z-1D-H, ID not used anymore |
| ptcFrontEndPSV_Z_3D_H | PSV-Z-3D-H, ID not used anymore |
| ptcFrontEndTMS_350 | TMS-350 |
| ptcFrontEndUnknown | Unknown front-end. |
| ptcFrontEndVDD_E_600 | VDD-E-600 |
| ptcFrontEndVDD_Z_010 | VDD-Z-010, ID not used anymore |
| ptcFrontEndVDD_Z_011 | VDD-Z-011, ID not used anymore |
| ptcFrontEndVFX | VFX-F-110 |
| ptcFrontEndVFX120 | VFX-F-120 |
| ptcFrontEndVGO200 | VGO-200 |
| ptcFrontEndVGO200_P | VGO-200-P |
| ptcFrontEndVIB_E_220 | VIB-E-220 |
| ptcFrontEndVIB_E_400_1000 | VIB-E-400-1000 |
| ptcFrontEndVIB_E_400_1004 | VIB-E-400-1004 |
| ptcFrontEndVIB_E_400_3D_1004 | VIB-E-400-3D-1004 |
| ptcFrontEndVIB_E_400_3D_84 | VIB-E-400-3D-84 |
| ptcFrontEndVIB_E_400_80 | VIB-E-400-80 |
| ptcFrontEndVIB_E_400_84 | VIB-E-400-84 |
| ptcFrontEndVIB_E_400_VDD | VIB-E-400-VDD |
| ptcFrontEndVIB_Z_010 | VIB-Z-010, ID not used anymore |
| ptcFrontEndVIB_Z_012 | VIB-Z-012, ID not used anymore |
| ptcFrontEndVIB_Z_014 | VIB-Z-014, ID not used anymore |
| ptcFrontEndVIB_Z_015 | VIB-Z-015, ID not used anymore |
| ptcFrontEndVIB_Z_016 | VIB-Z-016, ID not used anymore |
| ptcFrontEndVIB_Z_017 | VIB-Z-017, ID not used anymore |
| ptcFrontEndVIO130 | VIO-130 |
The type of the front-end.
