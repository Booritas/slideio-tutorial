import json
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
import math
import numpy as np
import plotly.graph_objects as go
import slideio
import pandas as pd


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
            driver_images.append(image)
    return driver_images
            
            

def display_test_image_info(dictionary):
    table = "<table style='border-collapse: collapse'><tr><th style='text-align: left; border: 1px solid black'>{}</th><th style='border: 1px solid black'>{}</th></tr>{}</table>"
    row_strings = ""
    for image in dictionary:
        row_strings += "<tr><td style='text-align: left; border: 1px solid black'>{}</td><td style='font-weight: bold; border: 1px solid black'>{}</td></tr>".format(image["path"], image["driver"])
    html = table.format("Image Path", "Driver", row_strings)
    display(HTML(html))
    
def display_driver_test_image_info(image_list, driver, show_options=False):
    th = "<th style='text-align: left; border: 1px solid black'>{}</th>"
    tdf = "<td style='text-align: left; border: 1px solid black'>{}</td>"
    if show_options:
        table = f"<table style='border-collapse: collapse'><tr>{th}{th}{th}</tr>{{}}</table>"
    else:
        table = f"<table style='border-collapse: collapse'><tr>{th}{th}</tr>{{}}</table>"
    row_strings = ""
    for image_element in image_list:
        image = tdf.format(image_element["path"])
        driver = tdf.format(image_element["driver"])
        options = tdf.format("")
        if "options" in image_element:
            options = tdf.format(image_element["options"])
        if show_options:
            row_strings += "<tr>{}{}{}</tr>".format(image, driver,options)
        else:
            row_strings += "<tr>{}{}</tr>".format(image, driver)
    if show_options:
        html = table.format("Image Path", "Driver", "Options",row_strings)
    else:
        html = table.format("Image Path", "Driver", row_strings)
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

    # Check if the image has a single channel
    if image.ndim == 2:
        # Convert single-channel image to grayscale
        image = plt.cm.gray(image)

    fig, ax = plt.subplots(figsize=(new_width / 100, new_height / 100))
    ax.imshow(image)
    ax.axis('off')
    plt.show()

def convert_to_8bit(image):
    arr_normalized = (image - image.min()) / (image.max() - image.min())
    arr_8bit = (255 * arr_normalized).astype(np.uint8)
    return arr_8bit
    
def show_images(images, titles, max_size, columns=4):
    num_images = len(images)
    rows = math.ceil(num_images / columns)
    fig, axes = plt.subplots(rows, columns, figsize=(max_size * columns / 100, max_size * rows / 100))
    axes = axes.flatten()  # Flatten the axes array for easier indexing

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

        # Convert image to grayscale if it has only one channel
        if len(image.shape) == 2:
            image = np.dstack((image,) * 3)
        image = convert_to_8bit(image)
        axes[i].imshow(image)
        axes[i].axis('off')

        if titles is not None:
            axes[i].set_title(titles[i], fontproperties=font)

    # Hide empty subplots
    for j in range(num_images, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()  # Adjust spacing between subplots
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
        slice_count = scene.num_z_slices
        slice = 0
        if slice_count>1:
            slice = slice_count//2
        row_count += 1
        if channel_count>3:
            image = scene.read_block(size=(thw,0), channel_indices=[0,1,2], slices=(slice,slice+1))
        elif channel_count==2:
            image = scene.read_block(size=(thw,0), channel_indices=[0], slices=(slice,slice+1))
        else:
            image = scene.read_block(size=(thw,0))
        image_row = row_count//cols
        image_col = row_count - (image_row*cols)
        plt.subplot2grid((rows,cols),(image_row, image_col))
        if channel_count < 3:
            plt.imshow(image, cmap='gray')
        else:
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

def show_scene_details(scene, size):
    table = create_scene_info_table(scene)
    image = scene.read_block(size=(size,0))
    image_base64 = '<img src="data:image/png;base64,{}">'.format(base64.b64encode(image).decode('utf-8'))
    # Display the HTML table
    display(HTML(image_base64))


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

def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

def show_volume(volume):
    r, c = volume[0].shape
    # Define frames
    nb_frames = volume.shape[0]
    
    fig = go.Figure(frames=[go.Frame(data=go.Surface(
        z=(6.7 - k * 0.1) * np.ones((r, c)),
        surfacecolor=np.flipud(volume[nb_frames - 1 - k]), cmin=0, cmax=200
        ),
        name=str(k) # you need to name the frame for the animation to behave properly
        )
        for k in range(nb_frames)])
    
    # Add data to be displayed before animation starts
    fig.add_trace(go.Surface(
        z=6.7 * np.ones((r, c)),
        surfacecolor=np.flipud(volume[nb_frames-1]),
        colorscale='Gray',
        cmin=0, cmax=200,
        colorbar=dict(thickness=20, ticklen=4)
        ))
    
    sliders = [
                {
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0.1,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[f.name], frame_args(0)],
                            "label": str(k),
                            "method": "animate",
                        }
                        for k, f in enumerate(fig.frames)
                    ],
                }
            ]
    
    # Layout
    fig.update_layout(
             title='Slices in volumetric data',
             width=500,
             height=500,
             scene=dict(
                        zaxis=dict(range=[-0.1, 6.8], autorange=False),
                        aspectratio=dict(x=1, y=1, z=1),
                        ),
             updatemenus = [
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(50)],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
                }
             ],
             sliders=sliders
    )
    fig.show()

def extract_image_properties(images):
    image_infos = []
    for image in images:
        image_info = {}
        slide = slideio.open_slide(image['path'],image['driver'])
        for index in range(0, slide.num_scenes):
            scene = slide.get_scene(index)
            image_info['Path'] = image['path']
            image_info['Scene index'] = index
            image_info['Num Channels'] = scene.num_channels
            image_info['Data Type'] = scene.get_channel_data_type(0)
            image_info['Compression'] = str(scene.compression).replace('Compression.','')
            image_info['Width'] = scene.size[0]
            image_info['Height'] = scene.size[1]
            image_info['Z Slices'] = scene.num_z_slices
            image_info['Z Frames'] = scene.num_t_frames
            image_infos.append(image_info)
    return pd.DataFrame(image_infos)