import json
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

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
    
import matplotlib.pyplot as plt

def show_image(image, max_size):
    width, height = image.shape[1], image.shape[0]
    aspect_ratio = width / height

    if width > height:
        new_width = max_size
        new_height = int(max_size / aspect_ratio)
    else:
        new_height = max_size
        new_width = int(max_size * aspect_ratio)

    # Check if the image has a single channel
    if image.ndim == 2:
        # Convert single-channel image to grayscale
        image = plt.cm.gray(image)

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

def delete_file(file_path):
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def show_scenes(scenes, cols, thumbnail_size):
    dpi = 80
    thw = thumbnail_size[0]
    scene_count = len(scenes)
    print(f"Number of scenes: {scene_count}")
    rows = (scene_count - 1)//cols + 1
    figsize = (cols*thumbnail_size[0]//dpi, rows*thumbnail_size[1]//dpi)
    plt.figure(figsize=figsize,dpi=dpi)
    row_count = -1
    for index in range(scene_count):
        scene = scenes[index]
        channel_count = scene.num_channels
        row_count += 1
        if channel_count>3:
            image = scene.read_block(size=(thw,0), channel_indices=[0,1,2])
        elif channel_count==2:
            image = scene.read_block(size=(thw,0), channel_indices=[0])
        else:
            image = scene.read_block(size=(thw,0))
        image_row = row_count//cols
        image_col = row_count - (image_row*cols)
        plt.subplot2grid((rows,cols),(image_row, image_col))
        plt.imshow(image)
        plt.xticks([])
        plt.yticks([])
        plt.title(f"{scene.file_path}")
    plt.tight_layout()
    plt.show()    

def create_scene_info_table(scene):
    table = "<table style='border-collapse: collapse;'>"
    
    # Add table header row
    table += "<tr>"
    table += "<th style='border: 1px solid black; padding: 8px; text-align: left;'>Property</th>"
    table += "<th style='border: 1px solid black; padding: 8px; text-align: left;'>Value</th>"
    table += "</tr>"
    
    # Create rows for each property
    for property_name, value in [
        ("Name", scene.name),
        ("File Path", scene.file_path),
        ("Size (Width, Height)", scene.size),
        ("Number of Channels", scene.num_channels),
        ("Compression", scene.compression),
        ("Data Type", scene.get_channel_data_type(0)),
        ("Magnification", scene.magnification),
        ("Resolution", scene.resolution),
        ("Z-Resolution", scene.z_resolution),
        ("Time Resolution", scene.t_resolution),
        ("Number of Z-Slices", scene.num_z_slices),
        ("Number of Time Frames", scene.num_t_frames)
    ]:
        table += "<tr>"
        table += "<td style='border: 1px solid black; padding: 8px; text-align: left;'>{}</td>".format(property_name)
        table += "<td style='border: 1px solid black; padding: 8px; text-align: left;'>{}</td>".format(value)
        table += "</tr>"

    table += "</table>"
    return table
    
def show_scene_info(scene):
    table = create_scene_info_table(scene)
    # Display the HTML table
    display(HTML(table))

def show_scene_info_tablesN(scenes):
    table_html = ""
    
    # Create a table for each scene
    for scene in scenes:
        table_html += "<div style='display: inline-block; margin-right: 20px;'>"
        table_html += create_scene_info_table(scene)
        table_html += "</div>"
    
    # Display the HTML tables
    from IPython.display import display, HTML
    display(HTML(table_html))

def show_scene_info_tables(scenes):
    table_html = "<table style='border-collapse: collapse;'><tr>"
    
    # Create a table for each scene
    for scene in scenes:
        table_html += "<td>" + create_scene_info_table(scene) + "</td>"
    
    table_html += "</tr></table>"
    
    # Display the HTML table
    display(HTML(table_html))

def create_output_file_path(file_path):
    folder = "temp"
    file_name, extension = os.path.splitext(file_path)
    modified_path = os.path.join(".", folder, file_name.split("/")[-1] + ".svs")
    return modified_path
