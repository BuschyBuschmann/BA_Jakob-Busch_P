# POLYSIGNALLib – FunctionTypes

## FunctionTypes Object

*Quelle: `POLYSIGNALLib~FunctionTypes.html` · Polytec PolySignal Type Library*

### Description

The FunctionTypes object provides a list of all PTCFunctionType enumerator values and their string representations. You can use the object e.g. to create a user interface to let the user select a value.

### Remarks

Supported languages are English (US) and German (Germany). All other system languages default to English (US).

### Example

The following example lists all PTCFunctionType enumerator values and their string representations in the current system language and in German.

- List FunctionTypes (Visual Basic)

```
Option Explicit

Sub Main
    Debug.Clear

    Dim oFunctionTypes As New FunctionTypes
    Dim index As Long
    For index = 0 To oFunctionTypes.Count-1
        Dim ptcFunction As PTCFunctionType
        ptcFunction = oFunctionTypes.GetEnumItem(index)
        Dim strGerman As String
        strGerman = oFunctionTypes.GetLocaleString(ptcFunction, &H0407)
        Dim strDefault As String
        strDefault = oFunctionTypes.GetString(ptcFunction)
        Debug.Print "Index: ";index;" Enum: ";ptcFunction;" German: ";strGerman; " Default: ";strDefault
    Next
End Sub
```


---

## FunctionTypes Object Members

*Quelle: `POLYSIGNALLib~FunctionTypes_members.html` · Polytec PolySignal Type Library*

### Public Methods

| GetEnumItem | Gets the enumerator value for the given index. |
|---|---|
| GetIndex | Gets the index for the given enumerator value. |
| GetLocaleString | Gets the string representation for the given enumerator value in the given locale. |
| GetString | Gets the string representation for the given enumerator value in the current system locale. |

### Public Properties

| Count | The number of enumerator values. |
|---|---|


---

## GetEnumItem Method

*Quelle: `POLYSIGNALLib~FunctionTypes~GetEnumItem.html` · Polytec PolySignal Type Library · FunctionTypes Object : GetEnumItem Method*

### Description

Gets the enumerator value for the given index.

### Syntax

*Visual Basic:*
```
Public Function GetEnumItem( _
   ByVal lIndex As Long _
) As PTCFunctionType
```

### Parameters

lIndex

The 0-based index of the enumerator value.


---

## GetIndex Method

*Quelle: `POLYSIGNALLib~FunctionTypes~GetIndex.html` · Polytec PolySignal Type Library · FunctionTypes Object : GetIndex Method*

### Description

Gets the index for the given enumerator value.

### Syntax

*Visual Basic:*
```
Public Function GetIndex( _
   ByVal PTCFunctionType As PTCFunctionType _
) As Long
```

### Parameters

PTCFunctionType

| Value | Description |
|---|---|
| ptcFunctionAutoCorrelationType | Auto correlation. |
| ptcFunctionAutoSpectrumType | Auto power. |
| ptcFunctionBand | Band. |
| ptcFunctionCoherenceType | Coherence. |
| ptcFunctionComplexValuedDataType | Complex Valued Data. |
| ptcFunctionCrossCorrelationType | Cross correlation. |
| ptcFunctionCrossSpectrumType | Cross power. |
| ptcFunctionCumulativeFrequencyDistributionType | Cumulative Frequency Distribution. |
| ptcFunctionEigenvalueType | Eigenvalue. |
| ptcFunctionEigenvectorType | Eigenvector. |
| ptcFunctionEnergySpectralDensityType | ESD. |
| ptcFunctionFiniteImpulseResponseFilterType | FIR Filter. |
| ptcFunctionForcePatternType | Force Pattern. |
| ptcFunctionFrequencyResponseFunctionH1Type | H1. |
| ptcFunctionFrequencyResponseFunctionH2Type | H2. |
| ptcFunctionFrequencyResponseFunctionPCAH1Type | H1 for principal component analysis (MIMO). |
| ptcFunctionFrequencyResponseFunctionType | FRF |
| ptcFunctionImpulseResponseType | Impulse Response. |
| ptcFunctionIntensityType | Intensity. |
| ptcFunctionModeIndicatorFunctionType | Mode Indicator Function. |
| ptcFunctionMultipleCoherenceType | Multiple Coherence. |
| ptcFunctionOrbitType | Orbit. |
| ptcFunctionOrderFunctionType | Order. |
| ptcFunctionPartialCoherenceType | Partial Coherence. |
| ptcFunctionPartialPowerType | Partial Power. |
| ptcFunctionParticleVelocityType | Particle Velocity. |
| ptcFunctionPCAPrincipalInputsType | Principal Inputs for PCA (MIMO). |
| ptcFunctionPCAVirtualCoherencesType | Virtual Coherences for PCA (MIMO). |
| ptcFunctionPeaksValleyType | Peaks Valley. |
| ptcFunctionPIIndexType | PI Index. |
| ptcFunctionPowerSpectralDensityType | PSD. |
| ptcFunctionProbabilityDensityFunctionType | Probability density. |
| ptcFunctionRealValuedDataType | Real Valued Data. |
| ptcFunctionShockResponseSpectrumType | Shock Response. |
| ptcFunctionSoundPowerType | Sound Power. |
| ptcFunctionSoundPressureLevelType | Sound Pressure Level. |
| ptcFunctionSpectrumType | Spectrum. |
| ptcFunctionStrainCyclesType | Strain Cycles. |
| ptcFunctionStressCyclesType | Stress Cycles. |
| ptcFunctionTemperatureType | Temperature. |
| ptcFunctionTimeResponseType | Time Signal. |
| ptcFunctionTransmissibilityType | Transmissibility. |
| ptcFunctionUnknownType | Unknown. |
| ptcFunctionVddIQType | IQ signal for digital demodulation. |
The function type enumerator value.


---

## GetLocaleString Method

*Quelle: `POLYSIGNALLib~FunctionTypes~GetLocaleString.html` · Polytec PolySignal Type Library · FunctionTypes Object : GetLocaleString Method*

### Description

Gets the string representation for the given enumerator value in the given locale.

### Syntax

*Visual Basic:*
```
Public Function GetLocaleString( _
   ByVal PTCFunctionType As PTCFunctionType, _
   ByVal lLocaleID As Long _
) As String
```

### Parameters

PTCFunctionType

| Value | Description |
|---|---|
| ptcFunctionAutoCorrelationType | Auto correlation. |
| ptcFunctionAutoSpectrumType | Auto power. |
| ptcFunctionBand | Band. |
| ptcFunctionCoherenceType | Coherence. |
| ptcFunctionComplexValuedDataType | Complex Valued Data. |
| ptcFunctionCrossCorrelationType | Cross correlation. |
| ptcFunctionCrossSpectrumType | Cross power. |
| ptcFunctionCumulativeFrequencyDistributionType | Cumulative Frequency Distribution. |
| ptcFunctionEigenvalueType | Eigenvalue. |
| ptcFunctionEigenvectorType | Eigenvector. |
| ptcFunctionEnergySpectralDensityType | ESD. |
| ptcFunctionFiniteImpulseResponseFilterType | FIR Filter. |
| ptcFunctionForcePatternType | Force Pattern. |
| ptcFunctionFrequencyResponseFunctionH1Type | H1. |
| ptcFunctionFrequencyResponseFunctionH2Type | H2. |
| ptcFunctionFrequencyResponseFunctionPCAH1Type | H1 for principal component analysis (MIMO). |
| ptcFunctionFrequencyResponseFunctionType | FRF |
| ptcFunctionImpulseResponseType | Impulse Response. |
| ptcFunctionIntensityType | Intensity. |
| ptcFunctionModeIndicatorFunctionType | Mode Indicator Function. |
| ptcFunctionMultipleCoherenceType | Multiple Coherence. |
| ptcFunctionOrbitType | Orbit. |
| ptcFunctionOrderFunctionType | Order. |
| ptcFunctionPartialCoherenceType | Partial Coherence. |
| ptcFunctionPartialPowerType | Partial Power. |
| ptcFunctionParticleVelocityType | Particle Velocity. |
| ptcFunctionPCAPrincipalInputsType | Principal Inputs for PCA (MIMO). |
| ptcFunctionPCAVirtualCoherencesType | Virtual Coherences for PCA (MIMO). |
| ptcFunctionPeaksValleyType | Peaks Valley. |
| ptcFunctionPIIndexType | PI Index. |
| ptcFunctionPowerSpectralDensityType | PSD. |
| ptcFunctionProbabilityDensityFunctionType | Probability density. |
| ptcFunctionRealValuedDataType | Real Valued Data. |
| ptcFunctionShockResponseSpectrumType | Shock Response. |
| ptcFunctionSoundPowerType | Sound Power. |
| ptcFunctionSoundPressureLevelType | Sound Pressure Level. |
| ptcFunctionSpectrumType | Spectrum. |
| ptcFunctionStrainCyclesType | Strain Cycles. |
| ptcFunctionStressCyclesType | Stress Cycles. |
| ptcFunctionTemperatureType | Temperature. |
| ptcFunctionTimeResponseType | Time Signal. |
| ptcFunctionTransmissibilityType | Transmissibility. |
| ptcFunctionUnknownType | Unknown. |
| ptcFunctionVddIQType | IQ signal for digital demodulation. |
The function type enumerator value.

lLocaleID

The locale identifier.

### Remarks

Supported values are &H0407 for German (Germany) and &H0409 for English (US).


---

## GetString Method

*Quelle: `POLYSIGNALLib~FunctionTypes~GetString.html` · Polytec PolySignal Type Library · FunctionTypes Object : GetString Method*

### Description

Gets the string representation for the given enumerator value in the current system locale.

### Syntax

*Visual Basic:*
```
Public Function GetString( _
   ByVal PTCFunctionType As PTCFunctionType _
) As String
```

### Parameters

PTCFunctionType

| Value | Description |
|---|---|
| ptcFunctionAutoCorrelationType | Auto correlation. |
| ptcFunctionAutoSpectrumType | Auto power. |
| ptcFunctionBand | Band. |
| ptcFunctionCoherenceType | Coherence. |
| ptcFunctionComplexValuedDataType | Complex Valued Data. |
| ptcFunctionCrossCorrelationType | Cross correlation. |
| ptcFunctionCrossSpectrumType | Cross power. |
| ptcFunctionCumulativeFrequencyDistributionType | Cumulative Frequency Distribution. |
| ptcFunctionEigenvalueType | Eigenvalue. |
| ptcFunctionEigenvectorType | Eigenvector. |
| ptcFunctionEnergySpectralDensityType | ESD. |
| ptcFunctionFiniteImpulseResponseFilterType | FIR Filter. |
| ptcFunctionForcePatternType | Force Pattern. |
| ptcFunctionFrequencyResponseFunctionH1Type | H1. |
| ptcFunctionFrequencyResponseFunctionH2Type | H2. |
| ptcFunctionFrequencyResponseFunctionPCAH1Type | H1 for principal component analysis (MIMO). |
| ptcFunctionFrequencyResponseFunctionType | FRF |
| ptcFunctionImpulseResponseType | Impulse Response. |
| ptcFunctionIntensityType | Intensity. |
| ptcFunctionModeIndicatorFunctionType | Mode Indicator Function. |
| ptcFunctionMultipleCoherenceType | Multiple Coherence. |
| ptcFunctionOrbitType | Orbit. |
| ptcFunctionOrderFunctionType | Order. |
| ptcFunctionPartialCoherenceType | Partial Coherence. |
| ptcFunctionPartialPowerType | Partial Power. |
| ptcFunctionParticleVelocityType | Particle Velocity. |
| ptcFunctionPCAPrincipalInputsType | Principal Inputs for PCA (MIMO). |
| ptcFunctionPCAVirtualCoherencesType | Virtual Coherences for PCA (MIMO). |
| ptcFunctionPeaksValleyType | Peaks Valley. |
| ptcFunctionPIIndexType | PI Index. |
| ptcFunctionPowerSpectralDensityType | PSD. |
| ptcFunctionProbabilityDensityFunctionType | Probability density. |
| ptcFunctionRealValuedDataType | Real Valued Data. |
| ptcFunctionShockResponseSpectrumType | Shock Response. |
| ptcFunctionSoundPowerType | Sound Power. |
| ptcFunctionSoundPressureLevelType | Sound Pressure Level. |
| ptcFunctionSpectrumType | Spectrum. |
| ptcFunctionStrainCyclesType | Strain Cycles. |
| ptcFunctionStressCyclesType | Stress Cycles. |
| ptcFunctionTemperatureType | Temperature. |
| ptcFunctionTimeResponseType | Time Signal. |
| ptcFunctionTransmissibilityType | Transmissibility. |
| ptcFunctionUnknownType | Unknown. |
| ptcFunctionVddIQType | IQ signal for digital demodulation. |
The function type enumerator value.

### Remarks

Supported languages are English (US) and German (Germany). All other system languages default to English (US).


---

## Count Property

*Quelle: `POLYSIGNALLib~FunctionTypes~Count.html` · Polytec PolySignal Type Library · FunctionTypes Object : Count Property*

### Description

The number of enumerator values.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```
