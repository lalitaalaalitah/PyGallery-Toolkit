# Duplicates remover 🗑️

Identify and remove duplicate or similar images from your collection.

## Description 📝

The duplicates_remover.py script helps you clean up your image collection by identifying and optionally removing duplicate or similar images. It uses a hashing algorithm to detect similarities between images based on their content.

## Usage 💡

To run the script, use the following command:

```
python duplicates_remover.py input_path --arg1 --arg2 ...
```

### Arguments

- **input_path (required)**: Absolute path to the images to process.

- **--hash_size**: Used for identification of similar images. Larger values provide more exhaustive search but slower performance. Setting it to 0 skips the search for duplicates/similar images altogether. Default is 16.

- **-s, --similarity**: Similarity threshold of the images that will trigger an action. It is a number from 0 to 100, with 100 indicating only completely identical images trigger action. This parameter does not affect the speed of the process like hash_size.

- **--plot_disabled**: Disable image display before confirming removal. By default, images are displayed for confirmation before removal.

- **-c, --copy**: Copy files instead of moving. Note that moving is generally faster than copying, specially with big files.

- **--recursive**: Whether we should search for files in subdirectories of the input directory. Default is True.

- **-v, --verbose**: Enable verbose output.

## Important notes ⚠️

- Make sure the `input_path` is an absolute path.
- Use caution when adjusting `hash_size` and `similarity` to balance accuracy and performance.

## Examples 🛠️

### Basic Example

Remove duplicate or similar images from the "C:/users/your_user/images" directory:

```
python duplicates_remover.py "C:/users/your_user/images"
```

### Adjusting Hash Size and Similarity

Use a larger hash size and stricter similarity threshold:

```
python duplicates_remover.py "C:/users/your_user/images" --hash_size 32 --similarity 98
```

### Disable Image Display

Remove duplicates without displaying images for confirmation:

```
python duplicates_remover.py "C:/users/your_user/images" --similarity 96 --plot_disabled
```

### Verbose Output

Use the `--verbose` fag anywhere to enable an output with more detailed logs:

```
python duplicates_remover.py "C:/users/your_user/images" --similarity 96 --verbose
```
