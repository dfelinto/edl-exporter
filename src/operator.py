import bpy

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


# ############################################################
# Exporting Operator
# ############################################################

class SEQUENCER_OT_EDLExport(Operator, ExportHelper):
    """Export Sequence Strips to EDL"""
    bl_idname = "sequencer.export_edl"
    bl_label = "Export EDL"

    filename_ext = ".edl"

    filter_glob = StringProperty(
            default="*.edl",
            options={'HIDDEN'},
            maxlen=255)

    def execute(self, context):
        """Build EDL file"""
        self.report({'ERROR'}, "Not implemented yet.")
        return {'CANCELLED'}


# ############################################################
# Un/Registration
# ############################################################

def register():
    bpy.utils.register_class(SEQUENCER_OT_EDLExport)


def unregister():
    bpy.utils.unregister_class(SEQUENCER_OT_EDLExport)

