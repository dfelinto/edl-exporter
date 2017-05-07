#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>
bl_info = {
    "name": "EDL Exporter",
    "author": "Dalai Felinto, Francesco Siddi",
    "version": (0, 1),
    "blender": (2, 7, 8),
    "location": "File Exporter",
    "description": "",
    "warning": "",
    "wiki_url": "https://github.com/dfelinto/edl-exporter",
    "tracker_url": "",
    "category": "video Sequencer"}


import bpy

from . import ui
from . import operator


# ############################################################
# User Preferences
# ############################################################

# Preferences
class EDLExportsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        return


# ############################################################
# Un/Registration
# ############################################################

def register():
    bpy.utils.register_class(EDLExportsPreferences)

    operator.register()
    ui.register()


def unregister():
    bpy.utils.unregister_class(EDLExportsPreferences)

    operator.unregister()
    ui.unregister()


if __name__ == '__main__':
    register()
