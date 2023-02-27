#
# Copyright (c) 2023 5@xes
# AutoRotationTool is released under the terms of the AGPLv3 or higher.
# AutoRotationTool plugin is a simple wrapper around the excellent OrientationPlugin of Nallah
# https://github.com/nallath/CuraOrientationPlugin
# Original Source for Auto Orientation : https://github.com/iot-salzburg/STL-tweaker
# Post on Cura : https://community.ultimaker.com/topic/16037-3d-object-auto-rotate-plugin-for-cura-1504-23
# Tweaker_-_Auto_Rotation_Module_for_FDM_3D_Printing : https://www.researchgate.net/publication/311765131_Tweaker_-_Auto_Rotation_Module_for_FDM_3D_Printing
#

import os
import numpy
import trimesh

VERSION_QT5 = False
try:
    from PyQt6.QtCore import pyqtSlot, QObject
except ImportError:
    from PyQt5.QtCore import pyqtSlot, QObject
    VERSION_QT5 = True

from typing import Optional, List, Dict

from cura.CuraApplication import CuraApplication

from UM.Extension import Extension
from UM.Message import Message
from UM.Logger import Logger
from UM.Version import Version

from UM.Scene.Selection import Selection
from UM.Scene.SceneNode import SceneNode
from UM.Operations.GroupedOperation import GroupedOperation
from UM.Resources import Resources

from UM.Math.Plane import Plane
from UM.Math.Quaternion import Quaternion
from UM.Math.Vector import Vector

from UM.Operations.SetTransformOperation import SetTransformOperation

from UM.Math.Vector import Vector
from UM.Math.Matrix import Matrix

from UM.i18n import i18nCatalog

from .CalculateOrientationJob import CalculateOrientationJob
# Origine Source Code from [FieldOfView ](https://github.com/fieldOfView) 
from .SetTransformMatrixOperation import SetTransformMatrixOperation

Resources.addSearchPath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)))
)  # Plugin translation file import

catalog = i18nCatalog("autorotationtool")

if catalog.hasTranslationLoaded():
    Logger.log("i", "Auto Rotation Tool Plugin translation loaded!")
    
class AutoRotationTool(Extension, QObject,):
    def __init__(self, parent = None) -> None:
        QObject.__init__(self, parent)
        Extension.__init__(self)

        self._application = CuraApplication.getInstance()

        self._qml_folder = "qml_qt6" if not VERSION_QT5 else "qml_qt5"

        self._application.engineCreatedSignal.connect(self._onEngineCreated)
        
        self._extended_mode = False

        self.addMenuItem(catalog.i18nc("@item:inmenu", "Calculate fast optimal printing orientation"), self.doFastAutoOrientation)
        self.addMenuItem(catalog.i18nc("@item:inmenu", "Calculate extended optimal printing orientation"), self.doExtendedAutoOrientation)
        
        self.addMenuItem(catalog.i18nc("@item:inmenu", "Rotate side direction (X)"), self.rotateSideDirection)
        # Issue with trimesh.bounds.oriented_bounds_2D in release 4.X for Trimesh
        if not VERSION_QT5:        
            self.addMenuItem(catalog.i18nc("@item:inmenu", "Rotate main direction (X)"), self.rotateMainDirection)
        
        self.addMenuItem(catalog.i18nc("@item:inmenu", "Reinit Rotation"), self.resetRotation)

        self._message = Message(title=catalog.i18nc("@info:title", "Auto Rotate Tool"))
        self._additional_menu = None  # type: Optional[QObject]

    # Origine Source Code from [FieldOfView ](https://github.com/fieldOfView)   
    def _onEngineCreated(self) -> None:
        # To add items to the ContextMenu, we need access to the QML engine
        # There is no way to access the context menu directly, so we have to search for it
        main_window = self._application.getMainWindow()
        if not main_window:
            return

        context_menu = None
        for child in main_window.contentItem().children():
            try:
                if not VERSION_QT5:
                    test = child.handleVisibility # With QtQuick Controls 2, ContextMenu is the only item that has a findItemIndex function in the main window root contentitem
                else:
                    test = child.findItemIndex  # With QtQuick Controls 1, ContextMenu is the only item that has a findItemIndex function
                context_menu = child
                break
            except:
                pass

        if not context_menu:
            Logger.log("w", "Could not find the viewport context menu")
            return

        Logger.log("d", "Inserting item in context menu")
        qml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self._qml_folder, "AutoRotationToolMenu.qml")
        self._additional_menu = self._application.createQmlComponent(qml_path, {"manager": self})
        if not self._additional_menu:
            return

        if VERSION_QT5:
            context_menu.insertSeparator(0)
            context_menu.insertMenu(0, catalog.i18nc("@info:title", "Auto Rotate Tool"))

        # Move additional menu items into context menu
        self._additional_menu.moveToContextMenu(context_menu)

    def _getSelectedNodes(self, force_single = False) -> List[SceneNode]:
        self._message.hide()
        selected = Selection.getAllSelectedObjects()[:]
        if force_single:
            if len(selected) == 1:
                return selected[:]

            self._message.setText(catalog.i18nc("@info:status", "Please select a single model first"))
        else:
            if len(selected) >= 1:
                return selected[:]

            self._message.setText(catalog.i18nc("@info:status", "Please select one or more models first"))

        self._message.show()
        return []

    def _getAllSelectedNodes(self) -> List[SceneNode]:
        self._message.hide()
        selected = Selection.getAllSelectedObjects()[:]
        if selected:
            deep_selection = []  # type: List[SceneNode]
            for selected_node in selected:
                if selected_node.hasChildren():
                    deep_selection = deep_selection + selected_node.getAllChildren()
                if selected_node.getMeshData() != None:
                    deep_selection.append(selected_node)
            if deep_selection:
                return deep_selection

        self._message.setText(catalog.i18nc("@info:status", "Please select one or more models first"))
        self._message.show()

        return []          
 
    @pyqtSlot()
    def resetRotation(self) -> None:
        """Reset the orientation of the mesh(es) to their original orientation(s)"""

        Selection.applyOperation(SetTransformOperation, None, Quaternion(), None)
        
    @pyqtSlot()
    def rotateMainDirection(self) -> None:
        nodes_list = self._getSelectedNodes()
        if not nodes_list:
            return

        op = GroupedOperation()
        for node in nodes_list:
            mesh_data = node.getMeshData()
            if not mesh_data:
                continue
            
            hull_polygon = node.callDecoration("_compute2DConvexHull")
            # test but not sure in witch case we have this situation ?
            if not hull_polygon or hull_polygon.getPoints is None:
                Logger.log("w", "Object {} cannot be calculated because it has no convex hull.".format(node.getName()))
                continue

            points=hull_polygon.getPoints()
            # Get the Rotation Matrix     
            # Logger.log('d', "Points : \n{}".format(points))                  
            transform, rectangle = trimesh.bounds.oriented_bounds_2D(points)
            Logger.log('d', "Rotation : \n{}".format(transform)) 

            # Change Transfo data
            # Don't ask me Why just test and try not sure of the validity of oriented_bounds_2D by trimesh 
            t = Matrix()
            Vect = [transform[1][1],0,transform[0][1]]
            t.setColumn(0,Vect)
            Vect = [transform[1][0],0,transform[0][0]]
            t.setColumn(2,Vect)

            #local_transformation.setColumn(1,transform[1])
            local_transformation = Matrix()
            local_transformation.multiply(t)
            local_transformation.multiply(node.getLocalTransformation())  

            # Log for debugging and Analyse           
            Logger.log('d', "Local_transformation     :\n{}".format(node.getLocalTransformation())) 
            Logger.log('d', "TransformMatrixOperation :\n{}".format(local_transformation))   
            # By using this code rotate the Element but no Undo is possible via the Reinit rotation function
            # node.setTransformation(local_transformation)            
            op.addOperation(SetTransformMatrixOperation(node, local_transformation))

        op.push()

    @pyqtSlot()
    def rotateSideDirection(self) -> None:
        nodes_list = self._getSelectedNodes()
        if not nodes_list:
            return

        op = GroupedOperation()
        for node in nodes_list:
            mesh_data = node.getMeshData()
            if not mesh_data:
                continue
            
            hull_polygon = node.callDecoration("_compute2DConvexHull")
            # test but not sure in witch case we have this situation ?
            if not hull_polygon or hull_polygon.getPoints is None:
                Logger.log("w", "Object {} cannot be calculated because it has no convex hull.".format(node.getName()))
                continue
 
            points=hull_polygon.getPoints()

            # Init
            np = 0
            l_v = 0
            for point in points:
                # Logger.log('d', "p{} X : {} Y : {}".format(np,point[0],point[1]))
                if np>0 :                         
                    new_position = Vector(point[0], point[1], 0)
                    lg=new_position-first_pt
                    lght = lg.length()
                    if lght>l_v :
                        l_v = lght
                        s_lg=lg

                    first_pt=new_position
                else :
                    first_pt = Vector(point[0], point[1], 0)             
                np+=1
            
            # Last vector  to close the loop       
            lg=Vector(points[0][0], points[0][1], 0)-first_pt
            lght = lg.length()
            if lght>l_v :
                s_lg=lg
                # Logger.log('d', "s_lg on las point : {}".format(s_lg))
            
            vectX = (1, 0, 0)
            vectY = (0, 1, 0)
            anGl= self._angle_between(vectX,(s_lg.x, s_lg.y, 0))
            deganGl = anGl/numpy.pi*180
            
            # For debuging output the vector director and the Angle ( in radians and degree)
            Logger.log('d', "s_lg   : {}".format(s_lg))
            Logger.log('d', "Angle : {} Angle° : {}".format(anGl,deganGl)) 
            #Something done in the AutoRotationTool.py ... It's not very clear for me, but I still have to investigate this point
            dv=self._dot_vector(vectY,(s_lg.x, s_lg.y, 0))
            Logger.log('d', "Dot vector : {}".format(dv))  
            if dv > 0 :
                direction = 1
            else :
                direction = -1
                
            extents = mesh_data.getExtents()
            center = Vector(extents.center.x, extents.center.y, extents.center.z)

            # Get the Rotation Matrix
            rotation = Matrix()
            # setByRotationAxis or rotateByAxis ?  don't think there is a difference
            rotation.setByRotationAxis(direction*anGl, Vector(0, 1, 0))
            Logger.log('d', "Rotation                 :\n{}".format(rotation))
            
            # Change Transfo data
            local_transformation = Matrix()      
            local_transformation.multiply(rotation)
            local_transformation.multiply(node.getLocalTransformation()) 
            # Log for debugging and Analyse           
            Logger.log('d', "Local_transformation     :\n{}".format(node.getLocalTransformation())) 
            Logger.log('d', "TransformMatrixOperation :\n{}".format(local_transformation))   
            # By using this code rotate the Element but no Undo is possible via the Reinit rotation function
            # node.setTransformation(local_transformation)            
            op.addOperation(SetTransformMatrixOperation(node, local_transformation))

        op.push()
    
    def _unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / numpy.linalg.norm(vector)

    def _angle_between(self, v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::
        """

        v1_u = self._unit_vector(v1)
        v2_u = self._unit_vector(v2)
        
        angle = numpy.arccos(numpy.clip(numpy.dot(v1_u, v2_u), -1.0, 1.0))
     
        return angle
 
    def _dot_vector(self, v1, v2):
        """ Returns the scalar product between vectors 'v1' and 'v2'::
        """

        v1_u = self._unit_vector(v1)
        v2_u = self._unit_vector(v2)
        
        dotv = numpy.dot(v1_u, v2_u)
     
        return dotv

    @pyqtSlot()
    def doFastAutoOrientation(self):
        self._extended_mode=False    
        self.doAutoOrientation(False)
    @pyqtSlot()
    def doExtendedAutoOrientation(self):
        self._extended_mode=True    
        self.doAutoOrientation(True)

    def doAutoOrientation(self, extended_mode):
        # If we still had a message open from last time, hide it.
        if self._message:
            self._message.hide()

        selected_nodes = Selection.getAllSelectedObjects()
        if len(selected_nodes) == 0:
            self._message = Message(catalog.i18nc("@info:status", "No objects selected to orient. Please select one or more objects and try again."), title = catalog.i18nc("@title", "Auto Rotate Tool"))
            self._message.show()
            return

        message = Message(catalog.i18nc("@info:status", "Calculating the optimal orientation..."), 0, False, -1, title = catalog.i18nc("@title", "Auto Rotate Tool"))
        message.show()

        job = CalculateOrientationJob(selected_nodes, extended_mode = extended_mode, message = message)
        job.finished.connect(self._onFinished)
        job.start()

    def _onFinished(self, job):
        if self._message:
            self._message.hide()

        if job.getMessage() is not None:
            job.getMessage().hide()
            if self._extended_mode :
                _text = catalog.i18nc("@info:status", "All selected objects have been oriented using the extended mode.")
            else :
                _text = catalog.i18nc("@info:status", "All selected objects have been oriented.")
            self._message = Message(_text, title=catalog.i18nc("@title", "Auto Rotate Tool"), message_type = Message.MessageType.POSITIVE)
            self._message.show()