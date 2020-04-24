import os
import glob
from catsndogs.data import get_test_data
folder = get_test_data()
cats = glob.glob(os.path.join(get_test_data(), "cat", "*.jpg"))
dogs = glob.glob(os.path.join(get_test_data(), "dog", "*.jpg"))
