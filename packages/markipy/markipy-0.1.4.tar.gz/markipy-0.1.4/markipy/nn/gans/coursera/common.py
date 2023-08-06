from torch import nn
from torchvision.utils import make_grid

import matplotlib.pyplot as plt

from markipy import makedirs


def show_tensor_images(image_tensor, num_images=25, size=(1, 28, 28), filename=None):
    '''
    Function for visualizing images: Given a tensor of images, number of images, and
    size per image, plots and prints the images in an uniform grid.
    '''
    image_tensor = (image_tensor + 1) / 2
    image_unflat = image_tensor.detach().cpu()
    image_grid = make_grid(image_unflat[:num_images], nrow=5)
    plt.imshow(image_grid.permute(1, 2, 0).squeeze())
    if filename is not None:
        # Image results
        images_path = '/tmp/coursera/mnist/week3/'
        makedirs(images_path)
        plt.savefig(filename, format='jpg')
    else:
        plt.show()


def make_grad_hook():
    '''
    Function to keep track of gradients for visualization purposes,
    which fills the grads list when using model.apply(grad_hook).
    '''
    grads = []

    def grad_hook(m):
        if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
            grads.append(m.weight.grad)

    return grads, grad_hook
