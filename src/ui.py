import bpy

from .operator import SEQUENCER_OT_EDLExport


# ############################################################
# User Interface
# ############################################################

def menu_func_export(self, context):
    self.layout.operator(
        SEQUENCER_OT_EDLExport.bl_idname, text="Video Sequence (.edl)")


# ############################################################
# Un/Registration
# ############################################################

def register():
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
