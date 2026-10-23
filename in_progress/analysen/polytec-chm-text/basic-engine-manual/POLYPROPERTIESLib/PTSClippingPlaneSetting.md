# POLYPROPERTIESLib – PTSClippingPlaneSetting

## PTSClippingPlaneSetting UDT

*Quelle: `POLYPROPERTIESLib~PTSClippingPlaneSetting.html` · Polytec PolyProperties Type Library*

### Description

The settings for a clipping plane.

### UDT Members

| Member | Type | Description |
|---|---|---|
| m_active | Boolean | Specifies whether the clipping plane is enabled. |
| m_positionBoxSizeRatio | Double | Relative position of the clipping plane, see the explanation below. |

### Remarks

The relative position of the clipping plane is given as the ratio of the plane position relative to the center of the bounding box of the full geometry and half the extension of the bounding box in the direction which the plane refers to.

### Example

If for the clipping plane denoted by ptcClippingPlaneMinX the parameter m_positionBoxSizeRatio is equal to -0.7, then the plane is located to the left of the center of the bounding box of the geometry, at a distance equal to 70 % of half the width of the bounding box, assuming that the x-axis goes from the left to the right.
