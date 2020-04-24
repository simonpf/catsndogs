"""
This sub-module implements functionality to process the original
Oxford-IIIT Pet Dataset and produce a dataset with smaller and centered
images.
"""
import glob
import os
import re
import shutil
import xmltodict
import PIL
import PIL.Image

################################################################################
# Extract images from Oxford dataset.
################################################################################

def extract_bounding_box(annotation):
    """
    Extract bounding box from annotation file.

    Args:
        annotation: Filename of the .xml file cotaining the annotations
    Return:
        Tuple (xmin, ymin, xmax, ymax) representing the bounding box around
        the cat or dog.
    """
    dct = xmltodict.parse(open(annotation, "r").read())

    obj = dct["annotation"]["object"]
    if type(obj) == list:
        obj = obj[0]

    xmin = obj["bndbox"]["xmin"]
    ymin = obj["bndbox"]["ymin"]
    xmax = obj["bndbox"]["xmax"]
    ymax = obj["bndbox"]["ymax"]
    return (int(xmin), int(ymin), int(xmax), int(ymax))

class Image:
    """
    The Image class represents an image from the original dataset
    combined with the bounding box around the head of the animal.
    """
    def __init__(self,
                 image,
                 annotation):
        """
        Args:
            image: Filename of the image file
            annotation: Filename of the corresponding annotation
                file.
        """
        self.filename = image
        self.bounding_box = extract_bounding_box(annotation)

    @property
    def data(self):
        """
        Return image as PIL.Image
        """
        return PIL.Image.open(self.filename)

    @property
    def roi(self):
        """
        Return image centered around bounding box.
        """
        image = PIL.Image.open(self.filename)
        w, h = image.size
        xmin, ymin, xmax, ymax = self.bounding_box
        dx = min(xmin, w - xmax)
        dy = min(ymin, h - ymax)
        d = min(dx, dy)
        return image.crop((xmin - d, ymin -d, xmax + d, ymax + d))

    @property
    def roi_resized(self):
        """
        Centered and resized image.
        """
        roi = self.roi
        return roi.resize((128, 128))

class RawData:
    """
    Class representing the data of the original dataset. Provides
    access to annotated images in the dataset.
    """
    def __init__(self, path):
        self.image_path = os.path.join(path, "images")
        self.images = glob.glob(os.path.join(self.image_path, "*.jpg"))
        self.images.sort()
        self.annotation_path = os.path.join(path, "annotations", "xmls")
        self.annotations = glob.glob(os.path.join(self.annotation_path, "*xml"))
        self.annotations.sort()

    def __len__(self):
        """
        Number of available annotations.
        """
        return(len(self.annotations))

    def __getitem__(self, index):
        """
        Get image from dataset.
        """
        index = index % len(self)
        annotation = self.annotations[index]
        name, _ = os.path.splitext(os.path.basename(annotation))
        image = os.path.join(self.image_path, name + ".jpg")
        return Image(image, annotation)

################################################################################
# Splitting data
################################################################################
filename_pattern = re.compile("([\S]*)_([\d]*).jpg")

def read_classes(input_folder):
    """
    Read images from folders and sort into dict according to classes.

    Args:
        input_folder: Directory containing the Oxford-III Pet images.

    Returns: Dict with class names as keys and list of filenames of
        corresponding images as entries.
    """
    classes = {}
    files = glob.glob(os.path.join(os.path.expanduser(input_folder), "*.jpg"))
    for f in files:
        match = filename_pattern.match(os.path.basename(f))
        c = match.group(1)
        if not c in classes:
            classes[c] = []
        classes[c] += [f]
    return classes


def split_data(input_folder, training_folder, test_folder, split=0.8):
    """
    Split data sequentially into training and data.

    Args:
        input_folder: The folder containing the input images.
        training_folder: Folder in which to store the training images.
        test_folder: Folder in which to store the test images.
        split: Ratio between the number of images used for training
            and those used for testing.
    """
    training_folder = os.path.expanduser(training_folder)
    test_folder = os.path.expanduser(test_folder)

    if not os.path.exists(training_folder):
        try:
            os.makedirs(training_folder)
            os.makedirs(os.path.join(training_folder, "cat"))
            os.makedirs(os.path.join(training_folder, "dog"))
        except:
            pass

    if not os.path.exists(test_folder):
        try:
            os.makedirs(test_folder)
            os.makedirs(os.path.join(test_folder, "cat"))
            os.makedirs(os.path.join(test_folder, "dog"))
        except:
            pass

    classes = read_classes(input_folder)
    for c in classes:
        files = classes[c]
        if c[0].isupper():
            f_train = os.path.join(training_folder, "cat")
            f_test = os.path.join(test_folder, "cat")
        else:
            f_train = os.path.join(training_folder, "dog")
            f_test = os.path.join(test_folder, "dog")

        n = int(split * len(files))
        for f in files[:n]:
            out = os.path.join(f_train, os.path.basename(f))
            shutil.copyfile(f, out)
        for f in files[n:]:
            out = os.path.join(f_test, os.path.basename(f))
            shutil.copyfile(f, out)
