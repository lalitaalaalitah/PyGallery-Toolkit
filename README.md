# Image organizer 📂🖼️​​

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

Fantastic, right? But this is not all, many configuration options are also provided. You can consult your script settings by going to `settings > user_settings.yaml`. To modify this file is recommended to open it with an text editor such as VSCode (download [here](https://code.visualstudio.com/)) with the YAML extension installed.

When you open this file with a well-configured text editor like the one mentioned above, when you place your cursor over each setting, you will see a brief description of what it does:

## Next updates 🔜

- More keys to organize your folders
- Improve application performance (especially in the search for duplicates)
- Improve the way files are deleted, giving the user greater control

## Issues 🤕

- Creation date modification based on filename is not working correctly, making some files to not be organized correctly (<a href="https://github.com/enrique-lozano/Image-organizer/issues/1#issue-1437213445">more info</a>)

## Want to collaborate? 🙋🏻

Feel free to improve and optimize the existing code. To contribute to the project, read the previous points carefully and do the next steps with the project:

1. Fork it (<https://github.com/enrique-lozano/Image-organizer/fork>)
2. Create your feature branch (`git checkout -b feature/newFeature`)
3. Commit your changes (`git commit -am 'Add some newFeature'`)
4. Push to the branch (`git push origin feature/newFeature`)
5. Create a new Pull Request

## Need help ❓

Feel free to contact the developer if you have any questions or suggestions about the project or how you can help with it.
