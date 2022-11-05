# Image organizer 📂🖼️​​

Fix the metadata of your images and videos, find similar or duplicate images and organize your folder structure to create a well-organized gallery. All this in a simple script!

## Download/Installation steps 🚀

To install the project you must have python 3 installed and added to your path. Once this step is done, you should run this command in the terminal, in the directory where you have cloned the project:

```
pip install -r requirements.txt
```

**Notes:**

> The project has been made with python version 3.10, so its compatibility with later or previous versions is not guaranteed. Also, has been only tested in a Windows machine, so it is also not guaranteed that the results will be optimal in other systems (please, open an issue if that is the case).

## Usage example 💡

If the installation was successful, you are ready to start! To do it, paste some images into a new directory inside the project. That is, for example, create a folder called <code>input</code> in the root directory of the cloned project, and paste some files in .jpg / .jpeg. Then enter the following command:

```
python main.py --input_path='input' --output_path='output'
```

If everything went well, you will see that a new folder has been created called <code>output</code>, where your photos are organized in subfolders by year and month

### Settings & Customization ⚙️

Fantastic, right? But this is not all, many configuration options are also provided, which you can consult by typing <code>python main.py --help</code> in the terminal:

```
 --input_path INPUT_PATH
                        Path to the images to proccess
  --output_path OUTPUT_PATH
                        Path to save the proccessed images. If it is the same as the input_path the images will be
                        overwritten in that same directory
  --recursive, --no-recursive
                        Recursively process media (look for media in all the subfolders of the input_path) or not.
                        Defaults to True (--recursive)
  --fix_datetaken_mode {always,no_overwrite,never}
                        File metadata update/correction mode. Defaults to no_overwrite, that is, do not update the
                        metadata if already exists
  --hash_size HASH_SIZE
                        Hash size. Used for identification of similar images. With larger values the search will be
                        more exhaustive but slower. Giving a value of 0 skips the search for duplicates/similar
                        altogether. Defaults to 64
  --similarity SIMILARITY
                        Similarity of the images to be deleted by the user (always after being asked during the
                        process). It is a number from 0 to 100, with 100 being the number to pass when we want only
                        completely identical images to appear. This parameter does not affect the speed of the
                        process, as does --hash_size. Defaults to 99
  --folder_structure FOLDER_STRUCTURE
                        Folder tree in which your files will be organized based on their metadata. By default it is
                        'year>month', that is, first folders will be created with the years of the files, and within
                        these, folders with the months. Within each month the corresponding files will be located
```

Special mention requires the last parameter mentioned here, folder_structure, which allows you to customize the new folder structure. To do this, we will pass something like "key1 > key2 > key3" to this parameter, where each ">" represents a depth level in the folder structure and each key, a value of the files metadata, that will be the folder names. At the moment only structuring by <code>month</code> and <code>year</code> is allowed but many more keys will arrive soon. To see the available keys and other useful parameters for this customization visit <a href="https://github.com/enrique-lozano/Image-organizer/blob/main/src/constants/new_filenames_utils.py">this file</a>

So for example, to run the program with some of these more advanced settings, we could put something like this::

```
python main.py --input_path='input' --output_path='output' --fix_datetaken="always" --hash_size=32 --folder_structure="year > month"
```

## Next updates 🔜

- More keys to organize your folders
- Improve application performance (especially in the search for duplicates)
- Improve the way files are deleted, giving the user greater control

## Issues 🤕

- Creation date modification based on filename is not working correctly, making some files to not be organized correctly

## Want to collaborate? 🙋🏻

Feel free to improve and optimize the existing code. To contribute to the project, read the previous points carefully and do the next steps with the project:

1. Fork it (<https://github.com/enrique-lozano/Image-organizer/fork>)
2. Create your feature branch (`git checkout -b feature/newFeature`)
3. Commit your changes (`git commit -am 'Add some newFeature'`)
4. Push to the branch (`git push origin feature/newFeature`)
5. Create a new Pull Request

## Need help ❓

Feel free to contact the developer if you have any questions or suggestions about the project or how you can help with it.
