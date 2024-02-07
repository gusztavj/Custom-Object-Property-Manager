# T1nk-R's Custom Object Property Manager add-on for Blender
# - part of T1nk-R Utilities for Blender
#
# Version: Please see the version tag under bl_info below.
#
# This module is responsible for managing add-on and settings lifecycle.
#
# Module and add-on authored by T1nk-R (https://github.com/gusztavj/)
#
# PURPOSE & USAGE *****************************************************************************************************************
# You can use this add-on to add, edit and remove custom object properties for specific objects or in batches.
#
# Help, support, updates and anything else: https://github.com/gusztavj/Custom-Object-Property-Manager
#
# COPYRIGHT ***********************************************************************************************************************
#
# ** MIT License **
# 
# Copyright (c) 2023-2024, T1nk-R (Gusztáv Jánvári)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
# ** Commercial Use **
# 
# I would highly appreciate to get notified via [janvari.gusztav@imprestige.biz](mailto:janvari.gusztav@imprestige.biz) about 
# any such usage. I would be happy to learn this work is of your interest, and to discuss options for commercial support and 
# other services you may need.
#
# DISCLAIMER **********************************************************************************************************************
# This add-on is provided as-is. Use at your own risk. No warranties, no guarantee, no liability,
# no matter what happens. Still I tried to make sure no weird things happen:
#   * This add-on may add and delete custom object properties based on your instructions.
#   * This add-on is not intended to modify your objects and other Blender assets in any other way.
#   * You shall be able to simply undo consequences made by this add-on.
#
# You may learn more about legal matters on page https://github.com/gusztavj/Custom-Object-Property-Manager
#
# *********************************************************************************************************************************

# Blender add-on identification ===================================================================================================
bl_info = {
    "name": "T1nk-R Custom Object Property Manager (T1nk-R Utilities)",
    "author": "T1nk-R (GusJ)",
    "version": (1, 1, 1),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar (N) > T1nk-R Utils",
    "description": "You can use this add-on to add, edit and remove custom object properties in batches.",
    "category": "Object",
    "doc_url": "https://github.com/gusztavj/Custom-Object-Property-Manager",
}

# Lifecycle management ############################################################################################################

# Reimport libraries to make sure everything is up to date
if "bpy" in locals():
    from importlib import reload

    # Our own libraries
    libs = [updateChecker, decorator, decoratorworker]
    
    for lib in libs:        
        try:
            reload(lib)
        except:
            pass
    
    del reload

# Library imports -----------------------------------------------------------------------------------------------------------------
import bpy
from . import updateChecker
from . import decorator
from . import decoratorworker

# Properties ######################################################################################################################

classes = [
    updateChecker.T1nkerDecoratorUpdateInfo,
    updateChecker.T1NKER_OT_DecoratorUpdateChecker,
    decorator.T1nkerDecoratorAddonPreferences,
    decorator.DecoratorSettings,    
    decorator.DecoratorPanel,
    decorator.OBJECT_OT_DecoratorAdd,
    decorator.OBJECT_OT_DecoratorExtend,
    decorator.OBJECT_OT_DecoratorReset,
    decorator.OBJECT_OT_DecoratorRemove
]
"""
List of classes that need to be registered by Blender
"""

# Functions #######################################################################################################################

# Register the plugin -------------------------------------------------------------------------------------------------------------
def register():
    """
    Register classes and create add-on specific settings upon enabling the add-on. Settings are created in the current scene of 
    your Blender file and therefore travel with your file.
    """
    
    # Make sure to avoid double registration
    unregister()
    
    # Register classes
    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.types.Scene.decoratorSettings = bpy.props.PointerProperty(type=decorator.DecoratorSettings)


# Unregister the add-on -----------------------------------------------------------------------------------------------------------
def unregister():
    """
    Unregister everything that have been registered upon disabling the add-on.
    """
    
    # Delete settings
    
    try:
        del bpy.types.Scene.decoratorSettings
    except:
        # Don't panic, it was not added either
        pass

    # Unregister classes (in reverse order)
    for c in reversed(classes):
        try:
            bpy.utils.unregister_class(c)
        except:
            # Don't panic, it was not registered at all
            pass

# Run w/o installation ############################################################################################################
# Let you run registration without installing.
if __name__ == "__main__":
    register()
