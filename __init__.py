# T1nk-R's Custom Object Property Manager add-on for Blender
# - part of T1nk-R Utilities for Blender
#
# This module responsible for managing add-on and settings lifecycle.
#
# Module and add-on authored by T1nk-R (https://github.com/gusztavj/)
#
# PURPOSE & USAGE *****************************************************************************************************************
# You can use this add-on to add, edit and remove custom object properties for specific objects or in batches.
#
# Help, support, updates and anything else: https://github.com/gusztavj/Custom-Object-Property-Manager
#
# COPYRIGHT ***********************************************************************************************************************
# Creative Commons CC BY-NC-SA:
#       This license enables re-users to distribute, remix, adapt, and build upon the material in any medium 
#       or format for noncommercial purposes only, and only so long as attribution is given to the creator. 
#       If you remix, adapt, or build upon the material, you must license the modified material under 
#       identical terms. CC BY-NC-SA includes the following elements:
#           BY: credit must be given to the creator.
#           NC: Only noncommercial uses of the work are permitted.
#           SA: Adaptations must be shared under the same terms.
#
#       Credit text:
#           Original addon created by: T1nk-R - janvari.gusztav@imprestige.biz
#
#       For commercial use, please contact me via janvari.gusztav@imprestige.biz. Don't be scared of
#       rigid contracts and high prices, above all I just want to know if this work is of your interest,
#       and discuss options for commercial support and other services you may need.
#
#
# Version: Please see the version tag under bl_info below.
#
# DISCLAIMER **********************************************************************************************************************
# This add-on is provided as-is. Use at your own risk. No warranties, no guarantee, no liability,
# no matter what happens. Still I tried to make sure no weird things happen:
#   * This add-on may add and delete custom object properties based on your instructions.
#   * This add-on is not intended to modify your objects and other Blender assets in any other way.
#
# You may learn more about legal matters on page https://github.com/gusztavj/Custom-Object-Property-Manager
#
# *********************************************************************************************************************************


bl_info = {
    "name": "T1nk-R Custom Object Property Manager",
    "author": "T1nk-R (GusJ)",
    "version": (1, 0, 1),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar (N) > T1nk-R Utils",
    "description": "You can use this add-on to add, edit and remove custom object properties in batches.",
    "category": "Object",
    "doc_url": "https://github.com/gusztavj/Custom-Object-Property-Manager",
}

if "bpy" in locals():
    from importlib import reload

    libs = [decorator, decoratorworker]
    
    for lib in libs:        
        try:
            reload(lib)
        except:
            pass
    
    del reload

import bpy
from . import decorator
from . import decoratorworker


# Class registry
classes = [
    decorator.DecoratorSettings,
    decorator.DecoratorPanel,
    decorator.OBJECT_OT_DecoratorAdd,
    decorator.OBJECT_OT_DecoratorExtend,
    decorator.OBJECT_OT_DecoratorReset,
    decorator.OBJECT_OT_DecoratorRemove
]

# Register the plugin
def register():
    
    # Make sure to avoid double registration
    unregister()
    
    # Register classes
    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.types.Scene.decoratorSettings = bpy.props.PointerProperty(type=decorator.DecoratorSettings)


# Unregister the add-on
def unregister():
    
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
    
# Let you run registration without installing. You'll find the command in File > Export
if __name__ == "__main__":
    register()
