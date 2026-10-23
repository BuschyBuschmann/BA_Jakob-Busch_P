# POLYPROPERTIESLib – PTSClippingPlaneSettings

## PTSClippingPlaneSettings UDT

*Quelle: `POLYPROPERTIESLib~PTSClippingPlaneSettings.html` · Polytec PolyProperties Type Library*

### Description

The settings for the clipping plane functionality.

### UDT Members

| Member | Type | Description |
|---|---|---|
| m_lengthUnit | PTCLengthUnit | The length unit to be used for the display of the absolute position of the clipping planes in the clipping plane configuration dialog. |
| m_settingFar | PTSClippingPlaneSetting | The settings for the clipping plane denoted by ptcClippingPlaneFar . |
| m_settingMaxX | PTSClippingPlaneSetting | The settings for the clipping plane denoted by ptcClippingPlaneMaxX . |
| m_settingMaxY | PTSClippingPlaneSetting | The settings for the clipping plane denoted by ptcClippingPlaneMaxY . |
| m_settingMaxZ | PTSClippingPlaneSetting | The settings for the clipping plane denoted by ptcClippingPlaneMaxZ . |
| m_settingMinX | PTSClippingPlaneSetting | The settings for the clipping plane denoted by ptcClippingPlaneMinX . |
| m_settingMinY | PTSClippingPlaneSetting | The settings for the clipping plane denoted by ptcClippingPlaneMinY . |
| m_settingMinZ | PTSClippingPlaneSetting | The settings for the clipping plane denoted by ptcClippingPlaneMinZ . |
| m_settingNear | PTSClippingPlaneSetting | The settings for the clipping plane denoted by ptcClippingPlaneNear . |

### Remarks

The length unit stored in m_lengthUnit is also used to determine the step increment for the adjustment of the clipping plane positions by the controls in the clipping plane configuration dialog.
