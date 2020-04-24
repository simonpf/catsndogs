import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from skimage import io

from catsndogs.data import training_dir, is_cat, is_dog

dogs = os.path.join(training_dir, "dog")
cats = os.path.join(training_dir, "cat")

def plot_samples(axes=None,
                 n=4):

    m = 2
    files = glob.glob(os.path.join(training_dir, "*.jpg"))
    cats = [f for f in files if is_cat(f)]
    dogs = [f for f in files if is_dog(f)]

    if axes is None:
        f, axes = plt.subplots(m, n, figsize=(n*2, m*2))
    else:
        f = axes.figure()

    for i in range(n):
        ax = axes[0, i]
        img = io.imread(np.random.choice(cats))
        ax.imshow(img)
        ax.set_title("({}) A cat".format(chr(ord("a") + i)))

    for i in range(n):
        ax = axes[1, i]
        img = io.imread(np.random.choice(dogs))
        ax.imshow(img)
        ax.set_title("({}) A dog".format(chr(ord("a") + i)))

    plt.tight_layout()
