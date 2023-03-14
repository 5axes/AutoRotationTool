# Auto Rotate Tool

Plugin Rotate Tool to get the automatic rotation on Right Clic 

The Auto Rotate Tool plugin is a fork of the [CuraOrientationPlugin ](https://github.com/nallath/CuraOrientationPlugin). However, it allows to add an access to the orientation functions from keyboard shortcuts and a contextual menu.

Short-cut :

	- Calculate fast optimal printing orientation : Ctrl+Shift+R
	- Calculate extended optimal printing orientation: Ctrl+Alt+R       
	- Rotate Side direction (X): Ctrl+Shift+X
	- Rotate Main direction (X): Ctrl+Alt+X
	- Reset rotation : Ctrl+Alt+I

The orientation plugin is a simple wrapper around the excellent STL-Tweaker by Christoph Schranz. It allows you to quickly calculate and apply the best printable orientation directly from Cura.

More info on his research can be found [here](https://www.researchgate.net/publication/311765131_Tweaker_-_Auto_Rotation_Module_for_FDM_3D_Printing)

## Plugin Function

### Calculate fast optimal printing orientation
The orientation function is a simple wrapper around the excellent STL-Tweaker by Christoph Schranz. It allows you to quickly calculate and apply the best printable orientation directly from Cura

### Calculate extended optimal printing orientation
It allows an extended calculation and orientation according to the best printable calculated orientation.

### Rotate main direction (X)
Rotate the selected element automatically on its main direction, parallel to the X axis of the plate.

### Rotate longest side (X)
Rotate the selected element automatically on its longest side, parallel to the X axis of the plate.

### Reset Rotation
Re-Init the selected Objects to their initial Orientation. Function similar to the Re-Init Button in the Rotation Tool Menu.


# YouTube video

[![Ultimaker Cura Plugin AutoRotationTool](http://img.youtube.com/vi/RFb83o0sQwY/0.jpg)](https://www.youtube.com/watch?v=RFb83o0sQwY)
