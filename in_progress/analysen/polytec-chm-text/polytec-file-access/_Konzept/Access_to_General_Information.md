# _Konzept – Access to General Information

## Access to General Information

*Quelle: `Access to General Information.html` · Object Model Reference*

PolyFile has properties to access general file information, the acquisition settings, and the measurement data. Depending on the file type (measurement or settings) or the system type not all of these properties might be available. For details see the reference section.

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

 This does not work with VibSoft measurement files as there are no measurement points in VibSoft.

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

PSV/VibSoft support up to two groups of Vibrometer controllers attached to the system. For a 3D system the first group contains three Vibrometers. Below the laser wavelength of the first sensor head of the first controller of the first Vibrometer group is printed. Please note that the VibrometersAcqPropertiesContainer Collection uses 1-based indices, the SensorHeadSettingsCollection Collection uses 0-based indices.

*Access laser wavelength of the Vibrometer:*
```

  Dim oVibrometerAcqProperties As VibrometerAcqProperties
  oVibrometerAcqProperties = oFile.Infos.AcquisitionInfoModes.ActiveProperties.VibrometersProperties(1)
  Debug.Print oVibrometerAcqProperties.VibControllerSettings.SensorHeadSettingsCollection(0).SensorHeadInfo.LaserWavelength
```
