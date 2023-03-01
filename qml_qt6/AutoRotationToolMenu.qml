// Copyright (c) 2023 5@xes
// Cura is released under the terms of the LGPLv3 or higher.

import QtQuick 2.1

import UM 1.2 as UM
import Cura 1.0 as Cura

Cura.Menu
{
    Cura.Menu
    {
        id: rotateToolMenu

        title: catalog.i18nc("@item:inmenu", "Rotation Tools")

        Cura.MenuItem
		{
			text: catalog.i18nc("@item:inmenu", "Calculate fast optimal printing orientation")
			shortcut: "Ctrl+Shift+R"
			enabled: UM.Selection.hasSelection
			onTriggered: manager.doFastAutoOrientation()
		}
        Cura.MenuItem
		{
			text: catalog.i18nc("@item:inmenu", "Calculate extended optimal printing orientation")
			enabled: UM.Selection.hasSelection
			shortcut: "Ctrl+Alt+R"
			onTriggered: manager.doExtendedAutoOrientation()
		}
        Cura.MenuItem
        {
            text: catalog.i18nc("@item:inmenu", "Rotate side direction (X)")
            enabled: UM.Selection.hasSelection
			shortcut: "Ctrl+Shift+X"
            onTriggered: manager.rotateSideDirection()
        }		
        Cura.MenuItem
        {
            text: catalog.i18nc("@item:inmenu", "Rotate main direction (X)")
            enabled: UM.Selection.hasSelection
			shortcut: "Ctrl+Alt+X"
            onTriggered: manager.rotateMainDirection()
        }
        Cura.MenuItem
        {
            text: catalog.i18nc("@item:inmenu", "Reset Rotation")
            enabled: UM.Selection.hasSelection
			shortcut: "Ctrl+Alt+I"
            onTriggered: manager.resetRotation()
        }			
    }
    Cura.MenuSeparator
    {
        id: rotateToolSeparator
    }

    function moveToContextMenu(contextMenu)
    {
        contextMenu.insertItem(0, rotateToolSeparator)
        contextMenu.insertMenu(0, rotateToolMenu)
    }

    UM.I18nCatalog { id: catalog; name: "autorotationtool" }
}
