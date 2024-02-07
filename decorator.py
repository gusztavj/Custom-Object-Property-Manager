# T1nk-R's Custom Object Property Manager add-on for Blender
# - part of T1nk-R Utilities for Blender
#
# Version: Please see the version tag under bl_info in __init__.py.
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



import bpy
from bpy.props import StringProperty, BoolProperty
from . import decoratorworker

# Addon preferences ###############################################################################################################
class DecoratorSettings(bpy.types.PropertyGroup):
    """
    Settings for the T1nk-R Custom Object Property Manager add-on.
    """
    
    # Properties ==================================================================================================================

    affectSelectedObjectsOnly: BoolProperty(
        name="Only process selected objects",
        description="If unchecked, it will process all of your visible objects",
        default=False
    )
    """
    Controls whether to process selected objects or all.
    """
    
    propertyName: StringProperty(
        name="Property Name",
        description="Specify the name of the property to add or remove",
        default="Hide at Lod Level"
    )    
    """
    The name of the property to add or remove.
    """
    
    propertyValue: StringProperty(
        name="Property Value",
        description="The default value to set for the property (only if the property does not exist)",
        default=""
    )    
    """
    The name of the property to add or remove.
    """

    isVerbose: BoolProperty(
        name="Verbose mode",
        description="Check to get a detailed log on what happened and what not. Non-verbose mode only reports what actually happened.",
        default=False
    )
    """
    Controls log verbosity.
    """
    
    isTestOnly: BoolProperty(        
        name="Just a test", 
        description="Don't do anything, just show what you would do",
        default=False
    )    
    """
    Controls if actions are actually taken or just simulated.
    """

# Panel for the UI ################################################################################################################
class DecoratorPanel(bpy.types.Panel):
    """
    Panel on the sidebar (N) to add, edit or remove custom object properties
    """
    
    # Properties ==================================================================================================================
    
    # Blender-specific stuff ------------------------------------------------------------------------------------------------------    
    bl_idname = "OBJECT_PT_t1nker_decorator_panel"
    bl_label = "T1nk-R Custom Object Properties (T1nk-R Utilities)"
    bl_description = "Add, edit or remove custom object properties"
    bl_location = "3D View -> Sidebar"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "T1nk-R Utils"  # this is going to be the name of the tab

    # Public functions ============================================================================================================

    # Draw the panel  -------------------------------------------------------------------------------------------------------------
    def draw(self, context: bpy.types.Context):
        """
        Draws the panel.

        Args:
            context (Context): A bpy.context object passed by Blender.
        """
        
        # Store the settings in a shorthand variable
        self.settings = context.scene.decoratorSettings
        
        # We'll create boxes with rows for the various settings
        
        layout = self.layout
                
        
        # Scope
        box = layout.box()
                    
        row = box.row(align=True)
        row.label(text="Select scope")
        
        row = box.row(align=True)
        row.prop(self.settings, "affectSelectedObjectsOnly")
        
        
        # Property name and value
        box = layout.box()
                
        row = box.row(align=True)
        row.label(text="Property to add or remove")
        
        row = box.row(align=True)
        row.prop(self.settings, "propertyName")
        
        row = box.row(align=True)
        row.label(text="Type: String (others may be supported in the future)")

        row = box.row(align=True)
        row.prop(self.settings, "propertyValue")
        
        
        # Operation settings
        box = layout.box()
        
        row = box.row(align=True)
        row.label(text="Select operation mode") 
        
        row = box.row(align=True)
        row.prop(self.settings, "isVerbose")  
        
        row = box.row(align=True)
        row.prop(self.settings, "isTestOnly")  


        # Action section
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
        

# Operator to add a property ######################################################################################################
class OBJECT_OT_DecoratorAdd(bpy.types.Operator):    
    """Add the custom object property to objects. If the property exists for an object, its value will be reset to the value specified above"""
    
    # Properties ==================================================================================================================
    
    # Blender-specific stuff ------------------------------------------------------------------------------------------------------    
    bl_idname = "t1nker.object_property_manager_add"
    bl_label = "Add custom object property"
    bl_options = {'REGISTER', 'UNDO'}    
    
    # Lifecycle management ========================================================================================================
    
    # Initialize object -----------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Make an instance and create a scene-level copy of the settings.
        """
        
        self.settings = DecoratorSettings(self)
        """
        Copy of the operator settings specific to the Blender file (scene)
        """
    
    # Public functions ============================================================================================================
    
    # See if the operation can run ------------------------------------------------------------------------------------------------
    @classmethod
    def poll(cls, context):
        """
        Tell if the operator can run.

        Args:
            context (bpy.types.Context): A context object passed on by Blender for the current context.

        Returns:
            bool: `True` if the operator can run, `False` otherwise.
        """
        
        # Return true if the user is in object mode, false otherwise
        return context.mode == 'OBJECT'
    
    # Perform the operation -------------------------------------------------------------------------------------------------------
    def execute(self, context): 
        """
        Execute the operator
        """                     
        
        # We just need to run the worker with the context and the proper operation mode (addition here)
        
        dw = decoratorworker.DecoratorWorker()
        (opResult, report) = dw.processObjects(context = context, action = decoratorworker.DecoratorWorkerModes.Add)
        
        if opResult == {'FINISHED'}:
            self.report({'INFO'}, report)
        else:
            self.report({'ERROR'}, report)

        return opResult
    
# Operator to extend a property ###################################################################################################
class OBJECT_OT_DecoratorExtend(bpy.types.Operator):    
    """Add the custom object property to objects currently not having it. If the property exists for an object, its value won't be changed"""
    # Properties ==================================================================================================================
    
    # Blender-specific stuff ------------------------------------------------------------------------------------------------------    
    bl_idname = "t1nker.object_property_manager_extend"
    bl_label = "Extend custom object property"
    bl_options = {'REGISTER', 'UNDO'}    
    
    # Lifecycle management ========================================================================================================
    
    # Initialize object -----------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Make an instance and create a scene-level copy of the settings.
        """
        
        self.settings = DecoratorSettings(self)
        """
        Copy of the operator settings specific to the Blender file (scene)
        """
    
    # See if the operation can run ------------------------------------------------------------------------------------------------
    @classmethod
    def poll(cls, context):
        """
        Tell if the operator can run.

        Args:
            context (bpy.types.Context): A context object passed on by Blender for the current context.

        Returns:
            bool: `True` if the operator can run, `False` otherwise.
        """
        
        # Return true if the user is in object mode, false otherwise
        return context.mode == 'OBJECT'
    
    # Perform the operation -------------------------------------------------------------------------------------------------------
    def execute(self, context): 
        """
        Execute the operator
        """                     
        
        # We just need to run the worker with the context and the proper operation mode (extension here)
        
        dw = decoratorworker.DecoratorWorker()
        (opResult, report) = dw.processObjects(context = context, action = decoratorworker.DecoratorWorkerModes.Extend)
        
        if opResult == {'FINISHED'}:
            self.report({'INFO'}, report)
        else:
            self.report({'ERROR'}, report)
        
        return opResult
    
# Operator to reset a property ####################################################################################################
class OBJECT_OT_DecoratorReset(bpy.types.Operator):    
    """Reset the custom object property to the value specified above. Only objects having this property will be affected. If an object does not have this property now, it won't be added"""
    
    # Properties ==================================================================================================================
    
    # Blender-specific stuff ------------------------------------------------------------------------------------------------------    
    bl_idname = "t1nker.object_property_manager_reset"
    bl_label = "Reset custom object property"
    bl_options = {'REGISTER', 'UNDO'}    

    # Lifecycle management ========================================================================================================
    
    # Initialize object -----------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Make an instance and create a scene-level copy of the settings.
        """
        
        self.settings = DecoratorSettings(self)
        """
        Copy of the operator settings specific to the Blender file (scene)
        """
    
    # See if the operation can run ------------------------------------------------------------------------------------------------
    @classmethod
    def poll(cls, context):
        """
        Tell if the operator can run.

        Args:
            context (bpy.types.Context): A context object passed on by Blender for the current context.

        Returns:
            bool: `True` if the operator can run, `False` otherwise.
        """
        
        # Return true if the user is in object mode, false otherwise
        return context.mode == 'OBJECT'
    
    # Perform the operation -------------------------------------------------------------------------------------------------------
    def execute(self, context): 
        """
        Execute the operator
        """                     
        # We just need to run the worker with the context and the proper operation mode (reset here)
        
        dw = decoratorworker.DecoratorWorker()
        (opResult, report) = dw.processObjects(context = context, action = decoratorworker.DecoratorWorkerModes.Reset)
        
        if opResult == {'FINISHED'}:
            self.report({'INFO'}, report)
        else:
            self.report({'ERROR'}, report)
            
        return opResult    
    

    
# Operator to remove a property ###################################################################################################
class OBJECT_OT_DecoratorRemove(bpy.types.Operator):    
    """Remove the custom object property named above"""
    
    # Properties ==================================================================================================================
    
    # Blender-specific stuff ------------------------------------------------------------------------------------------------------    
    bl_idname = "t1nker.object_property_manager_remove"
    bl_label = "Remove custom object property"
    bl_options = {'REGISTER', 'UNDO'}    
    
    # Lifecycle management ========================================================================================================
    
    # Initialize object -----------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Make an instance and create a scene-level copy of the settings.
        """
        
        self.settings = DecoratorSettings(self)
        """
        Copy of the operator settings specific to the Blender file (scene)
        """
    
    # See if the operation can run ------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Make an instance and create a scene-level copy of the settings.
        """
        
        self.settings = DecoratorSettings(self)
        """
        Copy of the operator settings specific to the Blender file (scene)
        """
    
    # See if the operation can run ------------------------------------------------------------------------------------------------
    @classmethod
    def poll(cls, context):
        """
        Tell if the operator can run.

        Args:
            context (bpy.types.Context): A context object passed on by Blender for the current context.

        Returns:
            bool: `True` if the operator can run, `False` otherwise.
        """
        
        # Return true if the user is in object mode, false otherwise
        
        return context.mode == 'OBJECT'
    
    # Perform the operation -------------------------------------------------------------------------------------------------------
    def execute(self, context): 
        """Execute the operator
        """                     
        # We just need to run the worker with the context and the proper operation mode (removal here)
        
        dw = decoratorworker.DecoratorWorker()
        (opResult, report) = dw.processObjects(context = context, action = decoratorworker.DecoratorWorkerModes.Remove)
        
        if opResult == {'FINISHED'}:
            self.report({'INFO'}, report)
        else:
            self.report({'ERROR'}, report)
        
        return opResult    
    

