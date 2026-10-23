# _Konzept – Creating New Files

## Creating New Files

*Quelle: `Creating New Files.html` · Object Model Reference*

You can create MPV raw data files, PSV scan files, VibSoft single point files, and settings files for MPV, PSV, and VibSoft that contain a geometry (MPV and PSV files only) and user-defined datasets. These files can be opened by MPV, PSV, and VibSoft, and you can display and analyze the data in the files and load the settings, respectively.

The following macro creates a PSV scan file which contains a disk geometry and sine curves as time traces. You can open this file using MPV or PSV and display the data in the time domain.

See also the Create method of PolyFile for further information.

*Create a new file:*
```

Option Explicit
Const c_dPi As Double = Atn(1.0) * 4.0
Const c_lDiskSectors As Long = 32
Const c_lSamples As Long = 64
Const c_lVibrationNodes As Long = 2
Const c_strFileName As String = "D:\Temp\Disk.svd"
Sub Main
 Dim oFile As New PolyFile
 oFile.ReadOnly = False
 oFile.Create(c_strFileName, ptcCreateAlways)
 oFile.Version.FileID = ptcFileIDPSVFile
 Call CreateMeasPointsAndElements(oFile)
 Call CreateData(oFile)
 oFile.Save()
 oFile.Close()
End Sub
Sub CreateMeasPointsAndElements(oFile As PolyFile)
 Dim x As Double
 Dim y As Double
 Dim oMeasPoints As MeasPoints
 Set oMeasPoints = oFile.Infos.Add(ptcInfoMeasPoints)
 Dim oElements As Elements
 Set oElements = oFile.Infos.Add(ptcInfoElements)
 Dim oMeasPoint As MeasPoint
 Set oMeasPoint = oMeasPoints.Add()
 oMeasPoint.SetCoordXYZ(0.0, 0.0, 0.0)
 oMeasPoint.SetVideoXY(0.0, 0.0)
 Dim i As Integer
 For i = 1 To c_lDiskSectors
  x = Sin(i * 2 * c_dPi / c_lDiskSectors)
  y = Cos(i * 2 * c_dPi / c_lDiskSectors)
  Set oMeasPoint = oMeasPoints.Add()
  oMeasPoint.SetCoordXYZ(x, y, 0.0)
  oMeasPoint.SetVideoXY(x, y)
 Next i
 Dim elementIndices(0 To 2) As Long
 For i = 1 To c_lDiskSectors
  elementIndices(0) = 1
  elementIndices(1) = i + 1
  If (i < c_lDiskSectors) Then
   elementIndices(2) = i + 2
  Else
   elementIndices(2) = 2
  End If
  oElements.Add(elementIndices, False)
 Next i
End Sub
Sub CreateData(oFile As PolyFile)
 Dim oUSD As New SignalDescription
 oUSD.Name = "Sine"
 oUSD.DataType = ptcDataPoint
 oUSD.DomainType = ptcDomainTime
 oUSD.FunctionType = ptcFunctionTimeResponseType
 oUSD.XAxis.MaxCount = c_lSamples
 oUSD.XAxis.Min = 0
 oUSD.XAxis.Max = 2 * c_dPi
 oUSD.XAxis.Unit = "s"
 oUSD.XAxis.Name = "Time"
 oUSD.YAxis.Min = -1.0
 oUSD.YAxis.Max = 1.0
 oUSD.YAxis.Name = "Voltage"
 oUSD.YAxis.Unit = "V"
 oUSD.ResponseDOFs.Assign(0, ptcPlusZTranslation, "Usr", "Voltage", "V")
 Dim oPointDomains As PointDomains
    Set oPointDomains = oFile.GetPointDomains(ptcBuildPointData3d)
 Dim oSignal As Signal
 Set oSignal = oPointDomains.AddSignal(oUSD)
 Dim data(0 To c_lSamples-1) As Single
 Dim oPointDomain As PointDomain
 Set oPointDomain = oPointDomains.type(ptcDomainTime)
 Dim oDataPoint As DataPoint
 Set oDataPoint = oPointDomain.DataPoints(1)
 oDataPoint.SetData(oSignal, 1, data)
 Dim i As Integer
 Dim j As Integer
 For i = 1 To c_lDiskSectors
  Dim phase As Double
  phase = i * c_lVibrationNodes * 2 * c_dPi / c_lDiskSectors
  For j = 0 To c_lSamples-1
   data(j) = Sin(phase + j * 2 * c_dPi / c_lSamples)
  Next j
  Set oDataPoint = oPointDomain.DataPoints(i + 1)
  oDataPoint.SetData(oSignal, 1, data)
 Next
End Sub
```
