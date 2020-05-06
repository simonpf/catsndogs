import catsndogs.test
import catsndogs.training
import pytest
import glob
import os

def test_test_data():
    folders = glob.glob(os.path.join(catsndogs.test.folder, "*"))
    assert(len(folders) == 2)
    assert(len(catsndogs.test.cats) == 239)
    assert(len(catsndogs.test.dogs) == 500)

def test_training_data_data():
    folders = glob.glob(os.path.join(catsndogs.training.folder, "*"))
    assert(len(folders) == 2)
    assert(len(catsndogs.training.cats) == 949)
    assert(len(catsndogs.training.dogs) == 1998)


