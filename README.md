# T1nk-R Custom Object Property Manager

Part of **T1nk-R Utilities for Blender**. Authored by [**T1nk-R**](https://github.com/gusztavj).

Version 1.0 @ 2023-12-07

You can use this Blender add-on to add, edit and remove custom object properties in batches. You need Blender 3.3 or newer for this addon to work.

Help, support, updates and anything else: [https://github.com/gusztavj/Custom-Object-Property-Manager](https://github.com/gusztavj/Custom-Object-Property-Manager)

## Copyright

Creative Commons CC-BY-SA. Simply to put, you can create derivative works based on this script, and if you are nice, you don't remove the following attribution:

> Original addon created by: T1nk-R - [https://github.com/gusztavj](https://github.com/gusztavj)

## Disclaimer

This script is provided as-is. Use at your own risk. No warranties, no guarantee, no liability, no matter what happens. Still I tried to make sure no weird things happen.

## What's the Purpose?

This addon helps adding, editing and removing custom properties of Blender objects. You can make a good use of it if you need to:

* Add a custom property to many objects
* Reset the value of a custom property to a specific value for many objects
* Add a custom property to objects which do not yet have it, without changing the value for those objects which already have it
* Delete a custom property from many objects

## Reference

The panel looks like this:

![The panel of Custom Object Property Manager](art/panel.png)

### Set Scope

* **Only process selected objects**. When checked, only selected objects will be processed, otherwise all objects in the view layer of the current scene.

### Configure Property

* **Property name.** Type the name of the property to set, extend, reset or remove.
* **Property value.** Type the value of the property. The value is not observed when removing the property.

### Operation Mode

* **Verbose mode**. When checked, the log in the **System Console** will detail what is happening. For example it will list all objects in the scope and all modifiers processed. Otherwise the log will only list changes made.
* **Just a test**. When checked, nothing will actually happen. Open the **System Console** and learn the effects of your settings before actually applying them.

### Take action

* **Set.** Process all object in the scope, and 
  * add the property to objects not yet having this property, and 
  * reset the property value to **Property Value** for objects already having this property.

* **Extend.** Process all object in the scope, and add the property to objects not yet having this property. If an object already has this property, it's value won't be changed.

* **Reset.** Process all object in the scope, and reset the property value to **Property Value** for objects already having this property. If an object doesn't have this property, it won't be added.

* **Remove.** Process all object in the scope, and remove this property from each having it.
