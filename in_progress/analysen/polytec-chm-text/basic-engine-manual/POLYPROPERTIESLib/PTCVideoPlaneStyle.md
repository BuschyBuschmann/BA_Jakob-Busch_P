# POLYPROPERTIESLib – PTCVideoPlaneStyle

## PTCVideoPlaneStyle Enumeration

*Quelle: `POLYPROPERTIESLib~PTCVideoPlaneStyle.html` · Polytec PolyProperties Type Library*

### Description

The style for displaying the video planes in the 3D view.

### Members

| Member | Value | Description |
|---|---|---|
| ptcVideoPlaneStyleAll | 2 | All video planes are displayed. |
| ptcVideoPlaneStyleNone | 0 | No video plane is displayed. |
| ptcVideoPlaneStyleSelected | 1 | All video planes associated with all selected scan points are displayed in their full extension. This option is targeted at combined files which contain multiple video planes. For non-combined files with a single video plane, this option has the same effect as the option ptcVideoPlaneStyleAll except for the special case that no scan point is selected, where with ptcVideoPlaneStyleSelected the video plane is hidden. |
