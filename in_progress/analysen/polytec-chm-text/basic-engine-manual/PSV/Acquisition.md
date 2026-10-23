# PSV – Acquisition

## Acquisition Object

*Quelle: `PSV~Acquisition.html` · Polytec PSV Type Library*

### Description

The Acquisition object controls the hardware and data acquisition of PSV and VibSoft.

### Object Model


---

## Acquisition Object Members

*Quelle: `PSV~Acquisition_members.html` · Polytec PSV Type Library*

### Public Methods

| AssignFocusAutomatically | Performs the assign focus values automatically command for all scan points or for the selected scan points, only. |
|---|---|
| AutoFocusLaser | Focuses the lasers of the scanning heads. |
| CalculateFocusValues | Calculates the focus values for the specified laser positions. |
| ExportVideoSnapshot | Exports a snapshot of the video image to a file in the formats Bitmap (.bmp), Jpeg (.jpg), Tiff (.tif), PNG (.png) or GIF (.gif). |
| ExportVideoSnapshotEx | Exports a snapshot of the requested camera video image to a file in the formats Bitmap (.bmp), Jpeg (.jpg), Tiff (.tif), PNG (.png) or GIF (.gif). |
| GeometryScan | Performs a geometry scan for all scan points or for the selected scan points, only. |
| GetData | Gets a PointData object for the given display. |
| GetLaserOn | Checks whether the laser of the specified scanning head is on. |
| GetSelectedMeasPoints | Gets the indices (labels) or numbers of the scan points currently selected in acquisition mode. |
| GetSignalAmplitudes | Gets the signal amplitude values for the channels referenced by the given channel indices. |
| MatchPointMarkers | Matches markers in the live video with previously found markers. |
| MeasurePathLength | Measures the optical path length of the reference path on MSA-650 systems. |
| PathLengthScan | On MSA-650 systems starts a path length scan. |
| Scan | Starts a scanning measurement. |
| ScanEx | Starts a scanning measurement. |
| SetLaserOn | Switches the laser of the specified scanning head on or off. |
| SetSelectedMeasPoints | Sets the indices (labels) or numbers of the scan points currently selected in acquisition mode. |
| Start | Starts a single point measurement. |
| Stop | Stops a measurement. |
| TakeReferenceSnapshot | Takes and stores a snapshot of the live video image. |
| TakeSnapshotAndGetPixelCoordinates | Takes a snapshot of the live video image and calclates the translation of a patten in the video image relative to the position of the pattern in the snapshot taken by TakeReferenceSnapshot . |

### Public Properties

| ActiveProperties | The acquisition properties for the active acquisition mode. |
|---|---|
| AvailableSnapshotTypes | Gets the available snapshot types. |
| Document | The acquisition document. |
| FindPointMarkers | Finds point markers in the live video image and returns a collection with the found markers. |
| GeneratorsOn | Specifies, whether the signal generators are switched on. |
| Infos | The InfosAcq collection . |
| Mode | Specifies the active acquisition mode. |
| ModeProperties | The collection of acquisition properties. This collection contains the acquisition properties for every acquisition mode. |
| PointDomains | Named and typed collection of the available domains of the point data. |
| ScanCaps | The capabilities for a scan. |
| ScanFileName | Specifies the file name for a scanning measurement. |
| State | The state of the acquisition. |

### Events

| AcqStateChanged | The AcqStateChanged event is raised, when the acquisition state has changed. |
|---|---|
| ScanStateChanged | The ScanStateChanged event is raised, when the scan state has changed. |


---

## AssignFocusAutomatically Method

*Quelle: `PSV~Acquisition~AssignFocusAutomatically.html` · Polytec PSV Type Library · Acquisition Object : AssignFocusAutomatically Method*

### Description

Performs the assign focus values automatically command for all scan points or for the selected scan points, only.

### Syntax

*Visual Basic:*
```
Public Sub AssignFocusAutomatically( _
   ByVal assignFocusAutomaticallyCaps As PTCAssignFocusAutomaticallyCaps _
)
```

### Parameters

assignFocusAutomaticallyCaps

| Value | Description |
|---|---|
| ptcAssignFocusAutomaticallyCapsNone | The focus values are determined from and assigned to all scan points. |
| ptcAssignFocusAutomaticallyCapsSelected | The focus values are determined from and assigned to the selected scan points, only. |
The capabilities of the assign focus values automatically command.

### Remarks

A number of scan points determined by the software is automatically focused and the focus values determined are assigned to all scan points and are saved with the object geometry.


---

## AutoFocusLaser Method

*Quelle: `PSV~Acquisition~AutoFocusLaser.html` · Polytec PSV Type Library · Acquisition Object : AutoFocusLaser Method*

### Description

Focuses the lasers of the scanning heads.

### Syntax

*Visual Basic:*
```
Public Function AutoFocusLaser( _
   ByVal scanHeadIndex As Long, _
   ByVal fullRange As Boolean _
) As Boolean
```

### Parameters

scanHeadIndex

The one-based index of the scanning head to focus.

fullRange

Specify true to search the focus in the full range. Specify false to search near the current focus position only, which is faster.

### Remarks

Specify -1 for the scan head index to focus all scanning heads.


---

## CalculateFocusValues Method

*Quelle: `PSV~Acquisition~CalculateFocusValues.html` · Polytec PSV Type Library · Acquisition Object : CalculateFocusValues Method*

### Description

Calculates the focus values for the specified laser positions.

### Syntax

*Visual Basic:*
```
Public Function CalculateFocusValues( _
   ByVal laserPositions() As Double, _
   ByVal scanHeadIndex() As Long _
) As Long()
```

### Parameters

laserPositions

The array containing the coordinates of the laser positions, where the positions are stored consecutively as triples of their x-, y-, and z-coordinates in meter.

scanHeadIndex

The zero-based indices of the scan heads corresponding to the referenced lasers.

### Return Type

The focus values for the laser positions.


---

## ExportVideoSnapshot Method

*Quelle: `PSV~Acquisition~ExportVideoSnapshot.html` · Polytec PSV Type Library · Acquisition Object : ExportVideoSnapshot Method*

### Description

Exports a snapshot of the video image to a file in the formats Bitmap (.bmp), Jpeg (.jpg), Tiff (.tif), PNG (.png) or GIF (.gif).

### Syntax

*Visual Basic:*
```
Public Sub ExportVideoSnapshot( _
   ByVal bstrFileName As String _
)
```

### Parameters

bstrFileName

The file name of the export file.


---

## ExportVideoSnapshotEx Method

*Quelle: `PSV~Acquisition~ExportVideoSnapshotEx.html` · Polytec PSV Type Library · Acquisition Object : ExportVideoSnapshotEx Method*

### Description

Exports a snapshot of the requested camera video image to a file in the formats Bitmap (.bmp), Jpeg (.jpg), Tiff (.tif), PNG (.png) or GIF (.gif).

### Syntax

*Visual Basic:*
```
Public Sub ExportVideoSnapshotEx( _
   ByVal bstrFileName As String, _
   ByVal snapshotType As PTCSnapshotType _
)
```

### Parameters

bstrFileName

The file name of the export file.

snapshotType

| Value | Description |
|---|---|
| ptcSnapshotTypeAuxCamera | A snapshot of the auxiliary camera is generated. |
| ptcSnapshotTypeMainCamera | A snapshot of the main camera is generated. |
| ptcSnapshotTypeOverviewImage | A snapshot of the overview image is generated. |
The type of the snapshot to create and export.

### Remarks

For a list of the available snapshot types see AvailableSnapshotTypes Property.


---

## GeometryScan Method

*Quelle: `PSV~Acquisition~GeometryScan.html` · Polytec PSV Type Library · Acquisition Object : GeometryScan Method*

### Description

Performs a geometry scan for all scan points or for the selected scan points, only.

### Syntax

*Visual Basic:*
```
Public Sub GeometryScan( _
   ByVal geometryScanCaps As PTCGeometryScanCaps _
)
```

### Parameters

geometryScanCaps

| Value | Description |
|---|---|
| ptcGeometryScanCapsNone | The geometry scan is performed for all scan points and without refining the measured distances using the focusing unit. |
| ptcGeometryScanCapsRefineWithAutoFocus | Uses the focusing unit of the scanning head after measuring the distances to refine the measured distances. |
| ptcGeometryScanCapsSelected | Performs the geometry scan for the selected scan points, only. |
The capabilities of the geometry scan.

### Remarks

If applicable, the software switches over to the geometry laser automatically. The geometry laser is positioned at every scan point, measures the distance from the scanning head and determines every x, y and z-coordinate.


---

## GetData Method

*Quelle: `PSV~Acquisition~GetData.html` · Polytec PSV Type Library · Acquisition Object : GetData Method*

### Description

Gets a PointData object for the given display.

### Syntax

*Visual Basic:*
```
Public Function GetData( _
   ByVal pIDisplay As IDisplay2 _
) As IPointData
```

### Parameters

pIDisplay

The Display object.

### Example

For a complete example on how to use the GetData method, see the RemoteAcquisition.bas example macro.

The following subroutine gets the acquisition point data for a specific domain, channel, signal and display for the current scan point index. It traces the data to the debug output window.

- Get Data during Acquisition (Visual Basic)

```
Private Sub GetData(DomainType As PTCDomainType, ChannelString As String, SignalString As String, DisplayType As PTCDisplayType, ScanPoint As Long)
    Dim oAcquisition As Acquisition
    Set oAcquisition = Application.Acquisition

    Dim oDisplay As Display
    Set oDisplay = oAcquisition.PointDomains.Type(DomainType).Channels.Item(ChannelString).Signals.Item(SignalString).Displays.Type(DisplayType)

    ' Get the acquisition data object used for the current data acquisition.
    ' Release this acquisition data instance before new data acquisition will be started.
    Dim oAcquisitionPointData As AcquisitionPointData
    Set oAcquisitionPointData = oAcquisition.GetData(oDisplay)

    Dim oAcquisitionPointDataStream As AcquisitionPointDataStream
    Set oAcquisitionPointDataStream = oAcquisitionPointData.OpenDataStream(oAcquisitionPointData.BlockCount, 0)

    Debug.Print "ScanPoint Index: ";ScanPoint
    Debug.Print "Domain: ";oDisplay.Signal.Channel.Domain.Name
    Debug.Print "Channel: ";ChannelString
    Debug.Print "Signal: ";SignalString
    Debug.Print "Display: ";oDisplay.Name

    Dim oXAxis As AcquisitionXAxis
    Set oXAxis = oAcquisitionPointData.XAxis

    Dim oYAxes As AcquisitionYAxes
    Set oYAxes = oAcquisitionPointData.YAxes

    Dim AxesString As String
    AxesString = oXAxis.Name + " / " + oXAxis.Unit

    If (oAcquisitionPointDataStream.Stride <> oYAxes.Count) Then
        MsgBox "oAcquisitionPointDataStream.Stride should be equal to oYAxes.Count."
    End If

    Dim oYAxis As AcquisitionYAxis

    For Each oYAxis In oYAxes
        AxesString = AxesString + "    " + oYAxis.Name + " / " + oYAxis.Unit
    Next oYAxis

    Debug.Print AxesString

    Dim Stride As Long
    Stride = oAcquisitionPointDataStream.Stride

    While (oAcquisitionPointDataStream.Position < oAcquisitionPointDataStream.Length)

        Dim XIndex As Long
        XIndex = oAcquisitionPointDataStream.Position

        Dim Data() As Single
        oAcquisitionPointDataStream.Read(0, -1, Data)

        Dim LineString As String

        Dim SampleIndex As Long
        SampleIndex = 0

        Dim DataIndex, StrideIndex As Long

        For DataIndex = Lbound(Data) To Ubound(Data) Step Stride

            LineString = CStr(oXAxis.GetMidX(XIndex+SampleIndex))

            For StrideIndex = 0 To Stride-1
                LineString = LineString + "    " + CStr(Data(DataIndex+StrideIndex))
            Next StrideIndex

            Debug.Print LineString

            SampleIndex = SampleIndex + 1

        Next DataIndex
    Wend

    Debug.Print ""

    oAcquisitionPointDataStream.Close

End Sub
```


---

## GetLaserOn Method

*Quelle: `PSV~Acquisition~GetLaserOn.html` · Polytec PSV Type Library · Acquisition Object : GetLaserOn Method*

### Description

Checks whether the laser of the specified scanning head is on.

### Syntax

*Visual Basic:*
```
Public Function GetLaserOn( _
   ByVal scanHeadIndex As Long _
) As Boolean
```

### Parameters

scanHeadIndex

The index of the scanning head (1 for top, 2 for left, 3 for right) or -1 for all scanning heads.

### Remarks

If -1 is passed as the scanning head index, the returned value is true, if the lasers of all scanning heads are on and false otherwise.

### Example


---

## GetSelectedMeasPoints Method

*Quelle: `PSV~Acquisition~GetSelectedMeasPoints.html` · Polytec PSV Type Library · Acquisition Object : GetSelectedMeasPoints Method*

### Description

Gets the indices (labels) or numbers of the scan points currently selected in acquisition mode.

### Syntax

*Visual Basic:*
```
Public Function GetSelectedMeasPoints( _
   Optional ByVal labels As Boolean = True _
) As Long()
```

### Parameters

labels

If true the indices (labels) of the points are returned, otherwise the numbers.

### Return Type

Array of indices (labels) or numbers of the scan points


---

## GetSignalAmplitudes Method

*Quelle: `PSV~Acquisition~GetSignalAmplitudes.html` · Polytec PSV Type Library · Acquisition Object : GetSignalAmplitudes Method*

### Description

Gets the signal amplitude values for the channels referenced by the given channel indices.

### Syntax

*Visual Basic:*
```
Public Function GetSignalAmplitudes( _
   ByVal channelIndices() As Long _
) As Double()
```

### Parameters

channelIndices

The list of the one-based channel indices of the channels for which to return the signal amplitude values. An empty array indicates to return the signal amplitude values of all channels.

### Return Type

The signal amplitude values.

### Remarks

The amplitude values are given in percent of the maximum level.

If a referenced channel has multiple physical subchannels, then the signal amplitude values of all physical subchannels are stored consecutively in the return array, at the corresponding position for the channel in the array. Likewise, if the channel Vib3D is requested, then the amplitude values of VibTop, VibLeft, and VibRight are embedded consecutively and in the given order in the return array.


---

## MatchPointMarkers Method

*Quelle: `PSV~Acquisition~MatchPointMarkers.html` · Polytec PSV Type Library · Acquisition Object : MatchPointMarkers Method*

### Description

Matches markers in the live video with previously found markers.

### Syntax

*Visual Basic:*
```
Public Function MatchPointMarkers( _
   ByVal foundPointMarkers As PointMarkers _
) As PointMarkers
```

### Parameters

foundPointMarkers

The previously found markers.

### Return Type

The matched markers.

### Remarks

From the first and second 3D coordinates of the markers, a transformation can be calculated that can be applied to the current 3D alignment. With that, movements of the measurement object can be compensated before the scan starts and the lasers will still hit the correct positions on the measurement object.


---

## MeasurePathLength Method

*Quelle: `PSV~Acquisition~MeasurePathLength.html` · Polytec PSV Type Library · Acquisition Object : MeasurePathLength Method*

### Description

Measures the optical path length of the reference path on MSA-650 systems.

### Syntax

*Visual Basic:*
```
Public Function MeasurePathLength( _
   ByRef pathLength As Double _
) As Boolean
```

### Parameters

pathLength

Receives the measured optical path length.

### Return Type

Returns true, if the measurement was successful.


---

## PathLengthScan Method

*Quelle: `PSV~Acquisition~PathLengthScan.html` · Polytec PSV Type Library · Acquisition Object : PathLengthScan Method*

### Description

On MSA-650 systems starts a path length scan.

### Syntax

*Visual Basic:*
```
Public Sub PathLengthScan()
```


---

## Scan Method

*Quelle: `PSV~Acquisition~Scan.html` · Polytec PSV Type Library · Acquisition Object : Scan Method*

### Description

Starts a scanning measurement.

### Syntax

*Visual Basic:*
```
Public Sub Scan( _
   ByVal ScanMode As PTCScanMode _
)
```

### Parameters

ScanMode

| Value | Description |
|---|---|
| ptcScanAll | Starts a complete scan of all measurement points. |
| ptcScanContinue | Continues a previously started scan. |
| ptcScanRemeasure | Starts a re-measurement of a previously started scan. |
| ptcScanRemeasureAutoRange | Starts a re-measurement of a previously started scan with automatic adjustment of the vibrometer range for scan points with scan status overrange. |
| ptcScanRemeasureFile | Starts a re-measurement of the scan file specified in the ScanFileName Property . |
The mode of the scan.

### Remarks

This method is relevant for PSV only.


---

## ScanEx Method

*Quelle: `PSV~Acquisition~ScanEx.html` · Polytec PSV Type Library · Acquisition Object : ScanEx Method*

### Description

Starts a scanning measurement.

### Syntax

*Visual Basic:*
```
Public Sub ScanEx( _
   ByVal ScanMode As PTCScanMode, _
   ByVal ScanCaps As PTCScanCaps _
)
```

### Parameters

ScanMode

| Value | Description |
|---|---|
| ptcScanAll | Starts a complete scan of all measurement points. |
| ptcScanContinue | Continues a previously started scan. |
| ptcScanRemeasure | Starts a re-measurement of a previously started scan. |
| ptcScanRemeasureAutoRange | Starts a re-measurement of a previously started scan with automatic adjustment of the vibrometer range for scan points with scan status overrange. |
| ptcScanRemeasureFile | Starts a re-measurement of the scan file specified in the ScanFileName Property . |
The mode of the scan.

ScanCaps

| Value | Description |
|---|---|
| ptcScanCapsAsynchronousScanEvent | When passing this flag, the scan-progress/completion events are fired. asynchronously. On VibroScan systems this allows the software to use the faster, autonomous scan mode. In this case, you cannot rely on e.g. getting the current values of the scanner angles or being able to modify those before progressing to the next scan point, because the scan is performed asynchronously by the VibroScan system. |
| ptcScanCapsAutoFocusDuringScan | The autofocusing will be performed during the scan. |
| ptcScanCapsNone | No capabilities. |
| ptcScanCapsUseAssignedFocusValuesDuringScan | The assigned focus values will be used during the scan. |
| ptcScanCapsVideoTriangulation | The video triangulation will be performed during the scan. |
| ptcScanCapsVideoTriangulationFast | The fast video triangulation will be performed during the scan. |
The capabilities of the scan.

### Remarks

This method is relevant for PSV only.


---

## SetLaserOn Method

*Quelle: `PSV~Acquisition~SetLaserOn.html` · Polytec PSV Type Library · Acquisition Object : SetLaserOn Method*

### Description

Switches the laser of the specified scanning head on or off.

### Syntax

*Visual Basic:*
```
Public Sub SetLaserOn( _
   ByVal scanHeadIndex As Long, _
   ByVal laserOn As Boolean, _
   ByVal moveLaser As Boolean _
)
```

### Parameters

scanHeadIndex

The index of the scanning head (1 for top, 2 for left, 3 for right) or -1 for all scanning heads.

laserOn

True to switch the laser on, false to switch the laser off.

moveLaser

True to move the laser in addition to switching it off.

### Remarks

When you pass False to the laserOn parameter and True to the moveLaser parameter, the laser is switched off and in addition to that the laser is moved to the maximum scanner angles to avoid the remaining light of the laser being visible in the video image.

### Example


---

## SetSelectedMeasPoints Method

*Quelle: `PSV~Acquisition~SetSelectedMeasPoints.html` · Polytec PSV Type Library · Acquisition Object : SetSelectedMeasPoints Method*

### Description

Sets the indices (labels) or numbers of the scan points currently selected in acquisition mode.

### Syntax

*Visual Basic:*
```
Public Sub SetSelectedMeasPoints( _
   ByVal pointNumbers() As Long, _
   Optional ByVal labels As Boolean = True _
)
```

### Parameters

pointNumbers

Array of indices (labels) or numbers of the scan points.

labels

If true the indices (labels) of the points are specified, otherwise the numbers.

### Remarks

If only a single scan point is selected, the software will move the lasers to this point. Please note that this is not be possible during a measurement.


---

## Start Method

*Quelle: `PSV~Acquisition~Start.html` · Polytec PSV Type Library · Acquisition Object : Start Method*

### Description

Starts a single point measurement.

### Syntax

*Visual Basic:*
```
Public Sub Start( _
   ByVal StartMode As PTCAcqStartMode _
)
```

### Parameters

StartMode

| Value | Description |
|---|---|
| ptcAcqStartContinuous | Continuous measurement. |
| ptcAcqStartSingle | Single measurement. |
The mode of the single point measurement.


---

## Stop Method

*Quelle: `PSV~Acquisition~Stop.html` · Polytec PSV Type Library · Acquisition Object : Stop Method*

### Description

Stops a measurement.

### Syntax

*Visual Basic:*
```
Public Sub Stop()
```


---

## TakeReferenceSnapshot Method

*Quelle: `PSV~Acquisition~TakeReferenceSnapshot.html` · Polytec PSV Type Library · Acquisition Object : TakeReferenceSnapshot Method*

### Description

Takes and stores a snapshot of the live video image.

### Syntax

*Visual Basic:*
```
Public Sub TakeReferenceSnapshot()
```

### Remarks

Later on you can use TakeSnapshotAndGetPixelCoordinates to calculate the translation of a patten in the video image.

### Example

See sample macro MoveGeometryMSA.bas.


---

## TakeSnapshotAndGetPixelCoordinates Method

*Quelle: `PSV~Acquisition~TakeSnapshotAndGetPixelCoordinates.html` · Polytec PSV Type Library · Acquisition Object : TakeSnapshotAndGetPixelCoordinates Method*

### Description

Takes a snapshot of the live video image and calclates the translation of a patten in the video image relative to the position of the pattern in the snapshot taken by TakeReferenceSnapshot.

### Syntax

*Visual Basic:*
```
Public Sub TakeSnapshotAndGetPixelCoordinates( _
   ByVal aoiTopLeftX As Long, _
   ByVal aoiTopLeftY As Long, _
   ByVal aoiWidth As Long, _
   ByVal aoiHeight As Long, _
   ByRef refPixelX As Double, _
   ByRef refPixelY As Double, _
   ByRef currentPixelX As Double, _
   ByRef currentPixelY As Double _
)
```

### Parameters

aoiTopLeftX

The x-coordinate of the top left corner of the area of interest (the patten) in pixels.

aoiTopLeftY

The y-coordinate of the top left corner of the area of interest (the patten) in pixels.

aoiWidth

The width of the area of interest (the patten) in pixels.

aoiHeight

The height of the area of interest (the patten) in pixels.

refPixelX

Receives the x-coordinate of the position of the pattern in the reference snapshot.

refPixelY

Receives the y-coordinate of the position of the pattern in the reference snapshot.

currentPixelX

Receives the x-coordinate of the position of the pattern in the current snapshot.

currentPixelY

Receives the y-coordinate of the position of the pattern in the current snapshot.

### Example

See sample macro MoveGeometryMSA.bas.


---

## ActiveProperties Property

*Quelle: `PSV~Acquisition~ActiveProperties.html` · Polytec PSV Type Library · Acquisition Object : ActiveProperties Property*

### Description

The acquisition properties for the active acquisition mode.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ActiveProperties As IAcquisitionProperties3
```


---

## AvailableSnapshotTypes Property

*Quelle: `PSV~Acquisition~AvailableSnapshotTypes.html` · Polytec PSV Type Library · Acquisition Object : AvailableSnapshotTypes Property*

### Description

Gets the available snapshot types.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AvailableSnapshotTypes As PTCSnapshotType()
```

### Return Type

The available snapshot types.

### Remarks

Gets an array of the snapshot types that are available for export via the ExportVideoSnapshotEx Method.


---

## Document Property

*Quelle: `PSV~Acquisition~Document.html` · Polytec PSV Type Library · Acquisition Object : Document Property*

### Description

The acquisition document.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Document As VibDocument
```


---

## FindPointMarkers Property

*Quelle: `PSV~Acquisition~FindPointMarkers.html` · Polytec PSV Type Library · Acquisition Object : FindPointMarkers Property*

### Description

Finds point markers in the live video image and returns a collection with the found markers.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FindPointMarkers As PointMarkers
```

### Return Type

The found markers.


---

## GeneratorsOn Property

*Quelle: `PSV~Acquisition~GeneratorsOn.html` · Polytec PSV Type Library · Acquisition Object : GeneratorsOn Property*

### Description

Specifies, whether the signal generators are switched on.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property GeneratorsOn As Boolean
```

### Remarks

Currently PSV and VibSoft only support a single generator.


---

## Infos Property

*Quelle: `PSV~Acquisition~Infos.html` · Polytec PSV Type Library · Acquisition Object : Infos Property*

### Description

The InfosAcq collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Infos As IInfos8
```


---

## Mode Property

*Quelle: `PSV~Acquisition~Mode.html` · Polytec PSV Type Library · Acquisition Object : Mode Property*

### Description

Specifies the active acquisition mode.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Mode As PTCAcqMode
```


---

## ModeProperties Property

*Quelle: `PSV~Acquisition~ModeProperties.html` · Polytec PSV Type Library · Acquisition Object : ModeProperties Property*

### Description

The collection of acquisition properties. This collection contains the acquisition properties for every acquisition mode.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ModeProperties As AcqModeProperties
```


---

## PointDomains Property

*Quelle: `PSV~Acquisition~PointDomains.html` · Polytec PSV Type Library · Acquisition Object : PointDomains Property*

### Description

Named and typed collection of the available domains of the point data.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PointDomains As IDomains2
```

### Return Type

The Domains object.

### Remarks

Use this property to select a domain, channel, signal and display to retrieve data for with the GetData method.

### Example


---

## ScanCaps Property

*Quelle: `PSV~Acquisition~ScanCaps.html` · Polytec PSV Type Library · Acquisition Object : ScanCaps Property*

### Description

The capabilities for a scan.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanCaps As PTCScanCaps
```

### Remarks

All or a subset of these capabilities can be specified as a parameter for the ScanEx Method.


---

## ScanFileName Property

*Quelle: `PSV~Acquisition~ScanFileName.html` · Polytec PSV Type Library · Acquisition Object : ScanFileName Property*

### Description

Specifies the file name for a scanning measurement.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScanFileName As String
```

### Remarks

This property is relevant for PSV only. If the scan file name is empty, the software will ask at the start of the scan for a file name. To retrieve the filename of the scan file in this case, you can use the Name Property of the document returned by the ActiveDocument Property.


---

## State Property

*Quelle: `PSV~Acquisition~State.html` · Polytec PSV Type Library · Acquisition Object : State Property*

### Description

The state of the acquisition.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property State As PTCAcqState
```


---

## AcqStateChanged Event

*Quelle: `PSV~Acquisition~AcqStateChanged_EV.html` · Polytec PSV Type Library · Acquisition Object : AcqStateChanged Event*

### Description

The AcqStateChanged event is raised, when the acquisition state has changed.

### Syntax

*Visual Basic:*
```
Public Event AcqStateChanged( _
   ByVal AcqState As PTCAcqState _
)
```

### Parameters

AcqState

| Value | Description |
|---|---|
| ptcAcqStateAutoFocus | A focus measurement is in progress. |
| ptcAcqStateContinuous | Continuous measurement is in progress. |
| ptcAcqStatePathLength | A measurement of the optical path length is in progress. |
| ptcAcqStateScanAll | A scanning measurement of all points is in progress. |
| ptcAcqStateScanContinue | A scanning measurement is being continued. |
| ptcAcqStateScanRemeasure | A scanning re-measurement is in progress. |
| ptcAcqStateSingle | Single shot measurement is in progress. |
| ptcAcqStateStopped | Measurement is stopped. |
The new acquisition state.


---

## ScanStateChanged Event

*Quelle: `PSV~Acquisition~ScanStateChanged_EV.html` · Polytec PSV Type Library · Acquisition Object : ScanStateChanged Event*

### Description

The ScanStateChanged event is raised, when the scan state has changed.

### Syntax

*Visual Basic:*
```
Public Event ScanStateChanged( _
   ByVal ScanState As PTCScanState, _
   ByVal ScanPoint As Long _
)
```

### Parameters

ScanState

| Value | Description |
|---|---|
| ptcScanStateBeginScan | The scan has begun. |
| ptcScanStateBeginScanPoint | The mirrors have been positioned and the measurement at the scan point is about to begin. |
| ptcScanStateEndScan | The scan has finished. |
| ptcScanStateEndScanPoint | The measurement at the scan point has finished. |
The new scan state.

ScanPoint

The 1-based index of the current scan point.

### Remarks

During a scan, the sequence of ScanStateChanged events is

- Acquisition.Scan()
- ScanStateChanged(ptcScanStateBeginScan, 0)
- For every scan point n
- The PSV Software positions the laser beam and prepares the measurement at the current scan point
- ScanStateChanged(ptcScanStateBeginScanPoint, n)
- The PSV Software performs the measurement at the current scan point
- ScanStateChanged(ptcScanStateEndScanPoint, n)

- ScanStateChanged(ptcScanStateEndScan, 0))

On PSV-500-H, PSV-500-NB and PSV-500-3D-H systems the sequence is different when VideoTriangulation is off:

- Acquisition.Scan()
- ScanStateChanged(ptcScanStateBeginScan, 0)
- For every scan point n
- ScanStateChanged(ptcScanStateBeginScanPoint, n)
- The PSV Software triggers the movement of the mirrors and prepares the measurement at the current scan point
- The mirrors move and when the mirrors have stopped, the
- The PSV Software performs the measurement at the current scan point
- ScanStateChanged(ptcScanStateEndScanPoint, n)

- ScanStateChanged(ptcScanStateEndScan, 0)

### Example

The following example shows how to handle the ScanStateChanged event in a PSV Basic Engine macro during a scan. The macro waits for the scan to finish. If you do not wait, the macro will finish before the scan finishes and the handler will not be called any more.

For a scan with 9 scan points the macro will generate e.g. the following output. The sequence of the scan points depends on the geometry and the preferences set for the scan direction.

ptcScanStateBeginScan 0
ptcScanStateBeginScanPoint 3
ptcScanStateEndScanPoint 3
ptcScanStateBeginScanPoint 2
ptcScanStateEndScanPoint 2
ptcScanStateBeginScanPoint 1
ptcScanStateEndScanPoint 1
ptcScanStateBeginScanPoint 4
ptcScanStateEndScanPoint 4
ptcScanStateBeginScanPoint 5
ptcScanStateEndScanPoint 5
ptcScanStateBeginScanPoint 6
ptcScanStateEndScanPoint 6
ptcScanStateBeginScanPoint 9
ptcScanStateEndScanPoint 9
ptcScanStateBeginScanPoint 8
ptcScanStateEndScanPoint 8
ptcScanStateBeginScanPoint 7
ptcScanStateEndScanPoint 7
ptcScanStateEndScan 0

- Handle the ScanStateChanged Event (Visual Basic)

```
Option Explicit

Sub Main
    Debug.Clear
    Acquisition.ScanFileName = "D:\Temp\Scan.svd"
    Acquisition.Scan(ptcScanAll)
    While (Acquisition.State <> ptcAcqStateStopped)
        Wait 0.1
    Wend
End Sub

Public Sub ScanStateChanged(ScanState As PTCScanState, ScanPoint As Long)
    Select Case ScanState
        Case ptcScanStateBeginScan
            Debug.Print "ptcScanStateBeginScan      ";ScanPoint
        Case ptcScanStateBeginScanPoint
            Debug.Print "ptcScanStateBeginScanPoint ";ScanPoint
        Case ptcScanStateEndScanPoint
            Debug.Print "ptcScanStateEndScanPoint   ";ScanPoint
        Case ptcScanStateEndScan
            Debug.Print "ptcScanStateEndScan        ";ScanPoint
    End Select
End Sub
```

- Handle the ScanStateChanged Event with WWB.NET (Visual Basic)

```
'#Language "WWB.NET"

Option Explicit

Dim WithEvents oAcqEvents As Acquisition

Sub Main
    oAcqEvents = Acquisition

    Debug.Clear
    Acquisition.ScanFileName = "D:\Temp\Scan.svd"
    Acquisition.Scan(PTCScanMode.ptcScanAll)
    While (Acquisition.State <> PTCAcqState.ptcAcqStateStopped)
        Wait 0.1
    End While
End Sub

Public Sub AcqEvents_ScanStateChanged(ByVal ScanState As PTCScanState, ByVal ScanPoint As Integer) Handles oAcqEvents.ScanStateChanged
    Select Case ScanState
        Case PTCScanState.ptcScanStateBeginScan
            Debug.Print "ptcScanStateBeginScan      ";ScanPoint
        Case PTCScanState.ptcScanStateBeginScanPoint
            Debug.Print "ptcScanStateBeginScanPoint ";ScanPoint
        Case PTCScanState.ptcScanStateEndScanPoint
            Debug.Print "ptcScanStateEndScanPoint   ";ScanPoint
        Case PTCScanState.ptcScanStateEndScan
            Debug.Print "ptcScanStateEndScan        ";ScanPoint
    End Select
End Sub
```
