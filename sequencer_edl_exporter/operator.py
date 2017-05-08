import os
import re
import bpy

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


# ############################################################
# Classes
# ############################################################

class Strip(object):
    def __init__(self, index, strip, fps, fps_base):
        self._index = index
        self._fps = fps
        self._fps_base = fps_base
        self._process_strip(strip)
        self._create_data_dictionary()

    def to_edl(self):
        """
        Export strip data into .edl formatted line
        """
        line = "{index:03d} " \
               "{reel_name:8s} " \
               "{channel_type} " \
               "{cut_type} " \
               "{source_in} " \
               "{source_out} " \
               "{edit_in} " \
               "{edit_out}" \
               "\n" \
               .format(**self._data)
        return line

    def _create_data_dictionary(self):
        self._data = {
            "index": self._index + 1,
            "reel_name": self._reel_name,
            "channel_type": self._channel_type,
            "cut_type": "C",
            "source_in": self._smpte(self._source_in),
            "source_out": self._smpte(self._source_out),
            "edit_in": self._smpte(self._edit_in, style='RESOLVE'),
            "edit_out": self._smpte(self._edit_out, style='RESOLVE'),
            }

    def _smpte(self, frame, style=None):
        """
        Convert frames to SMPTE
        """
        if style is None:
            pass

        elif style == 'RESOLVE':
            "From Blender to DaVinci Resolve."
            seconds = 60
            minutes = 60
            frame += -1 + self._fps * seconds * minutes

        else:
            assert False, "Style :{0} not supported".format(style)

        return bpy.utils.smpte_from_frame(
            frame, fps=self._fps, fps_base=self._fps_base)

    def _get_reel_name(self, strip):
        """
        Get the reel name based on the directory.
        Also forces a 7-chars name like "01_02_B".
        """
        directories = bpy.path.abspath(strip.directory).split(os.path.sep)
        assert(len(directories) > 1 and directories[-2])
        return directories[-2][:7]

    def _get_image_offset(self, *args):
        return 0

    def _process_strip(self, strip):
        frame_start = strip.frame_start
        frame_offset_start = strip.frame_offset_start
        frame_final_duration = strip.frame_final_duration

        self._source_in = self._get_image_offset(strip) + frame_offset_start
        self._source_out = self._source_in + frame_final_duration
        self._edit_in = frame_start + frame_offset_start
        self._edit_out = self._edit_in + frame_final_duration

        self._reel_name = self._get_reel_name(strip)


class VideoStrip(Strip):
    _channel_type = 'V'


class ImageSequenceStrip(VideoStrip):
    def _get_image_offset(self, strip):
        """
        We should check if at least the first frame is in the
        hard disk.
        """
        return 0


class ImageStrip(ImageSequenceStrip):
    def _get_image_offset(self, strip):
        """
        Get the real offset of the image based on the
        image sequence the image is from.
        """
        filename = strip.elements[0].filename
        digits = list(re.finditer('\d+', filename))

        if len(digits) == 0:
            return 0

        directory = bpy.path.abspath(strip.directory)
        digits = digits[-1]
        number = int(digits.group())

        prefix = filename[:digits.start()]
        suffix = filename[digits.end():]

        filepath_values = {
            "directory": directory + os.path.sep,
            "prefix": prefix,
            "suffix": suffix,
            "number_len": len(digits.group()),
            "number": number,
            }

        real_offset = 0
        while number > 1:
            number -= 1
            filepath_values["number"] = number
            filepath = "" \
                "{directory}" \
                "{prefix}" \
                "{number:0{number_len}}" \
                "{suffix}" \
                "".format(**filepath_values)

            if os.path.isfile(filepath):
                real_offset += 1
            else:
                break

        expected_offset = strip.frame_offset_start
        return real_offset - expected_offset

    def to_edl(self):
        """
        M2 is the command to suggest speed change.
        In this case we do it with 000.0, which freezes the frame.
        """
        line = super(ImageStrip, self).to_edl()
        line += "" \
                "M2 " \
                "{reel_name:8s} " \
                "000.0 " \
                "{source_in}" \
                "\n\n" \
                .format(**self._data)
        return line


def refine_strip(index, strip, fps, fps_base):
    """
    Define which class to inherit based on the strip properties.
    """
    strip_class = Strip
    strip_type = strip.type

    if strip_type == 'IMAGE':
        if len(strip.elements) == 1:
            strip_class = ImageStrip
        else:
            strip_class = ImageSequenceStrip

    elif strip_type == 'MOVIE':
        strip_class = VideoStrip

    return strip_class(index, strip, fps, fps_base)


# ############################################################
# Main Exporting Routine
# ############################################################

def export(filepath, fps, fps_base, strips):
    """Create a new file"""
    """
    It's a bit tricky because we need to sort the strips in order
    and extract their reel number
    """
    order_strips = [refine_strip(i, s, fps, fps_base) for i, s in enumerate(
        sorted(strips, key=lambda s: s.frame_start + s.frame_offset_start))]

    with open(filepath, 'w') as f:
        f.write("TITLE: Agent 327\n")

        for strip in order_strips:
            f.write(strip.to_edl())


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
        maxlen=256,
        )

    def execute(self, context):
        """Build EDL file"""
        scene = context.scene
        fps = scene.render.fps
        fps_base = scene.render.fps_base

        if not scene.sequence_editor:
            self.report({'ERROR'}, "Scene has no video sequence")
            return {'CANCELLED'}

        channels = {}
        for strip in scene.sequence_editor.sequences:

            if strip.type not in {'IMAGE', 'MOVIE'}:
                continue

            if not strip.channel in channels:
                channels[strip.channel] = []

            channels[strip.channel].append(strip)

        for v_index, strips in channels.items():
            filepath = self.get_filepath(v_index)
            export(filepath, fps, fps_base, strips)

        return {'FINISHED'}

    def get_filepath(self, v_index):
        """
        Return filepath based on v_index
        """
        dirname = os.path.dirname(self.filepath)
        basename = os.path.basename(self.filepath)

        if basename.endswith(".edl"):
            basename = basename[:-4]

        return os.path.join(dirname, "{0}-V{1}.edl".format(basename, v_index))


# ############################################################
# Un/Registration
# ############################################################

def register():
    bpy.utils.register_class(SEQUENCER_OT_EDLExport)


def unregister():
    bpy.utils.unregister_class(SEQUENCER_OT_EDLExport)
