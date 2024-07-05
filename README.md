# PyGallery Toolkit 📂🖼️​​

A set of tools to fix the metadata of your images and videos, find and remove similar images, and organize your folder structure to create a well-structured gallery. All this with simple scripts!

## Download/Installation steps 🚀

To install the project you must have python 3 installed and added to your path. Once this step is done, you should clone/download this project and run this command in a terminal, in the directory where you have cloned the project:

```
pip install -r requirements.txt
```

**Notes:**

> The project has been made with python version 3.11, so its compatibility with later or previous versions is not guaranteed. Also, has been only tested in a Windows machine, so it is also not guaranteed that the results will be optimal in other systems (please, open an issue if that is the case).

## Usage example 💡

If the installation was successful, you are ready to start! To do it, you will have to run the functionality that you want in the following way:

```
python script.py your_path_to_the_assets --arg1 --arg2 ...
```

Here you will have to replace `script.py` for the script that you want.

### Available Scripts

#### - File Organizer - `file_organizer.py`

Organize your photos and videos into a structured folder hierarchy based on their metadata and your preferences. [See docs](https://github.com/enrique-lozano/PyGallery-Toolkit/blob/main/src/features/file_organizer/README.md)

#### - Duplicates Remover - `duplicates_remover.py`

Identify and remove similar/duplicate images from your gallery to save space and avoid clutter. [See docs](https://github.com/enrique-lozano/PyGallery-Toolkit/blob/main/src/features/duplicates_remover/README.md)

#### - Metadata Fixer - `metadata_fixer.py`

Fix the metadata of your images and videos to ensure consistency and accuracy accross different apps. Autocomplete missing dates in the metadata of your files. [See docs](https://github.com/enrique-lozano/PyGallery-Toolkit/blob/main/src/features/metadata_fixer/README.md)

---

For more detailed usage instructions for each script, please refer to their respective docs linked above. There you will have all the details about how to configure each script and what options do you have. As a example, if you want to identify and remove similar images you could use the following command:

```
python duplicates_remover.py "your_path" --hash_size 32
```

## Want to collaborate? 🙋🏻

Feel free to improve and optimize the existing code. To contribute to the project, read the previous points carefully and do the next steps with the project:

1. Fork it (<https://github.com/enrique-lozano/Image-organizer/fork>)
2. Create your feature branch (`git checkout -b feature/newFeature`)
3. Commit your changes (`git commit -am 'Add some newFeature'`)
4. Push to the branch (`git push origin feature/newFeature`)
5. Create a new Pull Request

## Need help ❓

Feel free to contact the developer if you have any questions or suggestions about the project or how you can help with it.
