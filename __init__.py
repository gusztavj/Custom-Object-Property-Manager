# T1nk-R's Custom Object Property Manager
# - part of T1nk-R Utilities for Blender
#
# COPYRIGHT **************************************************************************************************
# Creative Commons CC-BY-SA. Simply to put, you can create derivative works based on this script,
# and if you are nice, you don't remove the following attribution:
#
#       Original addon created by: T1nk-R - na.mondhatod@gmail.com
#
# Version 1.0.1 @ 2023-12-07
#
# DISCLAIMER *************************************************************************************************
# This script is provided as-is. Use at your own risk. No warranties, no guarantee, no liability,
# no matter what happens. Still I tried to make sure no weird things happen.
#
# USAGE ******************************************************************************************************
# You can use this add-on to add, edit and remove custom object properties in batches.
#
# Help, support, updates and anything else: https://github.com/gusztavj/Custom-Object-Property-Manager
#
# ************************************************************************************************************


bl_info = {
    "name": "T1nk-R's Custom Object Property Manager",
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
