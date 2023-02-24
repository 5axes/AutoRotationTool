# Copyright (c) 2023 5@xes
# AutoRotationTool is released under the terms of the AGPLv3 or higher.

from . import AutoRotationTool

def getMetaData():
    return {}

def register(app):
    return {"extension": AutoRotationTool.AutoRotationTool()}
