# _Konzept – Using Collections

## Using Collections

*Quelle: `Using Collections.html` · Object Model Reference*

Polytec File Access uses collections as containers for items of the same type or of different types. In total there are four types of collections used in Polytec File Access. Knowing the different types of collections is essential for an efficient access to the data stored in the files.

#### Standard Collections

Standard collections have the properties Item and Count. Item takes an integral value (Long) as an index and returns an item of the collection. Count returns the number of items in the collection. All items have the same type. The index is 1-based i.e. the index of the first item in the collection is 1 and the index of the last item is Count.

Examples: Elements, MeasPoints

To access all elements of the collection do the following:

*Access all elements of the collection:*
```

Dim oElements As Elements
Set oElements = oFile.Infos.Elements
' preferred method via For Each
Dim oElement As Element
For Each oElement In oElements
 ' do something with oElement
Next oElement
' or via index
Dim lElement As Long
For lElement = 1 To oElements.Count
 ' note: in VBA you can leave out the .Item because Item is the
 ' default property of the collection
 Set oElement = oElements(lElement)
 ' do something with oElement
Next lElement
```

#### Typed Collections

Typed collections have the properties Item and Count. Item takes an enumerator value as an index and returns an item of the collection. Count returns the number of items in the collection (including those that do not exist). The items of the collection have different types. Not all Items of the collection might exist. Item returns Nothing when the corresponding item does not exist.

Examples: AcquisitionInfoModes, AcquisitionPropertiesContainer.

To access elements of a typed collection do the following:

*Access elements of a typed collection:*
```

Dim oAcqProps As AcquisitionPropertiesContainer
Set oAcqProps = oFile.Infos.AcquisitionInfoModes.ActiveProperties
Dim oFFTProps As FftAcqPropertiesContainer
Set oFFTProps = oAcqProps(ptcAcqPropertiesTypeFft)
If (Not oFFTProps Is Nothing) Then
 ' do something with oFFTProps
End If
```

#### Named Collections

Named collections have the properties Item, Exists and Count. Count returns the number of items in the collection. Item takes either an integral value (Long) or a String as index and returns an item of the collection. The integral index is 1-based i.e. the index of the first item in the collection is 1 and the index of the last item is Count. Exists takes a String as parameter and returns True if an Item with this name exists in the collection and False if not. All items of the collection have the same type. All items have a property Name that returns the name of the item. This name can be used as an index.

 The strings returned by the Name property of the items are language dependant. On systems with German as user interface language the name for the signal velocity is "Geschwindigkeit". The Item and Exists properties of the signals collection accept "Geschwindigkeit" as well as "Velocity" as index on all systems. Therefore programs using any version of the string will run on all systems without change.

Examples: Channels, Signals, DataBands

To access elements of a named collection do the following:

*Access elements of a named collection:*
```

Dim oDomain As Domain
Set oDomain = oFile.GetPointDomains().Type(ptcDomainSpectrum)
Dim oSignals As Signals
Set oSignals = oDomain.Channels("Vib").Signals
Dim oSignal As Signal
If (oSignals.Exists("Velocity")) Then
 Set oSignal = oSignals("Velocity")
End If
If (oSignals.Exists("Weg")) Then
 Set oSignal = oSignals("Weg")
End If
For Each oSignal In oSignals
 ' do something with oSignal
 If (oSignal Is oSignals(oSignal.Name)) Then
  ' this is always true
 End If
 If (oSignals.Exists(oSignal.Name)) Then
  ' this is always true
 End If
Next oSignal
Dim lSignal As Long
For lSignal = 1 To oSignals.Count
 Set oSignal = oSignals(lSignal)
 ' do something with oSignal
Next lSignal
```

#### Named And Typed Collections

Named and typed collections have the properties Item, Type, Exists and Count. Count returns the number of items in the collection. Item takes either an integral value (Long) or a String as index and returns an item of the collection. Type takes an enumerator value as parameter and returns an item of the collection. Exists takes either an enumerator value or a String as parameter and returns True if the corresponding item exists in the collection or False if not. All items of the collection are of different type but all items are derived from the same type. All items have a property Name that returns the name of the item and a property Type that returns the type (enumerator value) of the item. The name can be used as a parameter for the Item and Exists properties of the collection and the Type can be used as a parameter for the Type and Exists property of the collection.

 The strings returned by the Name property of the items are language dependant. On systems with German as user interface language the name for the domain time is "Zeit". The Item and Exists properties of the PointDomains collection accept "Zeit" as well as "Time" as index on all systems. Therefore programs using any version of the string will run on all systems without change.

Examples: Infos, Displays, PointDomains.

To access items of a named and typed collection do the following:

*Access elements of a named and typed collection:*
```

Dim oInfos As Infos
Set oInfos = oFile.Infos
Dim oHardware As Hardware
' access via string
If (oInfos.Exists("Hardware")) Then
 Set oHardware = oInfos("Hardware")
End If
' access via type
If (oInfos.Exists(ptcInfoHardware)) Then
 Set oHardware = oInfos(ptcInfoHardware)
End If
' access via index
Dim lInfo As Long
For lInfo = 1 To oInfos.Count
 If (oInfos(lInfo).Name = "Hardware") Then
  Set oHardware = oInfos(lInfo)
  Exit For
 End If
Next lInfo
' access via property
' note that this is not supported by all collections
If (oInfos.HasHardware) Then
 Set oHardware = oInfos.Hardware
End If
Dim oInfo As Info
For Each oInfo In oInfos
 If (oInfo Is oInfos(oInfo.Name)) Then
  ' this is always true
 End If
 If (oInfo Is oInfos.type(oInfo.type)) Then
  ' this is always true
 End If
 If (oInfos.Exists(oInfo.Name)) Then
  ' this is always true
 End If
 If (oInfos.Exists(oInfo.type)) Then
  ' this is always true
 End If
Next oInfo
```
