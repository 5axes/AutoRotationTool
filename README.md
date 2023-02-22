# Auto Rotate Tool

Plugin Rotate Tool to get the automatic rotation on Right Clic 

The Auto Rotate Tool plugin is a copy of the [CuraOrientationPlugin ](https://github.com/5axes/CuraOrientationPlugin). However, it allows to add an access to the orientation functions from keyboard shortcuts and a contextual menu.

Short-cut :

	- Calculate fast optimal printing orientation : Ctrl+Shift+R
	- Calculate extended optimal printing orientation: Ctrl+Alt+R       
	- Rotate main direction (X): Ctrl+Alt+X

The orientation plugin is a simple wrapper around the excellent STL-Tweaker by Christoph Schranz. It allows you to quickly calculate and apply the best printable orientation directly from Cura.

More info on his research can be found [here](https://www.researchgate.net/publication/311765131_Tweaker_-_Auto_Rotation_Module_for_FDM_3D_Printing)

## Plugin Function

### Calculate fast optimal printing orientation
The orientation function is a simple wrapper around the excellent STL-Tweaker by Christoph Schranz. It allows you to quickly calculate and apply the best printable orientation directly from Cura

### Calculate extended optimal printing orientation
It allows an extended calculation and orientation according to the best printable calculated orientation.

### Rotate main direction (X)
Rotate the selected element automaticaly on its longest side, parallel to the X axis of the plate.