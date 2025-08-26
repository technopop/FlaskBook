import torchvision.transforms.functional as F


def image_to_tensor(image):
    image_tensor = F.to_tensor(image)
    return image_tensor
