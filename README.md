# PyGallery organizer 📂🖼️​​

Fix the metadata of your images and videos, find similar or duplicate images and organize your folder structure to create a well-organized gallery. All this in a simple script!

## Download/Installation steps 🚀

To install the project you must have python 3 installed and added to your path. Once this step is done, you should clone/download this project and run this command in a terminal, in the directory where you have cloned the project:

```
pip install -r requirements.txt
```

**Notes:**

> The project has been made with python version 3.11, so its compatibility with later or previous versions is not guaranteed. Also, has been only tested in a Windows machine, so it is also not guaranteed that the results will be optimal in other systems (please, open an issue if that is the case).

## Usage example 💡

If the installation was successful, you are ready to start! To do it, paste some images into a new directory inside the project. By default, the input directory where you should paste the images should be called `input` but you can change it whatever you want in the user settings (see below).

So, for example, to start, create a folder called <code>input</code> in the root directory of the cloned project, and paste some files in .jpg / .jpeg. Then enter the following command:

```
python main.py
```

If everything went well, you will see that a new folder has been created in the root folder of the project (by default called <code>output</code>). If you enter in this folder, you will see that your photos are organized in subfolders by year and month.

### Settings & Customization ⚙️

Fantastic, right? But this is not all, many configuration options are also provided. You can consult your script settings by going to `settings > user_settings.yaml`. To modify this file is recommended to open it with an text editor such as VSCode (download [here](https://code.visualstudio.com/)) with the YAML extension installed:

 <img src="https://user-images.githubusercontent.com/9625760/82730428-7b6fc880-9cf7-11ea-9d81-abee45435a3f.png" alt="YAML extension in VSCode" height="230">

When you open this file with a well-configured text editor like the one mentioned above, when you place your cursor over each setting, you will see a brief description of what it does. You will also have warnings and errors if you type something wrong.

Through this configuration file you can enable or disable which processes you want the program to carry out. For example, you may just want to organize your library without searching for duplicates or fixing metadata.

Precisely the latter is one of the most customizable options, since it allows you to create your own folder and file structure. Thanks to the use of variables, you can group and name some photos, replacing the variable by info of the files. You can use the following variables to name your files/folders:

| Placeholder                                                                                                                  | Where do we find this in the metadata (by order of precedence)                                      |     
| ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | 
| Any of [the standard Python time directives](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior) | EXIF:DateTimeOriginal, XMP:DateTimeOriginal, QuickTime:CreateDate, EXIF:CreateDate, EXIF:ModifyDate |  
| Camera Make                                                                                                                  | EXIF:Make, QuickTime:Make                                                                           |  
| Camera Model                                                                                                                 | EXIF:Model, QuickTime:Model                                                                         |   
| Software                                                                                                                     | EXIF: Software                                                                                      |

So, the string `IMG_%y_%m` will create file/folder names like `IMG_2020_03`, `IMG_2021_11`...

## Want to collaborate? 🙋🏻

Feel free to improve and optimize the existing code. To contribute to the project, read the previous points carefully and do the next steps with the project:

1. Fork it (<https://github.com/enrique-lozano/Image-organizer/fork>)
2. Create your feature branch (`git checkout -b feature/newFeature`)
3. Commit your changes (`git commit -am 'Add some newFeature'`)
4. Push to the branch (`git push origin feature/newFeature`)
5. Create a new Pull Request

## Need help ❓

Feel free to contact the developer if you have any questions or suggestions about the project or how you can help with it.
