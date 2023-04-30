import sys
import argparse
from PIL import Image, ImageDraw
import random


def create_canvas(width, height):
    return Image.new("RGBA", (width, height), (0, 0, 0, 0))

def generate_color(hex_color, min_size, max_size, dot_size):
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    alpha = int(255 * (dot_size - min_size) / (max_size - min_size))
    return (r, g, b, alpha)

class Dot:
    def __init__(self, x, y, size, speed, color, shape, direction, zigzag_direction, line_length=None):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.shape = shape
        self.direction = direction
        self.line_length = line_length
        self.zigzag_direction = zigzag_direction

def create_dots(shape_ratios, shape_colors, num_dots, min_size, max_size, width, height_range, num_frames, direction):
    dots = []
    total_ratio = sum(shape_ratios.values())

    for _ in range(num_dots):
        x = random.randint(0, width - max_size)
        y = random.randint(0, height_range - max_size)
        size = random.randint(min_size, max_size)
        if direction in {"left", "right"}:
            speed = width / num_frames
        else:
            speed = height_range / num_frames * random.randint(1, 3)
        line_length = int(speed * 1.5)

        random_value = random.uniform(0, total_ratio)
        current_sum = 0
        for shape, ratio in shape_ratios.items():
            current_sum += ratio
            if random_value <= current_sum:
                break

        color = generate_color(shape_colors[shape], min_size, max_size, size)
        zigzag_direction = random.choice(["left", "right"])
        if direction in {"left", "right"}:
            zigzag_cycle_frames = max(2, num_frames - 1)
        else:
            zigzag_cycle_frames = random.randint(num_frames // 50, num_frames // 40)
            zigzag_cycle_frames = max(2, zigzag_cycle_frames)
        initial_phase = random.uniform(0, 1) 
        dot = Dot(x, y, size, speed, color, shape, direction, zigzag_direction, line_length=line_length if shape == "line" else None)
        dot.initial_phase = initial_phase
        dot.zigzag_cycle_frames = zigzag_cycle_frames
        dots.append(dot)

    return dots





def create_frames(num_frames, width, height, dots):
    frames = []
    for i in range(num_frames):
        canvas = create_canvas(width, height)
        draw = ImageDraw.Draw(canvas)
        for dot in dots:
            for offset in range(0, height, height_range):
                y_with_offset = (dot.y + i * dot.speed + offset) % height

                if dot.direction == "left":
                    x_with_offset = (dot.x - int(i * dot.speed)) % width
                elif dot.direction == "right":
                    x_with_offset = (dot.x + int(i * dot.speed)) % width
                elif dot.direction == "zigzag":
                    cycle_frames = num_frames // dot.zigzag_cycle_frames
                    increment = ((i + int(dot.initial_phase * cycle_frames)) % cycle_frames) / (cycle_frames - 1)
                    zigzag_amplitude = width // dot.zigzag_cycle_frames * 2

                    if ((i + int(dot.initial_phase * cycle_frames)) // cycle_frames) % 2 == 0:
                        x_with_offset = dot.x + int(zigzag_amplitude * increment) if dot.zigzag_direction == "right" else dot.x - int(zigzag_amplitude * increment)
                    else:
                        x_with_offset = dot.x + int(zigzag_amplitude * (1 - increment)) if dot.zigzag_direction == "right" else dot.x - int(zigzag_amplitude * (1 - increment))
                    x_with_offset = x_with_offset % width


                else:
                    x_with_offset = dot.x

                if dot.shape == "cross":
                    draw.line([x_with_offset + dot.size // 2, y_with_offset, x_with_offset + dot.size // 2, y_with_offset + dot.size], fill=dot.color, width=1)
                    draw.line([x_with_offset, y_with_offset + dot.size // 2, x_with_offset + dot.size, y_with_offset + dot.size // 2], fill=dot.color, width=1)
                elif dot.shape == "line":
                    draw.line([x_with_offset, y_with_offset, x_with_offset, y_with_offset + dot.line_length], fill=dot.color, width=1)
                elif dot.shape == "star":
                    star_size=dot.size+5
                    long_diamond_height = star_size * 2 // 2
                    short_diamond_width = star_size * 2 // 5
                    draw.polygon([x_with_offset + star_size // 2, y_with_offset,
                                x_with_offset + short_diamond_width, y_with_offset + long_diamond_height // 2,
                                x_with_offset + star_size // 2, y_with_offset + long_diamond_height,
                                x_with_offset + star_size - short_diamond_width, y_with_offset + long_diamond_height // 2], fill=dot.color)
                    draw.polygon([x_with_offset, y_with_offset + star_size // 2,
                                x_with_offset + star_size // 2, y_with_offset + star_size - short_diamond_width,
                                x_with_offset + star_size, y_with_offset + star_size // 2,
                                x_with_offset + star_size // 2, y_with_offset + short_diamond_width], fill=dot.color)
                elif dot.shape == "circle":
                    draw.ellipse([x_with_offset, y_with_offset, x_with_offset + dot.size, y_with_offset + dot.size], outline=dot.color, width=1)
                else:
                    draw.ellipse([x_with_offset, y_with_offset, x_with_offset + dot.size, y_with_offset + dot.size], fill=dot.color)
        frames.append(canvas)
    return frames


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate a GIF with custom shapes and color')
    parser.add_argument('--shapes', nargs='+', type=str, default=["dot", 1], help='Space-separated list of shape, its ratio, and color (e.g., "cross 2 FF0000 line 9 00FF00")')
    parser.add_argument('--color', type=str, help='Dot color in 6-digit hex format (e.g., FF0000 for red)')
    parser.add_argument('--direction', type=str, default="down", choices=["down", "left", "right", "zigzag"], help='Direction of the falling dots (default: down)')
    parser.add_argument('--width', type=int, default=1024, help='Canvas width (default: 1024)')
    parser.add_argument('--height', type=int, default=1024, help='Canvas height (default: 1024)')
    parser.add_argument('--num_dots', type=int, default=150, help='Number of dots (default: 150)')
    parser.add_argument('--min_size', type=int, default=2, help='Minimum dot size (default: 2)')
    parser.add_argument('--max_size', type=int, default=10, help='Maximum dot size (default: 10)')
    parser.add_argument('--duration', type=int, default=150, help='Duration of each frame in milliseconds (default: 150)')
    parser.add_argument('--height_range', type=int, default=512, help='Height range for dots (default: 512)')
    parser.add_argument('--num_frames', type=int, default=200, help='Number of frames (default: 200)')


    args = parser.parse_args()

    shape_ratios = {}
    shape_colors = {}
    if args.shapes is not None:
        if len(args.shapes) == 1:
            shape = args.shapes[0]
            if shape not in ['dot', 'line', 'cross', 'star', 'circle']:
                raise ValueError("Invalid shape: {}. Allowed shapes: dot, line, cross, star, circle".format(shape))
            shape_ratios[shape] = 1
            if args.color is not None:
                shape_colors[shape] = args.color
            else:
                shape_colors[shape] = "FFFFFF"
        else:
            if args.color is not None:
                if len(args.shapes) % 2 != 0:
                    raise ValueError("Invalid shapes input. Each shape must be followed by its ratio.")
                for i in range(0, len(args.shapes), 2):
                    shape = args.shapes[i]
                    ratio = int(args.shapes[i + 1])
                    color = args.color
                    if shape not in ['dot', 'line', 'cross', 'star', 'circle']:
                        raise ValueError("Invalid shape: {}. Allowed shapes: dot, line, cross, star, circle".format(shape))
                    shape_ratios[shape] = ratio
                    shape_colors[shape] = color
            else:
                if len(args.shapes) % 3 != 0:
                    raise ValueError("Invalid shapes input. Each shape must be followed by its ratio and color.")
                for i in range(0, len(args.shapes), 3):
                    shape = args.shapes[i]
                    ratio = int(args.shapes[i + 1])
                    color = args.shapes[i + 2]
                    if shape not in ['dot', 'line', 'cross', 'star', 'circle']:
                        raise ValueError("Invalid shape: {}. Allowed shapes: dot, line, cross, star, circle".format(shape))
                    shape_ratios[shape] = ratio
                    shape_colors[shape] = color
    return shape_ratios, shape_colors, args.direction, args.width, args.height, args.num_dots, args.min_size, args.max_size, args.duration, args.height_range, args.num_frames


if __name__ == "__main__":
    shape_ratios, shape_colors, direction, width, height, num_dots, min_size, max_size, duration, height_range, num_frames = parse_arguments()

    dots = create_dots(shape_ratios, shape_colors, num_dots, min_size, max_size, width, height_range, num_frames, direction)
    frames = create_frames(num_frames, width, height, dots)

filename = f"falling_shapes_{direction}.gif"
frames[0].save(filename, save_all=True, append_images=frames[1:], duration=duration, loop=0, transparency=0, disposal=2)
