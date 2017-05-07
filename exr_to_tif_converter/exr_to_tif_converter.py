import os
import sys
import bpy


def create_directory(directory):
    """
    Create output folders.
    """
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as E:
        print(E)
        sys.exit(-1)
    else:
        print("Created directory: \"{0}\"".format(directory))


def convert_exr_to_tif(image_input, image_output):
    """
    Convert exr file to tif using Blender OCIO profile
    e.g., convert_exr_to_tif('/tmp/image.exr', '/tmp/output.tif')
    """
    print("Converting \"{0}\" into \"{1}\".".format(
        image_input, image_output))

    image = bpy.data.images.get('conversion_corner')
    if not image:
        image = bpy.data.images.new('conversion_corner', 10, 10)
        image.source = 'FILE'

    image.filepath = image_input
    image.colorspace_settings.name = 'Linear'
    image.save_render(image_output)


def convert(dir_input, dir_output):
    """
    Convert all .exr files in dir_input to .tif files in dir_output
    """
    create_directory(dir_output)

    for filepath_input in os.listdir(dir_input):

        if not filepath_input.endswith(".exr"):
            continue

        full_filepath_input = os.path.join(
                dir_input, filepath_input)

        if not os.path.isfile(full_filepath_input):
            continue

        filepath_output = "{0}.tif".format(filepath_input[:-4])
        full_filepath_output = os.path.join(
                dir_output, filepath_output)

        # Save new file.
        convert_exr_to_tif(full_filepath_input, full_filepath_output)


def get_directory_input(strip):
    """
    Returns the original folder for a strip
    """
    return bpy.path.abspath(strip.directory)


def get_directory_output(output_folder, strip):
    """
    Returns the destination folder for a strip

    output_folder: base folder to export to
    """
    directories = strip.directory.split(os.path.sep)
    assert(len(directories) > 2 and directories[-2])
    scene_name = directories[-2][:7]
    return os.path.join(output_folder, scene_name)


def set_scene_defaults(scene):
    """
    Set scene defaults for the project.
    """
    scene.view_settings.look = 'None'
    scene.render.image_settings.file_format = 'TIFF'
    scene.render.image_settings.color_depth = '16'


def main():
    context = bpy.context
    scene = context.scene

    if not scene.sequence_editor:
        print("Scene has no sequence editor")
        sys.exit(-1)

    set_scene_defaults()

    arguments = get_arguments()
    channel, output_folder = get_arguments()

    directories = []
    for strip in scene.sequence_editor.sequences:

        if strip.channel != channel:
            continue

        if strip.type != 'IMAGE':
            continue

        directories.append((
            get_directory_input(strip),
            get_directory_output(output_folder, strip),
            ))

    print("Starting the conversion")
    for dir_input, dir_output in directories:
        print("Converting \"{0}\" to \"{1}\"".format(dir_input, dir_output))
        convert(dir_input, dir_output)


def get_arguments():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"

    if len(argv) != 2:
        print("Wrong arguments, expected 2, got:", argv)
        sys.exit(-1)

    # Format the arguments.
    channel = int(argv[0])
    output = argv[1]

    return channel, output


main()
