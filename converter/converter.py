import json
import os
import shutil
from typing import Any

dir = os.dirname(__file__)

fluent_emoji_path = os.path.join(dir, '..', 'assets')

# Get all emoji folders in ../assets/
emoji_folders = os.listdir(fluent_emoji_path)

# Check if successful: print first 5 emoji types
print(emoji_folders[:5])

# Create array of objects for each emoji folder
emoji_data = dict[str, Any]()
for emoji_folder in emoji_folders:
    # Read metadata.json
    with open(os.path.join(fluent_emoji_path, emoji_folder, 'metadata.json'), encoding='utf8') as file:
        metadata = json.load(file)
        emoji_data[metadata.get('unicode')] = metadata
        file.close()

# Check if successful: print first in emoji_data
print(list(emoji_data.values())[0])

variants_export_paths = {
    '3D': os.path.join(dir, '../export/3D_png/'),
    'Color': os.path.join(dir, '../export/color_svg/'),
    'Flat': os.path.join(dir, '../export/flat_svg/'),
    'High Contrast': os.path.join(dir, '../export/highcontrast_svg/'),
}

# Delete previous export first
# for export_path in variants_export_paths.values():
#     for file in os.listdir(export_path):
#         os.remove(export_path + file)

# Create or open file for each emoji in emoji_data
emoji_index = -1
for unicode, data in emoji_data.items():
    emoji_index += 1

    for variant in variants_export_paths.keys():
        # Define import and export paths, sometimes svg files are in a Default folder
        import_folder_path = os.path.join(fluent_emoji_path, emoji_folders[emoji_index], variant)
        import_folder_path_2nd = os.path.join(fluent_emoji_path, emoji_folders[emoji_index], 'Default', variant)

        # Define the normal export file path with the unicode as the file name
        normal_export_file_path = os.path.join(variants_export_paths[variant], unicode.replace(' ', '-') + '.svg')
        export_file_paths = [normal_export_file_path]

        # If the unicode has a space in it and there is no other emoji with this name, also create a file with the first part only
        if ' ' in unicode:
            first_part = unicode.split(' ')[0]
            if first_part not in emoji_data.keys():
                export_file_paths.append(os.path.join(variants_export_paths[variant], first_part + '.svg'))

        for export_file_path in export_file_paths:
            # Create new export file, if it doesn't exist yet
            # if not os.path.exists(export_file_path):
            try:
                shutil.copy(os.path.join(import_folder_path, os.listdir(import_folder_path)[0]), export_file_path)
            except FileNotFoundError:
                try:
                    shutil.copy(os.path.join(import_folder_path_2nd, os.listdir(import_folder_path_2nd)[0]), export_file_path)
                except FileNotFoundError:
                    print('No ' + variant + ' variant found for ' + unicode)
                    continue
