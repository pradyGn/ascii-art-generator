import os
import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

ASCII_CHARS = ' .,-?*@#'

def detect_cont_string(ascii_line_str):
    """
    Returns the positions of a continous non-blank string.

    Args:
        ascii_line_str (str): Single line of an ascii art str

    Returns:
        (List[List[int, int]]): Start and end position of the continous non-blank string.
    """

    str_pos_lis = []
    for i, c in enumerate(ascii_line_str):
        if c != " ":
            str_pos_lis.append(i)
    
    if len(str_pos_lis) == 0:
        return str_pos_lis
    
    str_grp_lis = [[str_pos_lis[0]]]
    for i, v in enumerate(str_pos_lis):
        if i != 0:
            if v - 1 != str_pos_lis[i-1]:
                str_grp_lis[-1].append(str_pos_lis[i-1])
                str_grp_lis.append([v])
    
    str_grp_lis[-1].append(str_pos_lis[-1])
    
    return str_grp_lis

def image_to_ascii(image, introduction_str, width:int=80):
    """
    Convert an image to ASCII characters.

    Args:
        image (ImageFile): PIL Image object
        width (int): Desired output width

    Returns:
        (str): ASCII art as string
    """
    # Calculate aspect ratio and set new height
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width * 0.5)

    # Resize the image
    image = image.resize((width, new_height))
    
    # Convert to grayscale
    gray_image = image.convert("L")
    # display(gray_image)

    # Convert pixels to ASCII
    pixels = np.array(gray_image)
    max_pixel = max([max(row) for row in pixels])
    min_pixel = min([min(row) for row in pixels])
    sep = int((max_pixel - min_pixel)/len(ASCII_CHARS))


    # introduction_str = "hello_fellow_data_scientis__i_am_pradyuman__"
    len_introduction_str = len(introduction_str)
    ascii_str = ""
    for row in pixels:
        cur_introduction_str = ""; str_to_add = ""
        for pixel in row:
            str_to_add += ASCII_CHARS[min(pixel // sep, pixel // 40)]
        
        str_grp_lis = detect_cont_string(ascii_line_str = str_to_add)
        prev_end = 0
        if len(str_grp_lis) != 0:
            for grp in str_grp_lis:
                cur_introduction_str += " "*(grp[0] - prev_end)
                prev_end = grp[1]

                ratio_nbs_intro_str = (grp[1] - grp[0])/len_introduction_str
                cur_introduction_str += int(ratio_nbs_intro_str)*introduction_str

                remainder = ratio_nbs_intro_str - int(ratio_nbs_intro_str)
                cur_introduction_str += introduction_str[:int(len_introduction_str*remainder)]

                introduction_str = introduction_str[int(len_introduction_str*remainder):] + introduction_str[:int(len_introduction_str*remainder)]
            cur_introduction_str += " "*(len(str_to_add) - str_grp_lis[-1][-1])
            str_to_add = cur_introduction_str

        ascii_str += "".join(str_to_add) + "\n"

    return ascii_str

def extract_frames_from_gif(gif_path):
    """
    Extract frames from a GIF and return them as a list of PIL images.
    
    Args:
        gif_path (str): Path to the GIF file

    Return:
        (List[ImageFile]): List of PIL Image objects
    """
    frames = []
    image = Image.open(gif_path)

    try:
        while True:
            frame = image.convert("RGB")
            frames.append(frame)
            image.seek(image.tell() + 1)  # Move to next frame
    except EOFError:
        pass

    return frames

def play_ascii_animation(frames, frame_delay=0.1, width=80):
    """
    Play the ASCII animation in the terminal.
    :param frames: List of PIL images
    :param frame_delay: Time delay between frames
    :param width: Desired output width
    """
    try:
        for frame in frames:
            os.system("cls" if os.name == "nt" else "clear")
            introduction_str = "hello_fellow_data_scientis__i_am_pradyuman__"
            ascii_frame = image_to_ascii(frame, introduction_str, width)
            print(ascii_frame)
            time.sleep(frame_delay)
    except KeyboardInterrupt:
        print("\nAnimation stopped.")

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: python gif_to_ascii.py <path_to_gif>")
    #     sys.exit(1)

    # gif_path = sys.argv[1]

    # if not os.path.exists(gif_path):
    #     print(f"Error: File '{gif_path}' not found.")
    #     sys.exit(1)

    print("Extracting frames...")
    frames = extract_frames_from_gif("./data/star.gif")

    print("Playing ASCII animation...")
    play_ascii_animation(frames)