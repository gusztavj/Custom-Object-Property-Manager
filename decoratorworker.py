# T1nk-R's Custom Object Property Manager add-on for Blender
# - part of T1nk-R Utilities for Blender
#
# Version: Please see the version tag under bl_info in __init__.py.
#
# This module contains business logic for the add-on.
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

from datetime import datetime
from enum import Enum
import bpy

# Enum for operating modes ########################################################################################################
class DecoratorWorkerModes(Enum):
    """
    An enum for operating modes.
    """
    Add = 1,
    Remove = 2,
    Reset = 3,
    Extend = 4

    
# Container for the algorithm of supported operations #############################################################################
class DecoratorWorker:
    """
    Container for the algorithm of supported operations.
    """
    
    def processObjects(self, context, action: DecoratorWorkerModes): 
        """
        Process objects scoped by the decoratorSettings properties of context.scene, and add or delete a custom property,
        as controlled by action.

        Args:
            context (bpy.types.Context): A Blender context object containing Blender objects, selection info and operation settings.
            It is expected for context.scene to have a property decoratorSettings of the decorator.DecoratorSettings type.
            action (DecoratorWorkerModes): One of DecoratorWorkerModes's values to tell whether to add or delete the property.

        Returns:
            Operator Return Items: One of the values specified at https://docs.blender.org/api/current/bpy_types_enum_items/operator_return_items.html#rna-enum-operator-return-items
        """
        operationStarted = f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}"
        
        status = None
        summary = ""
        
        print("")
        print("")
        print(f"=" * 80)
        print(f"T1nk-R Custom Object Property Manager started ({operationStarted})")
        print(f"-" * 80)
        
        # Big try block to make sure we terminate gracefully
        
        try:
            print(f"Decorator {'addition' if action == DecoratorWorkerModes.Add else 'removal'} process started")
            
            # Get relevant stuff to shortcut variables
            settings = context.scene.decoratorSettings            
            viewLayer = context.view_layer            
            activeObject = viewLayer.objects.active
                        
            # Determine scope and collect objects
            if settings.affectSelectedObjectsOnly:
                if len(bpy.context.selected_objects) == 0:
                    print(f"You chose to process selected objects only, but no object is selected")
                    raise ValueError("You choose to process selected objects only, but no object is selected")
                else:
                    print(f"Will process only selected objects")
                objects = bpy.context.selected_objects
            else:
                print(f"Will process all objects as follows")
                objects = viewLayer.objects

            if settings.isVerbose:
                print("Objects to process" + ", ".join([o.name for o in objects]))

            # Make a note of what is going to happen
            match action:
                case DecoratorWorkerModes.Add:
                    print(f"Will add property {settings.propertyName} with a value of '{settings.propertyValue}'")         
                case DecoratorWorkerModes.Extend:
                    print(f"Will extend property {settings.propertyName} with the default value of '{settings.propertyValue}'")         
                case DecoratorWorkerModes.Reset:
                    print(f"Will reset property {settings.propertyName} to the default value of '{settings.propertyValue}'")         
                case DecoratorWorkerModes.Remove:
                    print(f"Will remove property {settings.propertyName}")
                case _:
                    raise ValueError("Invalid operation mode specified. This should not happen. Contact the developer and blame him.")
            
            print(f"Processing {len(objects)} objects...")
            changed = 0
                    
            # Process all objects in scope
            for object in objects:                
                    
                # Branch based on whether the current object has this property 
                if settings.propertyName in object.keys(): # this object has this property
                    
                    # Branch based on operation mode
                    match action:
                        
                        case DecoratorWorkerModes.Add: # addition requested                           
                            print(f"\tResetting property value for '{object.name}'")
                            
                            # The property already exists, don't need to re-add
                            if settings.isVerbose:
                                print(f"\tProperty already exists on '{object.name}' with a value of '{object[settings.propertyName]}', will be reset")
                                
                            if settings.isTestOnly:                                
                                print(f"\t\t-- Relax, nothing is done as this is just a test")
                            else:                                
                                object[settings.propertyName] = settings.propertyValue
                        
                        case DecoratorWorkerModes.Extend: # extension requested
                            # The property already exists, don't need to re-add
                            if settings.isVerbose:
                                print(f"\tProperty already exists on '{object.name}' with a value of '{object[settings.propertyName]}', and it won't be reset")
                        
                        case DecoratorWorkerModes.Reset: # reset value to default
                            # The property already exists, revert its value to the default
                            print(f"\tResetting property value for '{object.name}'")                            
                            
                            if settings.isVerbose:
                                if object[settings.propertyName] == settings.propertyValue:
                                    print(f"\tProperty already exists on '{object.name}' with a value of '{object[settings.propertyName]}', will be reset")
                                else:
                                    print(f"\tProperty already exists on '{object.name}', and is now reset")
                            
                            if settings.isTestOnly:                                
                                print(f"\t\t-- Relax, nothing is done as this is just a test")
                            else:
                                object[settings.propertyName] = settings.propertyValue
                                                    
                        case DecoratorWorkerModes.Remove: # removal requested
                            # The property exists, needs to be removed
                            print(f"\tRemoving property from '{object.name}'")
                            
                            if settings.isTestOnly:                                
                                print(f"\t\t-- Relax, nothing is done as this is just a test")    
                            else:
                                del object[settings.propertyName]
                                
                            changed = changed + 1
                                
                        case _:
                            # Do nothing, it may happen that nothing has to be made on this code branch with a specific operation mode
                            pass
                    
                else: # this object doesn't have this property
                    
                    # Branch based on operation mode
                    match action:
                        
                        case DecoratorWorkerModes.Add: # addition requested
                            # This object doesn't have this property, let's add it
                            print(f"\tAdding property to '{object.name}'")
                            
                            if settings.isTestOnly:                                
                                print(f"\t\t-- Relax, nothing is done as this is just a test")    
                            else:
                                object[settings.propertyName] = settings.propertyValue
                                
                            changed = changed + 1
                            
                        case DecoratorWorkerModes.Extend: # addition requested
                            # This object doesn't have this property, let's add it
                            print(f"\tAdding property to '{object.name}'")
                            
                            if settings.isTestOnly:                                
                                print(f"\t\t-- Relax, nothing is done as this is just a test")    
                            else:
                                object[settings.propertyName] = settings.propertyValue
                                
                            changed = changed + 1
                        
                        case DecoratorWorkerModes.Remove: # removal requested
                            # This object doesn't have this property, there's nothing to reset
                            if settings.isVerbose:
                                print(f"\tObject '{object.name}' doesn't have this property, therefore there's nothing to reset")
                                    
                        case DecoratorWorkerModes.Remove: # removal requested
                            # This object doesn't have this property, there's nothing to remove
                            if settings.isVerbose:
                                print(f"\tObject '{object.name}' doesn't have this property, therefore there's nothing to remove")
                        
                        case _:
                            # Do nothing, it may happen that nothing has to be made on this code branch with a specific operation mode
                            pass
            
            # Make a note of peaceful completion
            summary = \
                f"Processing finished, {changed} items would have been affected if this weren't a test" \
                if settings.isTestOnly else \
                f"Processing finished, {changed} items affected"
                
            status = {'FINISHED'}
            
        except Exception as ex:
            summary = f"An error occurred: {ex}"
            status = {'CANCELLED'}
        finally:
            # Restore active and selected flags
            viewLayer.objects.active = activeObject
            
            print("")
            print(f"-" * 80)        
            print(summary)
            print(f"-" * 80)
            print(f"T1nk-R Custom Object Property Manager finished")                                            
            print(f"=" * 80)
            print("")
        
        return (status, summary)
