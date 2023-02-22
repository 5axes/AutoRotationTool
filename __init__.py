# Copyright (c) 2023 5@xes
# AutoRotateTool is released under the terms of the AGPLv3 or higher.

from . import AutoRotateTool

def getMetaData():
    return {}

def register(app):
    return {"extension": AutoRotateTool.AutoRotateTool()}
