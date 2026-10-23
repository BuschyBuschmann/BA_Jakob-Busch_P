# _Konzept – Access to General Information

## Access to General Information

*Quelle: `Access to General Information.html` · Basic Engine Manual · The PSV/VibSoft Object Model > Access to General Information*

#### Access to General Information in PSV/VibSoft

PSV/VibSoft have properties to access general information about the hardware, the defined alignments, the attached scanning heads and vibrometer controllers.

Every item of the InfosAcq collection is also available via a property of the collection. You can check the properties starting with "Has" to find out whether the corresponding item exists in the collection.PolyFile has properties to access general file information, the acquisition settings, and the measurement data. Depending on the file type (measurement or settings) or the system type not all of these properties might be available. For details see the reference section.

PSV has to be in acquisition mode to provide access to the Acquisition object.

The property Infos of the Acquisition object returns the InfosAcq collection of objects that are derived from Info. All these objects share the properties of the Info object and have additional properties and methods. The number of items in the InfosAcq collection varies depending on the type of the system, so does the type of Info you get at index 1, 2, or 3 of the collection. To learn more about how to get the type of Info you want, see the following section Using Collections.

#### To access the attached front end do the following:

*Access to the attached front end:*
```
 Dim oInfosAcq As InfosAcq
 Set oInfosAcq = Acquisition.Infos
 Debug.Print oInfosAcq.Hardware.ActiveFrontEnd.Name
```

#### To access the attached scanning head do the following:

*Access to the attached scanning head:*
```
 Dim oInfosAcq As InfosAcq
 Set oInfosAcq = Acquisition.Infos
 If (oInfosAcq.HasScanHeadDevicesInfo) Then
  Dim oScanHeadDevicesInfo As ScanHeadDevicesInfo
  Set oScanHeadDevicesInfo = oInfosAcq.ScanHeadDevicesInfo
  Dim oScanHeadDevice As ScanHeadDevice
  Set oScanHeadDevice = oScanHeadDevicesInfo.ScanHeadDevices(1)
  Debug.Print oScanHeadDevice.SensorHeadName
 End If
```

This does not work for VibSoft, as there is no scanning head attached to VibSoft systems.

#### To access the geometry defined in the PSV acquisition mode do the following:

*Access to the geometry defined in the PSV acquisition mode:*
```
 Dim oInfosAcq As InfosAcq
 Set oInfosAcq = Acquisition.Infos
 If (oInfosAcq.HasElements) Then
  Debug.Print oInfosAcq.Elements.Count
 End If
 If (oInfosAcq.HasMeasPoints) Then
  Debug.Print oInfosAcq.MeasPoints.Count
 End If
```

#### To access the current signal level of a Vibrometer in PSV acquisition mode do the following:

PSV/VibSoft support up to two groups of Vibrometer controllers attached to the system. For a 3D system the first group contains three Vibrometers. Below the signal level of the first sensor head of the first controller of the first Vibrometer group is printed. Please note that the Vibrometers collection uses 1-based indices, the Controllers and SensorHeads collections use 0-based indices.

*Access to the current signal level of a Vibrometer in the PSV acquisition mode:*
```
 Dim oInfosAcq As InfosAcq
 oInfosAcq = Acquisition.Infos
 Debug.Print oInfosAcq.Vibrometers(1).Controllers(0).SensorHeads(0).SignalLevel
```

#### Access to General Information in Files

The properties SummaryInfo and Version give access to general file information like the author, project and comments, the file type, file version, and the program version.

The property Infos returns a collection of objects that are derived from Info. All these objects share the properties of the Info object and have additional properties and methods. The number of items in the Infos collection varies from file to file and depending on the file type, so does the type of Info you get at index 1, 2, or 3 of the collection. To learn more about how to get the type of Info you want, see the following section Using Collections.

Every item of the Infos collection is also available via a property of the collection. You can check the properties starting with "Has" to find out whether the corresponding item exists in the collection.

See the following examples how to access different types of information:

#### To access the type of acquisition board do the following:

*Access the type of acquisition board:*
```
 Dim acqBoard As PTCAcqBoardType
 If (oFile.Infos.HasHardware) Then
  Dim oHardware As Hardware
  Set oHardware = oFile.Infos.Hardware
  acqBoard = oHardware.AcqBoard
 End If
```

#### To access the number of measurement points:

This does not work with VibSoft measurement files, as there are no measurement points in VibSoft.

*Access number of measurement points:*
```
 Dim lPoints As Long
 If (oFile.Infos.HasMeasPoints) Then
  Dim oMeasPoints As MeasPoints
  Set oMeasPoints = oFile.Infos.MeasPoints
  lPoints = oMeasPoints.Count
 End If
```

#### To access the number of FFT lines used in an FFT mode measurement file:

This does not work for measurement files not taken in the FFT mode. The FFTAcqProperties object might not exist for all measurement modes (e.g. Time).

*Access number of FFT lines:*
```
 Dim lLines As Long
 If (oFile.Infos.HasAcquisitionInfoModes) Then
  Dim oAcqModes As AcquisitionInfoModes
  Set oAcqModes = oFile.Infos.AcquisitionInfoModes
  If (oAcqModes.ActiveProperties.HasFftProperties) Then
   Dim oFFTProps As FftAcqPropertiesContainer
   Set oFFTProps = oAcqModes.ActiveProperties.FftProperties
   lLines = oFFTProps.Lines
  End If
 End If
```

#### To access the laser wavelength of the Vibrometer that was used for the measurement:

*Access laser wavelength of the Vibrometer:*
```
  Dim oVibrometerAcqProperties As VibrometerAcqProperties
  oVibrometerAcqProperties = oFile.Infos.AcquisitionInfoModes.ActiveProperties.VibrometersProperties(1)
  Debug.Print oVibrometerAcqProperties.VibControllerSettings.SensorHeadSettingsCollection(0).SensorHeadInfo.LaserWavelength
```
