# Metadata fixer 📂

Fix common problems with your files by adding missing date metadata and other tags.

## Description 📝

Metadata is additional information embedded within the file that describes its attributes. For images, this may include details such as the date the photo was taken, the camera settings used, and even location information. Videos also contain metadata like duration, resolution, and creation date.

On many occasions, especially when the photos and videos come from external media such as the Internet or social networks such as WhatsApp, the metadata is very lacking in information or directly incorrect. This means that when using these images and videos on other platforms that use these metadata (such as Google Photos) you may see incorrect information.

The metadata_fixer.py script helps you address common issues with the metadata of your image and video files, such as missing date metadata. It can add missing dates based on various sources, fix GPS coordinates, and modify file creation and modification times based on existing metadata.

## Usage 💡

To run the script, use the following command:

```
python metadata_fixer.py input_path --arg1 --arg2 ...
```

### Arguments

- **input_path (required)**: Absolute path to the images to process.

- **--dates_from**: Sources to obtain the capture date of the asset, in order of preference. Options can include 'fileexif' (from file's EXIF data), 'filename' (from the filename) or 'filedate' (from the OS date of the file). Default is `["fileexif", "filename"]`.

- **--overwrite_dates**: Overwrite existing date tags based on the `--dates_from` argument, even if they are already defined.

- **--gps_fix**: Fix the `QuickTime` tag of the file metadata.

- **--os_dates**: Modify the file creation and modification time based on its EXIF data.

- **--recursive**: Whether we should search for files in subdirectories of the input directory. Default is True.

- **-v, --verbose**: Enable verbose output.

## Important notes ⚠️

- Make sure the `input_path` is an absolute paths.
- Use the `--overwrite_dates` flag cautiously, as it will overwrite existing date tags in your file metadata based on the specified sources.
- Ensure that the files have appropriate permissions for modification.

## Examples 🛠️

### Basic Example

Fix metadata in files from the "C:/users/your_user/images" directory:

```
python metadata_fixer.py "C:/users/your_user/images"
```

### Overwrite Dates from Filename

Update date metadata based on filenames, overwriting any existing date info in the metadata:

```
python metadata_fixer.py "C:/users/your_user/images" --dates_from filename --overwrite_dates
```

### Specify from where we should get date info

Update date metadata based on the date of the filename and if fails, the creation/modification date of the file. Also, overwrite any existing date info in the metadata:

```
python metadata_fixer.py "C:/users/your_user/images" --dates_from filedate filename --overwrite_dates
```

### Disable GPS Fix

Process files without fixing the GPS coordinates:

```
python metadata_fixer.py "C:/users/your_user/images" --no-gps_fix
```

### Disable OS Dates Modification

Process files without modifying file creation and modification times:

```
python metadata_fixer.py "C:/users/your_user/images" --no-os_dates
```

### Disable Recursive Processing

Process only files in the input directory without recursion:

```
python metadata_fixer.py "C:/users/your_user/images" --no-recursive
```

### Verbose Output

Enable verbose output to get detailed logs:

````
```python metadata_fixer.py "C:/users/your_user/images" --verbose
````
