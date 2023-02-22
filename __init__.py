# Copyright (c) 2023 5@xes
# RotateTool is released under the terms of the AGPLv3 or higher.

from . import RotateTool

def getMetaData():
    return {}

def register(app):
    return {"extension": RotateTool.RotateTool()}
