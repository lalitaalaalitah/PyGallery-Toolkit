# File Organizer 📂

Organize your photos and videos into a structured folder hierarchy based on their metadata.

## Description 📝

The file_organizer.py script helps you organize your image and video files into a directory structure based on their metadata. You can customize the folder structure and file naming conventions, as well as choose to copy or move the files.

## Usage 💡

To run the script, use the following command:

```
python file_organizer.py input_path --arg1 --arg2 ...
```

### Arguments

- **input_path (required)**: Absolute path to the images to process.

- **-o, --output_path**: Absolute path to save the processed images. If not specified, the script will prompt you for the output path during execution. If it is the same as the input_path, the images will be overwritten in that same directory.

- **--folder_structure**: Folder tree in which your files will be organized based on their metadata. Each list element will be a level in the new folder structure. To separate by subdirectories, just use a forward slash (even if you are on Windows). Default is `%Y/%m - %B`.

- **--file_name_template**: Names that will have the parsed files in the output directory. Leave it blank or null if you want the current file name to be maintained.

- **--auto_clean_output**: Whether we should reset the output directory before start. If `false` we will ask the user before removing any content in the output directory.

- **-c, --copy**: Copy files instead of moving. Note that moving is generally faster than copying, specially with big files.

- **--recursive**: Whether we should search for files in subdirectories of the input directory. Default is True.

- **-v, --verbose**: Enable verbose output.

## Important notes ⚠️

- Make sure the `input_path` and the `output_path` are absolute paths.
- Be careful when specifying the `file_name_template` argument, since a template that is too generic could lead to many duplicates. When this happens, file names are created by adding (1), (2)... to the current name.

## How do we organize the files? 🗄️

When organizing your files, we utilize metadata associated with each image or video. Metadata is additional information embedded within the file that describes its attributes. For images, this may include details such as the date the photo was taken, the camera settings used, and even location information. Videos also contain metadata like duration, resolution, and creation date.

By extracting this metadata, our script can intelligently categorize your files into a structured folder hierarchy. For example, photos and videos can be sorted into folders based on their creation date (e.g., year and month), allowing for a neat and organized directory structure that reflects the chronological order of your media files.

To configure this entire structure, we give you all the control! By default, we will put your files in a structure where in the first level of folders you will see years and in the second level you will see months. Within these month folders you will see the files with their original name, although this can also be modified.

To customize all this, the `folder_structure` and `file_name_template` parameters mentioned above are used. In them, you must use variables to organize your structure efficiently. Thanks to the use of variables, you can group and name some photos, replacing the variable with information from the files. You can use the following variables to name your files/folders:

| Placeholder                                                                                                                  | Where do we find this in the metadata (by order of precedence)                                      |
| ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Any of [the standard Python time directives](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior) | EXIF:DateTimeOriginal, XMP:DateTimeOriginal, QuickTime:CreateDate, EXIF:CreateDate, EXIF:ModifyDate |
| Camera Make                                                                                                                  | EXIF:Make, QuickTime:Make                                                                           |
| Camera Model                                                                                                                 | EXIF:Model, QuickTime:Model                                                                         |
| Software                                                                                                                     | EXIF: Software                                                                                      |

So, the string `IMG_%y_%m` will create file/folder names like `IMG_2020_03`, `IMG_2021_11` and so on.

## Examples 🛠️

### Basic Example

Organize images from the "C:/users/your_user/images" directory into the ./output directory:

```
python file_organizer.py "C:/users/your_user/images" -o ./output
```

### Custom Folder Structure

Organize images into a custom folder structure:

```
python file_organizer.py "C:/users/your_user/images" -o ./output --folder_structure "%Y/%m"
```

### Copy Files Instead of Moving

Copy files to the output directory instead of moving:

```
python file_organizer.py "C:/users/your_user/images" -o ./output --copy
```

### Verbose Output

Enable verbose output to get detailed logs:

```
python file_organizer.py "C:/users/your_user/images" -o ./output --verbose
```

### Combine Multiple Parameters

Organize images, use a custom folder structure, copy files, enable verbose output and not parse subdirectories in the input_path:

```
python file_organizer.py "C:/users/your_user/images" -o ./output --folder_structure "%Y/%m" --copy --verbose --no-recursive
```
