import argparse
import os
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont
import subprocess


def is_image(file_path):
    """
    Return True if the file path is a valid image file.
    input: file_path (string)
    output: boolean
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    file_extension = os.path.splitext(file_path)[1].lower()
    return file_extension in image_extensions


if __name__ == '__main__':
    """
    Create a gif from input images.
    Usage:
    create_gif.py --input ./images --output ./new_gif.gif --loop 0 --duration 1000 --add_name True
    Use create_gif.py --help for more information.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, default='./images', help='Input images folder path.')
    parser.add_argument('--output', '-o', type=str, default='./output/new_gif.gif', help='Output image file path.')
    parser.add_argument('--loop', '-l', type=int, default=0, help='Loop count. Set to 0 to enable infinite looping.')
    parser.add_argument('--delay', '-d', type=int, default=1000, help='Duration of the animation in milliseconds.')
    parser.add_argument('--add_name', '-n', type=bool, default=True, help='Add file name to the output image.')
    parser.add_argument('--font_path', '-f', type=str, default='fonts/Montserrat/static/Montserrat-Bold.ttf',
                        help='.ttf font path.')
    parser.add_argument('--font_size', '-s', type=int, default=25, help='Font size.')

    args = parser.parse_args()
    filepath = args.input
    output_filename = args.output
    loop: int = args.loop
    delay: int = args.delay
    add_name = args.add_name

    font=None

    try:
        # Load font
        font = ImageFont.truetype(args.font_path, args.font_size)
    except OSError:
        print("Font not found... Please specify a valid font path.")
        quit(1)

    input_files = []
    try:
        input_files.extend(
            filename for filename in os.listdir(filepath) if is_image(filename)
        )  # Get all images in the input folder
        input_files.sort()
    except FileNotFoundError:
        print("Input folder not found... Please specify a valid input folder.")
        quit(1)

    if not input_files:
        print("No images were found... Please specify a valid input folder.")
        quit(1)

    images = []
    for filename in input_files:
        base_name = os.path.splitext(filename)[0]  # Get the base name without the extension
        image = Image.fromarray(imageio.imread(f'{filepath}/{filename}'))  # Convert to PIL Image
        if add_name:
            # Add file name - especially useful for files named as years
            draw = ImageDraw.Draw(image)
            draw.text((50, 50), base_name, font=font, fill=(0, 0, 0))
        images.append(image)

    try:
        if os.path.splitext(output_filename)[1] != '.gif':
            print("Output file extension must be '.gif'. This has been automatically added.")

        imageio.mimsave(
            uri=f'{os.path.splitext(output_filename)[0]}.gif',
            ims=images,
            loop=loop,
            duration=delay,
        )

    except ValueError:
        print("Something went wrong... Your output filepath may be invalid.")
        quit(2)

    print(
        f"Done! New gif can be found at {os.path.splitext(output_filename)[0]}.gif"
    )
    quit(0)
