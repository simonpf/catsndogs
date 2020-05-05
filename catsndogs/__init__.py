import os
import glob
from catsndogs.data import training_dir, is_cat, is_dog

dogs = os.path.join(training_dir, "dog")
cats = os.path.join(training_dir, "cat")

def plot_samples(axes=None,
                 n=4):
    import matplotlib.pyplot as plt
    import numpy as np
    from skimage import io

    m = 2
    cats = glob.glob(os.path.join(training_dir, "cat", "*.jpg"))
    dogs = glob.glob(os.path.join(training_dir, "dog", "*.jpg"))

    if axes is None:
        f, axes = plt.subplots(m, n, figsize=(n*2, m*2))
    else:
        f = axes.figure()

    for i in range(n):
        ax = axes[0, i]
        img = io.imread(np.random.choice(cats))
        ax.imshow(img)
        ax.set_title("({}) A cat".format(chr(ord("a") + i)), loc="left")
        ax.set_xticks([])
        ax.set_yticks([])

    for i in range(n):
        ax = axes[1, i]
        img = io.imread(np.random.choice(dogs))
        ax.imshow(img)
        ax.set_title("({}) A dog".format(chr(ord("e") + i)), loc="left")
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
