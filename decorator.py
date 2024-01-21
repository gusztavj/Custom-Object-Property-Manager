# T1nk-R's Custom Object Property Manager add-on for Blender
# - part of T1nk-R Utilities for Blender
#
# This module contains the presentation layer of the add-on
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
#   * You shall be able to simply undo consequences made by this add-on.
#
# You may learn more about legal matters on page https://github.com/gusztavj/Custom-Object-Property-Manager
#
# *********************************************************************************************************************************



import bpy
from bpy.props import StringProperty, BoolProperty
from . import decoratorworker

class DecoratorSettings(bpy.types.PropertyGroup):
    
    # Properties ==================================================================================================================

    # Controls whether to process selected objects or all 
    affectSelectedObjectsOnly: BoolProperty(
        name="Only process selected objects",
        description="If unchecked, it will process all of your visible objects",
        default=False
    )
    """
    Controls whether to process selected objects or all.
    """
    
    # The name of the property to add or remove
    propertyName: StringProperty(
        name="Property Name",
        description="Specify the name of the property to add or remove",
        default="Hide at Lod Level"
    )    
    """
    The name of the property to add or remove.
    """
    
    # The name of the property to add or remove
    propertyValue: StringProperty(
        name="Property Value",
        description="The default value to set for the property (only if the property does not exist)",
        default=""
    )    
    """
    The name of the property to add or remove.
    """

    # Controls log verbosity.
    isVerbose: BoolProperty(
        name="Verbose mode",
        description="Check to get a detailed log on what happened and what not. Non-verbose mode only reports what actually happened.",
        default=False
    )
    """
    Controls log verbosity.
    """
    
    # Controls if actions are actually taken or just simulated.
    isTestOnly: BoolProperty(        
        name="Just a test", 
        description="Don't do anything, just show what you would do",
        default=False
    )    
    """
    Controls if actions are actually taken or just simulated.
    """
    



# Control panel to show in Blender's viewport, in the 'N' toolbar =================================================================
class DecoratorPanel(bpy.types.Panel):
    """Control panel to show in Blender's viewport, in the 'N' toolbar
    """
    # Blender-specific stuff
    bl_idname = "OBJECT_PT_t1nker_decorator_panel"
    bl_label = "T1nk-R Custom Object Properties (T1nk-R Utilities)"
    bl_description = "Add, edit or remove custom object properties"
    bl_location = "3D View -> Sidebar"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "T1nk-R Utils"  # this is going to be the name of the tab

    # Draw the panel  =============================================================================================================  
    def draw(self, context: bpy.types.Context):
        """Draws the panel.

        Args:
            context (Context): A bpy.context object passed by Blender.
        """
        
        # Store the settings in a shorthand variable
        self.settings = context.scene.decoratorSettings
        
        # We'll create boxes with rows for the various settings
        
        layout = self.layout
        
        
        
        box = layout.box()
                    
        row = box.row(align=True)
        row.label(text="Select scope")
        
        row = box.row(align=True)
        row.prop(self.settings, "affectSelectedObjectsOnly")
        
        
        
        box = layout.box()
                
        row = box.row(align=True)
        row.label(text="Property to add or remove")
        
        row = box.row(align=True)
        row.prop(self.settings, "propertyName")
        
        row = box.row(align=True)
        row.label(text="Type: String (others may be supported in the future)")

        row = box.row(align=True)
        row.prop(self.settings, "propertyValue")
        
        box = layout.box()
        
        row = box.row(align=True)
        row.label(text="Select operation mode") 
        
        row = box.row(align=True)
        row.prop(self.settings, "isVerbose")  
        
        row = box.row(align=True)
        row.prop(self.settings, "isTestOnly")  



        box = layout.box()
        
        row = box.row(align=True)
        row.label(text="Take action")
        
        row = box.row(align=True)
        col = row.column(align=True)
        
        col.label(text="Add property or reset value")
        col.label(text="Add if doesn't exist, don't reset")
        col.label(text="Reset value if exists")        
        col.label(text="Remove property")        
        
        col = row.column(align=True)
        col.operator("t1nker.object_property_manager_add", text="Set", icon="ADD")
        col.operator("t1nker.object_property_manager_extend", text="Extend", icon="FULLSCREEN_ENTER")
        col.operator("t1nker.object_property_manager_reset", text="Reset", icon="FILE_REFRESH")        
        col.operator("t1nker.object_property_manager_remove", text="Remove", icon="REMOVE")
        

# Operator to add a custom object property with a custom default value
class OBJECT_OT_DecoratorAdd(bpy.types.Operator):    
    """Add the custom object property to objects. If the property exists for an object, its value will be reset to the value specified above"""
    bl_idname = "t1nker.object_property_manager_add"
    bl_label = "Add custom object property"
    bl_options = {'REGISTER', 'UNDO'}    
    
    # Operator settings
    settings : DecoratorSettings = None        

    # Lifecycle management ========================================================================================================
    def __init__(self):
        self.log = None
        self.settings = DecoratorSettings(self)
    
    # See if the operation can run ================================================================================================
    @classmethod
    def poll(cls, context):
        # Return true if the current Blend file is saved and we are in object mode, not in some edit mode 
        # (being in a non-object mode would prevent creating doubles of objects for pre-export manipulation)
        return context.mode == 'OBJECT'
    
    # Here is the core stuff ======================================================================================================
    def execute(self, context): 
        """Execute the operator
        """                     
        
        # We just need to run the worker with the context and the proper operation mode (addition here)
        
        dw = decoratorworker.DecoratorWorker()
        opResult = dw.processObjects(context = context, action = decoratorworker.DecoratorWorkerModes.Add)
        
        return opResult
    
# Operator to add a custom object property with a custom default value
class OBJECT_OT_DecoratorExtend(bpy.types.Operator):    
    """Add the custom object property to objects currently not having it. If the property exists for an object, its value won't be changed"""
    bl_idname = "t1nker.object_property_manager_extend"
    bl_label = "Extend custom object property"
    bl_options = {'REGISTER', 'UNDO'}    
    
    # Operator settings
    settings : DecoratorSettings = None        

    # Lifecycle management ========================================================================================================
    def __init__(self):
        self.log = None
        self.settings = DecoratorSettings(self)
    
    # See if the operation can run ================================================================================================
    @classmethod
    def poll(cls, context):
        # Return true if the current Blend file is saved and we are in object mode, not in some edit mode 
        # (being in a non-object mode would prevent creating doubles of objects for pre-export manipulation)
        return context.mode == 'OBJECT'
    
    # Here is the core stuff ======================================================================================================
    def execute(self, context): 
        """Execute the operator
        """                     
        
        # We just need to run the worker with the context and the proper operation mode (addition here)
        
        dw = decoratorworker.DecoratorWorker()
        opResult = dw.processObjects(context = context, action = decoratorworker.DecoratorWorkerModes.Extend)
        
        return opResult
    
# Operator to remove a custom object property
class OBJECT_OT_DecoratorReset(bpy.types.Operator):    
    """Reset the custom object property to the value specified above. Only objects having this property will be affected. If an object does not have this property now, it won't be added"""
    bl_idname = "t1nker.object_property_manager_reset"
    bl_label = "Reset custom object property"
    bl_options = {'REGISTER', 'UNDO'}    
    
    # Operator settings
    settings : DecoratorSettings = None        

    # Lifecycle management ========================================================================================================
    def __init__(self):
        self.log = None
        self.settings = DecoratorSettings(self)
    
    # See if the operation can run ================================================================================================
    @classmethod
    def poll(cls, context):
        # Return true if the current Blend file is saved and we are in object mode, not in some edit mode 
        # (being in a non-object mode would prevent creating doubles of objects for pre-export manipulation)
        return context.mode == 'OBJECT'
    
    # Show the export dialog ======================================================================================================
    def invoke(self, context, event):
        
        # For first run in the session, load addon defaults (otherwise use values set previously in the session)
        if self.settings is None:
            self.settings = context.preferences.addons[__package__].preferences.settings

        # Show export dialog
        result = context.window_manager.invoke_props_dialog(self, width=400)
        
        return result

    # Here is the core stuff ======================================================================================================
    def execute(self, context): 
        """Execute the operator
        """                     
        # We just need to run the worker with the context and the proper operation mode (removal here)
        
        dw = decoratorworker.DecoratorWorker()
        opResult = dw.processObjects(context = context, action = decoratorworker.DecoratorWorkerModes.Reset)
        
        return opResult    
    

    
# Operator to remove a custom object property
class OBJECT_OT_DecoratorRemove(bpy.types.Operator):    
    """Remove the custom object property named above"""
    bl_idname = "t1nker.object_property_manager_remove"
    bl_label = "Remove custom object property"
    bl_options = {'REGISTER', 'UNDO'}    
    
    # Operator settings
    settings : DecoratorSettings = None        

    # Lifecycle management ========================================================================================================
    def __init__(self):
        self.log = None
        self.settings = DecoratorSettings(self)
    
    # See if the operation can run ================================================================================================
    @classmethod
    def poll(cls, context):
        # Return true if the current Blend file is saved and we are in object mode, not in some edit mode 
        # (being in a non-object mode would prevent creating doubles of objects for pre-export manipulation)
        return context.mode == 'OBJECT'
    
    # Show the export dialog ======================================================================================================
    def invoke(self, context, event):
        
        # For first run in the session, load addon defaults (otherwise use values set previously in the session)
        if self.settings is None:
            self.settings = context.preferences.addons[__package__].preferences.settings

        # Show export dialog
        result = context.window_manager.invoke_props_dialog(self, width=400)
        
        return result

    # Here is the core stuff ======================================================================================================
    def execute(self, context): 
        """Execute the operator
        """                     
        # We just need to run the worker with the context and the proper operation mode (removal here)
        
        dw = decoratorworker.DecoratorWorker()
        opResult = dw.processObjects(context = context, action = decoratorworker.DecoratorWorkerModes.Remove)
        
        return opResult    
    

