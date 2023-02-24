// Copyright (c) 2023 5@xes
// Cura is released under the terms of the LGPLv3 or higher.

import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.2
import QtQuick.Window 2.1

import UM 1.2 as UM
import Cura 1.0 as Cura

Menu
{
    id: base
    
	title: catalog.i18nc("@item:inmenu", "Rotate Tool")
	
    MenuItem
    {
        text: catalog.i18nc("@item:inmenu", "Calculate fast optimal printing orientation")
        enabled: UM.Selection.hasSelection
        onTriggered: manager.doFastAutoOrientation()
    }
    MenuItem
    {
        text: catalog.i18nc("@item:inmenu", "Calculate extended optimal printing orientation")
        enabled: UM.Selection.hasSelection
        onTriggered: manager.doExtendedAutoOrientation()
    }
    MenuItem
    {
        text: catalog.i18nc("@item:inmenu", "Rotate side direction (X)")
        enabled: UM.Selection.hasSelection
        onTriggered: manager.rotateSideDirection()
    }	
    // MenuItem
    // {
    //    text: catalog.i18nc("@item:inmenu", "Rotate main direction (X)")
    //    enabled: UM.Selection.hasSelection
    //    onTriggered: manager.rotateMainDirection()
    //}
	MenuItem
    {
        text: catalog.i18nc("@item:inmenu", "Reinit Rotation")
        enabled: UM.Selection.hasSelection
        onTriggered: manager.resetRotation()
    }
    function moveToContextMenu(contextMenu)
    {
        for(var i in base.items)
        {
            contextMenu.items[0].insertItem(i,base.items[i])
        }
    }

    UM.I18nCatalog { id: catalog; name: "autorotation
	tool" }
}
