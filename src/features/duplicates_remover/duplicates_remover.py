import os

from imagehash import ImageHash, average_hash
from PIL import Image
from src.utils.console import bcolors, printProgressBar


def find_file_to_keep(files: list[str]):
    """Finds the file to keep in a list of duplicates/similar files"""
    files.sort(key=len)
    return files[0]


def duplicates_remover(
    filepaths: list[tuple[str, str]], hash_size: int, similarity: int
):
    """Optionally find and remove duplicate images"""

    hashes = {}
    duplicates_imgs: list[tuple[list[str], float]] = []
    similar_imgs: list[list[str]] = []

    files_and_hashes: list[tuple[str, ImageHash]] = []

    print(
        bcolors.BLUE
        + "\u2731"
        + bcolors.ENDC
        + " Preparing for finding duplicates now!\n"
    )

    printProgressBar(
        0, len(filepaths), prefix="Finding duplicates:", suffix="Complete", length=50
    )

    for i, (path, filename) in enumerate(filepaths):

        printProgressBar(
            i + 1,
            len(filepaths),
            prefix="Finding duplicates:",
            suffix="Complete",
            length=50,
        )

        full_path_to_file = os.path.join(path, filename)

        try:
            img = Image.open(full_path_to_file)
        except:
            continue

        if not img:
            continue

        with img:
            try:
                temp_hash = average_hash(img, hash_size)

                if temp_hash:
                    files_and_hashes.append((full_path_to_file, temp_hash))
            except:
                continue

    if similarity > 100:
        similarity = 100
    elif similarity < 0:
        similarity = 0

    threshold = 1 - similarity / 100
    diff_limit = int(threshold * (hash_size**2))

    for i, file1 in enumerate(files_and_hashes):

        duplicates: list[str] = []
        _similarity: float

        for file2 in files_and_hashes[i:]:
            if file1[0] != file2[0]:

                if file1[1] - file2[1] < diff_limit:
                    if len(duplicates) == 0:
                        duplicates.append(file1[0])

                    duplicates.append(file2[0])
                    _similarity = round(
                        100 * ((file1[1] - file2[1]) / hash_size**2), 2
                    )

        already_found = False
        for founded in duplicates_imgs:
            if set(duplicates) <= set(founded[0]):
                already_found = True

        if len(duplicates) > 0 and not already_found:
            duplicates_imgs.append((duplicates, _similarity))

    if len(duplicates_imgs) == 0:
        print(bcolors.GREEN + "\u2714" + bcolors.ENDC + f" No duplicates found!\n")
        return

    else:
        print(
            bcolors.BLUE
            + "\u2731"
            + bcolors.ENDC
            + f" {len(duplicates_imgs)} duplicates found:"
        )

        for images in duplicates_imgs:
            print()
            print(f"Similarity: {100 - images[1]}%:")
            for img in images[0]:
                print(bcolors.BLUE + "-" + bcolors.ENDC + f" {img}")

        print()
        a = input(
            "Do you want to delete these {} Images? Press Y or N:  ".format(
                len(duplicates_imgs)
            )
        )
        space_saved = 0
        if a.strip().lower() == "y":
            for images in duplicates_imgs:
                images[0].remove(find_file_to_keep(images[0]))

                for img in images[0]:
                    space_saved += os.path.getsize(img)

                    os.remove(img)

            print(
                "\n"
                + bcolors.GREEN
                + "\u2714"
                + bcolors.ENDC
                + f" All images deleted succesfully. You saved {round(space_saved / 1000000, 2)}MB of space!"
            )
        else:
            print("Thank you for Using Duplicate Remover")
