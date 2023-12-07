# Trainz Batch Export - ComplExport
#
# COPYRIGHT **************************************************************************************************
# Creative Commons CC-BY-SA. Simply to put, you can create derivative works based on this script,
# and if you are nice, you don't remove the following attribution:
#
# Original script created by: T1nk-R - na.mondhatod@gmail.com
# Version 2020-01-15
#
# DISCLAIMER *************************************************************************************************
# This script is provided as-is. Use at your own risk. No warranties, no guarantee, no liability,
# no matter what happens. Still I tried to make sure no weird things happen.
#
# USAGE ******************************************************************************************************
# This script lets you define what objects you want to export as one FBX file. This is called an artifact. 
# You can define as many artifacts as you can, each may consists of any number of objects.
#
# Files are saved in the folder computed like this: the folder containing your Blender file combined
# with the subfolder name or relative path specified in variable subfolder below.
#
# The script saves and restores your selections and the visibility of objects.
#
# Form of definition: 
# 1. Scroll down to the line beginning with 'deliverables'.
# 2. Compile your first artifact.
#       * Each line corresponds to an artifact.
#       * The first item is the name of the FBX file.
#       * The second item is a list of object names. Include the objects you want to export to this FBX file.
# 3. Add as many artifacts as you want.
# 4. Run the script.
#
#
# Example configuration
#
#   deliverables = [
#       ['file01',  ['object-A-1',   'object-B-1',   'object-C-1']],
#       ['file02',  ['object-A-2',   'object-B-1',   'suspension-lod0']]
#   ]
#
#  This will create file01.fbx and file02.fbx in the folder hosting your Blender file. 
#  * file01 will contain the objects named object-A-1, object-B-1 and object-C-1
#  * file02 will contain the objects named object-A-2 and object-B-1
#
#
#  #    # Define the mesh compilation, file name comes first, then the mesh names
#    deliverables = [
#        ['<uvCode>gadget1',   ['handler-plate', 'Cone']]
#    ]

#    # In the form of <uvCode>, substring from object name, uv map name
#    uvCombinations = [
#        ['st01', [['handler-plate',      'UVMap1'],   ['Cone',     'UVMap1']]],
#        ['st02', [['handler-plate',      'UVMap3'],   ['Cone',     'UVMap2']]]
#    ]
    # **********************************************************************************************************

#

bl_info = {
    "name": "T1nk-R Trainz Exporter",
    "author": "GusJ",
    "version": (1, 0),
    "blender": (2, 91, 0),
    "location": "File > Export",
    "description": "Export compilations of objects with various UV layers to FBX files for Trainz 2019.",
    "category": "Import-Export",
    "doc_url": "Yet to come, till that just drop a mail to Gus at na.mondhatod@gmail.com",
}

if "bpy" in locals():
    from importlib import reload
    try:
        reload(exporter)
    except:
        pass
    
    try:
        reload(decorator)
    except:
        pass
    
    try:
        reload(decoratorworker)
    except:
        pass
    
    del reload

import bpy
from . import exporter
from . import decorator
from . import decoratorworker

# Store keymaps here to access after registration
addon_keymaps = []

# Register menu item  "Export Compilations to Trainz" under File > Export  
def menu_export(self, context):
    self.layout.operator(exporter.OBJECT_OT_TrainzExporter.bl_idname)


# Class registry
classes = [
    exporter.TrainzExporterAddonSettings, 
    exporter.TrainzExporterAddonPreferences, 
    exporter.OBJECT_OT_TrainzExporter,
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
    
    # Add menu command to File > Export
    bpy.types.TOPBAR_MT_file_export.append(menu_export)

    # Set CTRL+SHIFT+Y as shortcut
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(exporter.OBJECT_OT_TrainzExporter.bl_idname, 'Y', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))

# Unregister the add-on
def unregister():
    
    # Unregister key mapping
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except:
            # Don't panic, it was not added either
            pass
        
    addon_keymaps.clear()
    
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
    
    try:
        # Delete menu item
        bpy.types.TOPBAR_MT_file_export.remove(menu_export)  
    except:
        # Don't panic, it was not added at all
        pass

# Let you run registration without installing. You'll find the command in File > Export
if __name__ == "__main__":
    register()
