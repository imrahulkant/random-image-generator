#!/usr/bin/env python


import argparse
import random
import sys
from PIL import Image
from random_art import create_expression, run_expression


def generate_monochrome_image(expression,
                              width=450,
                              height=450,
                              min_intensity=0,
                              max_intensity=255):
    
    def convert_coords(x, y):
        
        width_unit = width / 2
        height_unit = height / 2
        rx = (x - width_unit) / width_unit
        ry = (y - height_unit) / height_unit
        return (rx, ry)

    def scale_intensity(rel_intensity):
        multiplier = (max_intensity - min_intensity) / 2
        return int((rel_intensity + 1) * multiplier) + min_intensity

    image = Image.new("L", (width, height))

    
    for py in range(height):
        for px in range(width):
            x, y = convert_coords(px, py)
            expr_value = run_expression(expression, x, y)
            intensity = scale_intensity(expr_value)
            image.putpixel((px, py), intensity)

    return image


def generate_rgb_image(red_exp, green_exp, blue_exp, width=450, height=450):
    red_image = generate_monochrome_image(
        red_exp, width, height, max_intensity=random.triangular(1, 255, 220))
    green_image = generate_monochrome_image(
        green_exp, width, height, max_intensity=random.triangular(1, 255, 220))
    blue_image = generate_monochrome_image(
        blue_exp, width, height, max_intensity=random.triangular(1, 255, 220))
    return Image.merge("RGB", (red_image, green_image, blue_image))


def generate_cmyk_image(cyan_exp,
                        magenta_exp,
                        yellow_exp,
                        black_exp,
                        width=450,
                        height=450):
    cyan_image = generate_monochrome_image(
        cyan_exp, width, height, max_intensity=random.randint(150, 255))
    magenta_image = generate_monochrome_image(
        magenta_exp, width, height, max_intensity=random.randint(150, 255))
    yellow_image = generate_monochrome_image(
        yellow_exp, width, height, max_intensity=random.randint(150, 255))
    black_image = generate_monochrome_image(
        black_exp, width, height, max_intensity=random.randint(1, 50))
    return Image.merge("CMYK",
                       (cyan_image, magenta_image, yellow_image, black_image))


def make_gray(seed, num_pics=1, width=450, height=450):
    
    random.seed(seed)
    for i in range(num_pics):
        filename = "image-{1}.png".format(seed, i)
        gray_exp = create_expression()
        print("{}: {}".format(filename, gray_exp))
        image = generate_monochrome_image(gray_exp, width, height)
        image.save(filename, "PNG")


def make_rgb(seed, num_pics=1, width=450, height=450):
    
    random.seed(seed)
    for i in range(num_pics):
        filename = "image-{1}.png".format(seed, i)
        red_exp = create_expression()
        green_exp = create_expression()
        blue_exp = create_expression()
        print("{}:\n  red: {}\n  green: {}\n  blue: {}".format(
            filename, red_exp, green_exp, blue_exp))
        image = generate_rgb_image(red_exp, green_exp, blue_exp, width, height)

        image.save(filename, "PNG")


def make_cmyk(seed, num_pics=1, width=450, height=450):
    
    random.seed(seed)
    for i in range(num_pics):
        filename = "image-{1}.png".format(seed, i)
        cyan_exp = create_expression()
        magenta_exp = create_expression()
        yellow_exp = create_expression()
        black_exp = create_expression()
        print(
            "{}:\n  cyan: {}\n  magenta: {}\n  yellow: {}\n  black: {}".format(
                filename, cyan_exp, magenta_exp, yellow_exp, black_exp))
        image = generate_cmyk_image(cyan_exp, magenta_exp, yellow_exp,
                                    black_exp, width, height).convert("RGB")
        image.save(filename, "PNG")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create random art.')
    parser.add_argument(
        '-S',
        '--seed',
        type=int,
        help="Set the seed for the random number generator.")
    parser.add_argument(
        '-s',
        '--size',
        type=str,
        default='450',
        help="Number of pixels for each side of the square.")
    parser.add_argument(
        '-n', '--number', type=int, default=1, help="Generate N images.")
    parser.add_argument(
        '--rgb', action='store_true', help="Generate RGB images (default).")
    parser.add_argument(
        '--gray', action='store_true', help="Generate grayscale images.")
    parser.add_argument(
        '--cmyk', action='store_true', help="Generate CMYK images.")

    args = parser.parse_args()
    if not (args.rgb or args.gray or args.cmyk):
        args.rgb = True

    if args.seed:
        seed = args.seed
    else:
        seed = random.randint(0, sys.maxsize)

    random.seed(seed)
    print("Seed: {}".format(seed))

    if args.size.isdigit():
        width = int(args.size)
        height = int(args.size)
    elif args.size and "x" in args.size:
        width, height = [int(n) for n in args.size.split("x")]
    else:
        width = height = 450

    if args.cmyk:
        make_cmyk(seed, args.number, width, height)

    if args.rgb:
        make_rgb(seed, args.number, width, height)

    if args.gray:
        make_gray(seed, args.number, width, height)
