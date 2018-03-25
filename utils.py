from PIL import ImageOps


def get_map(image):
    image_ = image.convert(mode='L')
    image_ = ImageOps.invert(image_)
    matrix = []
    for i in range(image_.height):
        row = []
        for j in range(image_.width):
            row.append(image_.getpixel((j, i)) / 64)
        matrix.append(row)
    return matrix
