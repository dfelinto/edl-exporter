SETLOCAL
REM Convert the .exr from the sequencer to .tif files

SET BLENDER=C:\src\blender\versions\blender-2.78a-windows64\blender.exe
SET PYTHON_SCRIPT=C:\src\addons\edl-export\exr_to_tif_converter.py
SET EDIT_FILE=R:\agent327\export\tools\edit.blend
SET CHANNEL=31
SET OUTPUT="R:\agent327\frames_grade"

REM "Debug Options"
SET CHANNEL=1
SET EDIT_FILE="S:\users\dalai\io_edl\test-vse.blend"

%BLENDER% -b %EDIT_FILE% -P %PYTHON_SCRIPT% -- %CHANNEL% %OUTPUT%

pause
