import os
import glob
from catsndogs.data import get_training_data
folder = get_training_data()
cats = glob.glob(os.path.join(get_training_data(), "cat", "*.jpg"))
dogs = glob.glob(os.path.join(get_training_data(), "dog", "*.jpg"))
