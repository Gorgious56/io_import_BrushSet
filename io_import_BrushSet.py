# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>


#---------------------------------------------#

import bpy
import os
from bpy.props import (
    CollectionProperty,
    StringProperty,
    BoolProperty,
)
from bpy.types import (
    Operator,
    OperatorFileListElement,
)

# addon description
bl_info = {
    "name": "Import BrushSet",
    "author": "Daniel Grauer (kromar), CansecoGPC, Gorgious56",
    "version": (1, 2, 3),
    "blender": (2, 80, 0),
    "location": "File > Import > BrushSet",
    "description": "Imports selected image files or all the images in the folder if no file is selected",
    "warning": '',    # used for warning icon and text in addons panel
    "doc_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/Scripts/Import-Export/BrushSet",
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "category": "Import-Export",
}

#---------------------------------------------#

# extension filter (alternative use mimetypes)
# TODO: rewrite so it tries to load image and if it fails we know its not a format blender can load
ext_list = ['.bmp',
            '.png',
            '.jpg',
            '.jp2',
            '.rgb',
            '.dds',
            '.hdr',
            '.exr',
            '.dpx',
            '.cin',
            '.tga',
            '.tif'];

#---------------------------------------------#

def LoadBrushSet(directory, files, use_fake_user, verbose, overwrite):
    imported_images = 0
    if files[0].name == "":
        # Selected a directory. Parse all its files 
        files = os.listdir(directory)
    else:
        # Selected at least one individual file. Get their name
        files = [f.name for f in files]
    print("\nBegin Importing Brush Set :")
    for file in files:
        path = directory + file
        # Filter image files :
        if any(file.lower().endswith(ext) for ext in ext_list):
            # Use existing image and texture if overwrite is selected :
            if overwrite and file in bpy.data.textures and file in bpy.data.images:
                texture = bpy.data.textures.get(file)
                image = bpy.data.images.get(file)
            else:
                texture = bpy.data.textures.new(file, 'IMAGE')
                image = bpy.data.images.load(path)
            texture.use_fake_user = use_fake_user
            image.use_fake_user = use_fake_user

            bpy.data.textures[texture.name].image = image
            if verbose: 
                print(f"  Imported {file}")
            imported_images += 1

    print(f"Import Ended : {imported_images} Textures were imported\n")

#---------------------------------------------#

class BrushSetImporter(Operator):
    '''Load Brush Set'''
    bl_idname = "import_image.brushset"
    bl_label = "Import BrushSet"
    
    use_fake_user: BoolProperty(name="Fake User", description="Import Textures and Images with Fake User")
    verbose: BoolProperty(name="Verbose Output", description="Verbose output in the System Console")
    overwrite: BoolProperty(name="Overwrite", description="Overwrite Image & Texture if already loaded in file")
 
    files: CollectionProperty(
        type=OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'},
        )
    
    directory: StringProperty(
        name="Selected Directory",
        description="Where I will save my stuff",
        )
    def execute(self, context):
        LoadBrushSet(self.directory, self.files, self.use_fake_user, self.verbose, self.overwrite)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

#---------------------------------------------#

def menu_func(self, context):
    # Clear the default name for import
    import_name = ""
    self.layout.operator(BrushSetImporter.bl_idname, text = "Brush Set").directory = ""


#---------------------------------------------#


classes = (
    BrushSetImporter,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)


if __name__ == "__main__":
    register()
