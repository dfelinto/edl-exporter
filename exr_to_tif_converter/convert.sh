#!/bin/bash
echo "Convert the .exr from the sequencer to .tif files"

BLENDER=/shared/software/blender/blender-buildbot/latest/blender
PYTHON_SCRIPT=/shared/software/edl-exporter/exr_to_tif_converter/exr_to_tif_converter.py
EDIT_FILE=/render/agent327/export/tools/edit.blend
CHANNEL=31
OUTPUT=/render/agent327/frames_grade

export OCIO=/shared/software/filmic-blender/config.ocio
$BLENDER -b $EDIT_FILE -P $PYTHON_SCRIPT -- $CHANNEL $OUTPUT
