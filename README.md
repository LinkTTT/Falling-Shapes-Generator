# Falling Shapes Generator

This Python script generates a GIF with custom falling shapes and colors. You can customize the shapes, their ratios, colors, direction, canvas size, number of dots, dot size, and duration of each frame. The generated GIF is saved to the current working directory.

## Dependencies

- Python 3.x
- Pillow (Python Imaging Library) - Install it with `pip install Pillow`

## Usage

```
cssCopy code
python falling_shapes.py [OPTIONS]
```

## Options

- ```
  --shapes
  ```

  : Space-separated list of shape, its ratio, and color (e.g., "cross 2 FF0000 line 9 00FF00"). Allowed shapes: dot, line, cross, star, circle. Default: "dot 1". The ratio determines the proportion of each shape in the generated GIF. For example, if you have two shapes with ratios 2 and 1, the first shape will appear twice as often as the second shape.

  - Example 1: "cross 2 FF0000 line 9 00FF00" - 2/11 of the shapes will be red crosses, and 9/11 will be green lines.
  - Example 2: "circle 3 0000FF star 1 FFFF00" - 3/4 of the shapes will be blue circles, and 1/4 will be yellow stars.

- `--color`: Dot color in 6-digit hex format (e.g., FF0000 for red). Ignored if color is specified for each shape.

- `--direction`: Direction of the falling dots. Allowed values: down (default), left, right, zigzag.

- `--width`: Canvas width. Default: 1024.

- `--height`: Canvas height. Default: 1024.

- `--num_dots`: Number of dots. Default: 150.

- `--min_size`: Minimum dot size. Default: 2.

- `--max_size`: Maximum dot size. Default: 10.

- `--duration`: Duration of each frame in milliseconds. Default: 150.

- `--height_range`: Height range for dots. Default: 512.

- `--num_frames`: Number of frames. Default: 200.

## Example

To generate a GIF with falling cross, line, and circle shapes in red, green, and blue colors respectively:

```
scssCopy code
python falling_shapes.py --shapes dot 11 star 3 --direction zigzag --color ff00ff --width 1024 --height 1024 --num_dots 150 --min_size 2 --max_size 10 --duration 150 --height_range 512 --num_frames 200
```
<img src="https://github.com/LinkTTT/Falling-Shapes-Generator/blob/main/falling_shapes_zigzag.gif" alt="example image" width="300" height="300"/>

```
scssCopy code
python falling_shapes.py --shapes line 11 cross 3 --color 0000FF
```
<img src="https://github.com/LinkTTT/Falling-Shapes-Generator/blob/main/falling_shapes_down.gif" alt="example image" width="300" height="300"/>

```
scssCopy code
python falling_shapes.py --shapes cross 2 FF0000 dot 11 00FF00 star 3 0000FF --direction left --width 1024 --height 1024 --num_dots 150 --min_size 2 --max_size 10 --duration 150 --height_range 512 --num_frames 200
```
<img src="https://github.com/LinkTTT/Falling-Shapes-Generator/blob/main/falling_shapes_left.gif" alt="example image" width="300" height="300"/>

```
scssCopy code
python falling_shapes.py --shapes cross 2 FF0000 line 9 00FF00 circle 3 0000FF --direction right --width 1024 --height 1024 --num_dots 150 --min_size 2 --max_size 10 --duration 150 --height_range 512 --num_frames 200
```
<img src="https://github.com/LinkTTT/Falling-Shapes-Generator/blob/main/falling_shapes_right.gif" alt="example image" width="300" height="300"/>

This will create a GIF named "falling_shapes_zigzag.gif" in the current working directory.

