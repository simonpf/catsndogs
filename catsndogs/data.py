from appdirs import AppDirs
import requests
import tarfile
import os

app_dirs = AppDirs("catsndogs", "simonpf")
training_dir = os.path.join(app_dirs.user_data_dir, "training_data")
test_dir = os.path.join(app_dirs.user_data_dir, "test_data")

def is_cat(file):
    """
    Args:
        Image filename.
    Returns:
        Whether the image contains a cat.

    """
    return os.path.basename(file)[0].isupper()

def is_dog(file):
    """
    Args:
        Image filename.
    Returns:
        Whether the image contains a dog.
    """
    return not is_cat(file)

def download_training_data():
    """
    Download and extract  training data and store to the user's local data directory.
    """
    filename = os.path.join(app_dirs.user_data_dir, "training_data.tar.gz")

    if not os.path.exists(app_dirs.user_data_dir):
        os.makedirs(app_dirs.user_data_dir)

    # Download data
    training_url = "http://spfrnd.de/datasets/catsndogs/training_data.tar.gz"
    r = requests.get(training_url)
    with open(filename, "wb") as ds:
        for chunk in r.iter_content(chunk_size=128):
            ds.write(chunk)

    # Extract
    tar = tarfile.open(filename)
    tar.extractall(path=app_dirs.user_data_dir)

    os.remove(filename)

def download_test_data():
    """
    Download and extract  test data and store to the user's local data directory.
    """
    filename = os.path.join(app_dirs.user_data_dir, "test_data.tar.gz")

    if not os.path.exists(app_dirs.user_data_dir):
        os.makedirs(app_dirs.user_data_dir)

    # Download data
    test_url = "http://spfrnd.de/datasets/catsndogs/test_data.tar.gz"
    r = requests.get(test_url)
    with open(filename, "wb") as ds:
        for chunk in r.iter_content(chunk_size=128):
            ds.write(chunk)

    # Extract
    tar = tarfile.open(filename)
    tar.extractall(path=app_dirs.user_data_dir)

    os.remove(filename)

def get_training_data():
    """
    If necessary, downloads training data and
    returns directory containing training data.
    """

    if not os.path.exists(training_dir):
        download_training_data()
    return training_dir

def get_test_data():
    """
    If necessary, downloads test data and
    returns directory containing test data.
    """
    if not os.path.exists(test_dir):
        download_test_data()
    return test_dir
