import json
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def get_test_images():
    file_path = 'images.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_driver_test_images(driver):
    driver_images = []
    images = get_test_images()
    for image in images:
        if image["driver"] == driver:
            driver_images.append(image["path"])
    return driver_images
            
            

def display_test_image_info(dictionary):
    table = "<table style='border-collapse: collapse'><tr><th style='text-align: left; border: 1px solid black'>{}</th><th style='border: 1px solid black'>{}</th></tr>{}</table>"
    rows = ""
    for image in dictionary:
        rows += "<tr><td style='text-align: left; border: 1px solid black'>{}</td><td style='font-weight: bold; border: 1px solid black'>{}</td></tr>".format(image["path"], image["driver"])
    html = table.format("Image Path", "Driver", rows)
    display(HTML(html))
    
def show_image(image, max_size):
    width, height = image.shape[1], image.shape[0]
    aspect_ratio = width / height

    if width > height:
        new_width = max_size
        new_height = int(max_size / aspect_ratio)
    else:
        new_height = max_size
        new_width = int(max_size * aspect_ratio)

    fig, ax = plt.subplots(figsize=(new_width / 100, new_height / 100))
    ax.imshow(image)
    ax.axis('off')
    plt.show()
    

def show_images(images, titles, max_size):
    num_images = len(images)
    fig, axes = plt.subplots(1, num_images, figsize=(max_size * num_images / 100, max_size / 100))

    font = FontProperties(weight='bold', size='x-large')

    for i, image in enumerate(images):
        width, height = image.shape[1], image.shape[0]
        aspect_ratio = width / height

        if width > height:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        axes[i].imshow(image)
        axes[i].axis('off')

        if titles is not None:
            axes[i].set_title(titles[i], fontproperties=font)

    plt.show()