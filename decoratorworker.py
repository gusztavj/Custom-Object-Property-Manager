# T1nk-R's Custom Object Property Manager add-on for Blender
# - part of T1nk-R Utilities for Blender
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

from enum import Enum
import bpy

# An enum for operating modes =====================================================================================================
class DecoratorWorkerModes(Enum):
    """An enum for operating modes
    """
    Add = 1,
    Remove = 2,
    Reset = 3,
    Extend = 4

    
# Container for the algorithm to to addition/deletion of object properties ========================================================
class DecoratorWorker:
    """
    Container for the algorithm to to addition/deletion of object properties.
    """
    
    def processObjects(self, context, action: DecoratorWorkerModes): 
        """Process objects scoped by the decoratorSettings properties of context.scene, and add or delete a custom property,
        as controlled by action.

        Args:
            context (bpy.types.Context): A Blender context object containing Blender objects, selection info and operation settings.
            It is expected for context.scene to have a property decoratorSettings of the decorator.DecoratorSettings type.
            action (DecoratorWorkerModes): One of DecoratorWorkerModes's values to tell whether to add or delete the property.

        Returns:
            Operator Return Items: One of the values specified at https://docs.blender.org/api/current/bpy_types_enum_items/operator_return_items.html#rna-enum-operator-return-items
        """
        
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
                            print(f"\tResetting property value for {object.name}")
                            
                            # The property already exists, don't need to re-add
                            if settings.isVerbose:
                                print(f"\tProperty already exists on {object.name} with a value of '{object[settings.propertyName]}', will be reset")
                                
                            if settings.isTestOnly:                                
                                print(f"\t\t-- Relax, nothing is done as this is just a test")
                            else:                                
                                object[settings.propertyName] = settings.propertyValue
                        
                        case DecoratorWorkerModes.Extend: # extension requested
                            # The property already exists, don't need to re-add
                            if settings.isVerbose:
                                print(f"\tProperty already exists on {object.name} with a value of '{object[settings.propertyName]}', and it won't be reset")
                        
                        case DecoratorWorkerModes.Reset: # reset value to default
                            # The property already exists, revert its value to the default
                            print(f"\tResetting property value for {object.name}")                            
                            
                            if settings.isVerbose:
                                if object[settings.propertyName] == settings.propertyValue:
                                    print(f"\tProperty already exists on {object.name} with a value of '{object[settings.propertyName]}', will be reset")
                                else:
                                    print(f"\tProperty already exists on {object.name}, and is now reset")
                            
                            if settings.isTestOnly:                                
                                print(f"\t\t-- Relax, nothing is done as this is just a test")
                            else:
                                object[settings.propertyName] = settings.propertyValue
                                                    
                        case DecoratorWorkerModes.Remove: # removal requested
                            # The property exists, needs to be removed
                            print(f"\tRemoving property from {object.name}")
                            
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
                            print(f"\tAdding property to {object.name}")
                            
                            if settings.isTestOnly:                                
                                print(f"\t\t-- Relax, nothing is done as this is just a test")    
                            else:
                                object[settings.propertyName] = settings.propertyValue
                                
                            changed = changed + 1
                            
                        case DecoratorWorkerModes.Extend: # addition requested
                            # This object doesn't have this property, let's add it
                            print(f"\tAdding property to {object.name}")
                            
                            if settings.isTestOnly:                                
                                print(f"\t\t-- Relax, nothing is done as this is just a test")    
                            else:
                                object[settings.propertyName] = settings.propertyValue
                                
                            changed = changed + 1
                        
                        case DecoratorWorkerModes.Remove: # removal requested
                            # This object doesn't have this property, there's nothing to reset
                            if settings.isVerbose:
                                print(f"\tObject {object.name} doesn't have this property, therefore there's nothing to reset")
                                    
                        case DecoratorWorkerModes.Remove: # removal requested
                            # This object doesn't have this property, there's nothing to remove
                            if settings.isVerbose:
                                print(f"\tObject {object.name} doesn't have this property, therefore there's nothing to remove")
                        
                        case _:
                            # Do nothing, it may happen that nothing has to be made on this code branch with a specific operation mode
                            pass
            
            # Make a note of peaceful completion
            if settings.isTestOnly:
                print(f"Processing finished, {changed} items would have been affected if this wasn't a test")
            else:
                print(f"Processing finished, {changed} items affected")
            
        except Exception as ex:
            print(ex)
        finally:
            # Restore active and selected flags
            viewLayer.objects.active = activeObject
            print(f"Property creation process exited")

        return {'FINISHED'}