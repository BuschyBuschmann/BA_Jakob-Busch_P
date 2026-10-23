# _Konzept – Access to Data

## Access to Data

*Quelle: `Access to Data.html` · Object Model Reference*

Before you access the data stored in MPV, PSV, and VibSoft measurement files you have to decide what kind of data you want to retrieve. You have access to point data (data taken at the scan points of a PSV scan or at the single measurement point of MPV and VibSoft), point average data (the average over all valid measurement points, available in PSV only) and band data (frequency bands combining the data of all measurement points within a given frequency band, available in MPV and PSV only).

In any case you have to choose a domain ("Time", "FFT", "1/3 Octave", etc.), a channel ("Vib", "Ref1", "Vib & Ref1", "A1" ,"R1", "A1 & R1"), a signal ("Velocity", "Displacement", "FRF Velocity/Voltage", etc.) and a display ("Magnitude", "Real", "Imaginary", etc.). To learn more about how to choose the appropriate domain, channel, signal, and display see chapter 6 ("Displaying Data") of your VibSoft Software Manual or chapter 7 of your MPV/PSV Software Manual, respectively.

By selecting a domain and a specific measurement point or a frequency band you can navigate to a DataPoint, PointAverageDomain or DataBand object. These objects provide a GetData method to retrieve the data. The first parameter of GetData is of type Display. With this object you specify what kind of data you want to get, i.e. you specify the channel, signal, and display. The second parameter of GetData denotes the frame number. If you have a measurement file taken in MultiFrame mode (PSV only, optional) or you have user-defined data, you can specify the frame. In all other cases this parameter should be set to zero. GetData returns an array of Single (32 bit float values) representing the data.

The retrieved array depends on the display you have chosen. In the time mode you will get the samples of the last average of the measurement. The data array starts at index 0 and ends at index number of samples  1. In the FFT mode you will get the averaged FFT data starting at line 1 (index 0) up to the number of lines (index number of lines  1). If you have selected a display that provides two kinds of data at the same time (like Real & Imaginary or Magnitude & Phase) the data is stored interlaced in the same array. Even indices reference the first part of the data (Real or Magnitude), odd indices the second part (Imaginary or Phase).

When you retrieve data of a 3D channel (the channel has the caps flag ptcChannelCapsVector set, see Caps Property), the returned array first contains the data for the x-direction, then the data for the y-direction, and finally the data for the z-direction.

#### Access to Point Data

To access point data you use the GetPointDomains method of PolyFile to get a named and typed collection of the available domains. Select a PointDomain from this collection. Via the Channels, Signals, and Displays collections you can select a Display object that represents the kind of data you want to retrieve. The DataPoints property of PointDomain returns a standard collection containing all available measurement points. Select a DataPoint and use its GetData method to retrieve the data. Use the Display object as the first parameter to GetData.

*Access to point data:*
```

' select a PointDomain
Dim oPointDomains As PointDomains
Set oPointDomains = oFile.GetPointDomains()
Dim oPointDomain As PointDomain
Set oPointDomain = oPointDomains("FFT")
' use base class Domain to access channels
Dim oDomain As Domain
Set oDomain = oPointDomain
' select a Display
Dim oDisplay As Display
Set oDisplay = _
oDomain.Channels("Vib").Signals("Velocity").Displays("Real")
' select a measurement point
Dim oDataPoint As DataPoint
Set oDataPoint = oPointDomain.DataPoints(1)
' now get the data
Dim Data() As Single
Data = oDataPoint.GetData(oDisplay, 0)
```

#### Access to Multipoint Data

Measurement files created by the MPV software (*.mvd) contain a single DataPoint which holds the raw data (i.e. the data not transformed to the coordinate system of the scan points). The channels of the multipoint data are named A1, A2, A3, ... F8 for the Vibrometer channels and R1 - R8 for the reference channels, respectively. To display the data on the geometry, the MPV software transforms the raw data to the coordinate system of the scan points. To do this, there has to be a relation between the measurement channels and the scan points. Moreover, the measurement directions V of the sensors and the normal vectors N at the measurement locations are used. For details please see chapter 4 ("Defining Measurement Locations") of your MPV software manual.

To access data for a given scan point you have to inspect the MeasurementLocations collection, which is accessible through the Infos collection. Then find the corresponding MeasurementLocation objects and by means of these the channel names. Then proceed as described in the previous section to access the point data. To transform the data to the coordinate system of the scan points you have to implement the methods and formulas provided in chapter 4 ("Defining Measurement Locations") of your MPV software manual.

*Access to multipoint data:*
```

' get the measurement locations
Dim oLocations As MeasurementLocations
Set oLocations = oFile.Infos.MeasurementLocations
' get the locations related to the scan point with the specified index
' for a 3D measurement, the returned array has 3 entries, otherwise the array
' has a single entry
Dim oLocationsOfMeasPoint() As Object
oLocationsOfMeasPoint = oLocations.GetMeasurementLocationsByMeasPointIndex(1)
Dim oLocation As MeasurementLocation
Set oLocation = oLocationsOfMeasPoint(0)
Dim channelName As String
channelName = oLocation.ChannelName
' from here on you can use the channel name to retrieve the raw data of this channel
```

#### Access to Point Average Data

Point average data is the average over all valid measurement points. It is available in PSV scan files only. To access the point average data select a PointAverageDomain from the PointAverageDomains named and typed collection of PolyFile. Select a Display object via Channels, Signals, and Displays collection. Use the GetData method of the PointAverageDomain to retrieve the data. Use the Display object as the first parameter to GetData.

*Access to point average data:*
```

' select a domain
Dim oPointAverageDomains As PointAverageDomains
Set oPointAverageDomains = oFile.GetPointAverageDomains()
Dim oPointAverageDomain As PointAverageDomain
Set oPointAverageDomain = oPointAverageDomains("FFT")
' use base class Domain to access channels
Dim oDomain As Domain
Set oDomain = oPointAverageDomain
' select a display
Dim oDisplay As Display
Set oDisplay = _
oDomain.Channels("Vib").Signals("Velocity").Displays("Magnitude")
' now get the data
Dim Data() As Single
Data = oPointAverageDomain.GetData(oDisplay, 0)
```

#### Access to Band Data

Band data are frequency bands over all measurement points. They are available in PSV scan files or MPV data files with defined bands only. To access the band data select a BandDomain from the BandDomains named and typed collection of PolyFile. Select a Display object via Channels, Signals, and Displays collection. Select a DataBand from the DataBands named collection. You can either use the band number starting at 1 as index or you can use a string "1", "2", "3" to select the band. In the "RMS" domain there is an additional band (last band of the collection) with the name "Entire Bandwidth" covering the whole bandwidth of the measurement. Use the GetData method of the DataBand to retrieve the data. Use the Display object as the first parameter to GetData.

*Access to band data:*
```

' select a domain
Dim oBandDomains As BandDomains
Set oBandDomains = oFile.GetBandDomains()
Dim oBandDomain As BandDomain
Set oBandDomain = oBandDomains("RMS")
' use base class Domain to access channels
Dim oDomain As Domain
Set oDomain = oBandDomain
' select a display
Dim oDisplay As Display
Set oDisplay = _
oDomain.Channels("Vib").Signals("Velocity").Displays("Magnitude")
' get the data bands
Dim oDataBands As DataBands
Set oDataBands = oBandDomain.GetDataBands(oDisplay.Signal)
' select a band
Dim oDataBand As DataBand
Set oDataBand = oDataBands("Entire Bandwidth")
' now get the data
Dim Data() As Single
Data = oDataBand.GetData(oDisplay, 0)
```

 The array now holds the data for every measurement point. Data(0) is the data of measurement point 1, Data(1) of point 2, etc.

#### Access to Instantaneous Values

The instantaneous value of complex data is the magnitude of the data at a given phase. To retrieve instantaneous values you have to select a display of type ptcDisplayInstVal or with name "Inst. Val.". The Display object you get is then of type DisplayInstVal, which is derived from Display. To give the phase (in degree) do the following:

*Access to instantaneous values:*
```

' select a domain
Dim oBandDomains As BandDomains
Set oBandDomains = _
   oFile.GetBandDomains(ptcBuildBandData3d Or ptcBuildDisplayInstVal)
Dim oBandDomain As BandDomain
Set oBandDomain = oBandDomains("FFT")
' use base class Domain to access channels
Dim oDomain As Domain
Set oDomain = oBandDomain
' select a display
Dim oDisplayInstVal As DisplayInstVal
Set oDisplayInstVal = _
    oDomain.Channels("Vib").Signals("Velocity").Displays("Inst. Val.")
oDisplayInstVal.Phase = 45
' get the data bands
Dim oDataBands As DataBands
Set oDataBands = oBandDomain.GetDataBands(oDisplayInstVal.Signal)
' select a band
Dim oDataBand As DataBand
Set oDataBand = oDataBands(1)
' retrieve instantaneous values
Dim Data() As Single
Data = oDataBand.GetData(oDisplayInstVal, 0)
```

#### Access to User Signals

User Signals enable you to add custom-defined signals and data to your acquired signals. You can add user signals only to the "Usr" channels in the "Time" and "FFT" domains. User-defined bands can only be added to the "FFT" domain. Follow the steps described below to add a User Signal.

- Create a SignalDescription Object and set the Name Property to give it a name.

 Dim oSignalDesc As SignalDescription
 Set oSignalDesc = New SignalDescription
 oSignalDesc.Name = "UserSignal"

- Set the DomainType Property, DataType Property, FunctionType Property.

- Create the DegreeOfFreedomIDs Object of the responses

 oSignalDesc.ResponseDOFs.Assign(-1, ptcPlusZTranslation, "Usr", "Velocity", "m/s")

- If you want to add 3D signal, create the response DOFs of the signal

 oSignalDesc.ResponseDOFs.Assign(-1, ptcVector, "Usr", "Velocity", "m/s")

- Set other properties of the signal description object, if necessary.

- If your signal is similar to an original signal, you can also retrieve the description of the original signal (see Description Property) and modify it, if necessary.

-
 Retrieve PointDomains, PointAverageDomains or BandDomains with GetPointDomains, GetPointAverageDomains or GetBandDomains. Please see the remarks section of the method description for the build flags to pass to these methods. Call the AddSignal Method, the AddSignal Method or the AddBand Method. You will get a Signal Object or a DataBand Object as return value. See the add methods for more examples for adding user-defined signals.

*Access to a user signal:*
```

Dim oSignalDesc As SignalDescription
Set oSignalDesc = New SignalDescription
oSignalDesc.Name = "UserSignal"
oSignalDesc.DomainType = ptcDomainSpectrum
oSignalDesc.DataType = ptcDataPoint
oSignalDesc.FunctionType = ptcFunctionSpectrumType
oSignalDesc.ResponseDOFs.Assign(-1, ptcPlusZTranslation, "Usr", "Velocity", "m/s")
oSignalDesc.XAxis.MaxCount = 100
oSignalDesc.XAxis.Min = 1.0
oSignalDesc.XAxis.Max = 100.0
oSignalDesc.XAxis.Name = "Frequency"
oSignalDesc.XAxis.Unit = "Hz"
oSignalDesc.YAxis.Name = "Velocity"
oSignalDesc.YAxis.Unit = "m/s"
Dim oPointDomains As PointDomains
Set oPointDomains = _
oFile.GetPointDomains(ptcBuildPointData3d)
Dim oSignal As Signal
Set oSignal = oPointDomains.AddSignal(oSignalDesc)
```

 To remove a user signal call the Remove Method of the Signals Collection with the name or Index of the signal as the only parameter.

*Removal of a user signal:*
```

Set oSignal = oPointDomains.FindSignal(oSignalDesc, True)
If (Not oSignal Is Nothing) Then
 oSignal.Channel.Signals.Remove(oSignal.Name)
End If
```

#### Access to User-Defined Data

You can retrieve a user-defined dataset in the same way as a normal dataset. The frame number must be between 1 and 12. Each dataset has its own frame count. If there is no data for a requested frame you will retrieve a zero length array and no error will be raised.

*Access to user-defined data:*
```

' select a PointDomain
Dim oPointDomain As PointDomain
Set oPointDomain = _
oFile.GetPointDomains(ptcBuildPointData3d)("FFT")
' use base class Domain to access channels
Dim oDomain As Domain
Set oDomain = oPointDomain
' select a Display
Dim oDisplay As Display
Set oDisplay = _
oDomain.Channels("Usr").Signals("UserSignal").Displays("Magnitude")
    ' use Usr 3D channel for 3D user signals
' select a measurement point
Dim oDataPoint As DataPoint
Set oDataPoint = oPointDomain.DataPoints(1)
' now get the data
Dim Data() As Single
Data = oDataPoint.GetData(oDisplay, 1)
```

To add data for this data point, call the SetData method from oDataPoint with the Signal as the first parameter. For a complex signal the length of the data array must be twice the MaxCount property of the XAxis property of the SignalDescription object. The frame number must be between 1 and 12. You will be able to enter data for frame 2 only if you have already entered data for frame 1. You can always change the data for an existing frame with this method. If your signal is 3D, then the array must contain x-, y-, and z-axis data sequentially for each frame; i.e. RX0, RX1, ..., RXn, RY0, RY1, ..., RYn, RZ0, RZ1, ..., RZn and for a complex signal RX0, IX0, RX1, IX1, ..., RXn, IXn, RY0, IY0, RY1, IY1, ..., RYn, IYn, RZ0, IZ0, RZ1, IZ1, ..., RZn, IZn.

*Setting data for a user-defined signal:*
```

' select a PointDomain
Dim oPointDomain As PointDomain
Set oPointDomain = _
 oFile.GetPointDomains(ptcBuildPointData3d)("FFT")
' use base class Domain to access channels
Dim oDomain As Domain
Set oDomain = oPointDomain
' select a user signal
Dim oSignal As Signal
Set oSignal = _
 oDomain.Channels("Usr").Signals("UserSignal")
' select a measurement point
Dim oDataPoint As DataPoint
Set oDataPoint = oPointDomain.DataPoints(1)
' now set the data
Dim Data() As Single
ReDim Data(0 To oSignal.Description.XAxis.MaxCount - 1)
' populate the array with appropriate data length
oDataPoint.SetData(oSignal, 1, Data)
```
