import argparse
from PIL import Image
import re

def hex_to_rgba(hex_color):
    # Convierte el color hex en una tupla RGBA
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        hex_color += 'FF'  # Anadir canal alfa para trasparencias
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))

def cambiar_color(input_file, output_file, hex_color):
    try:
        image = Image.open(input_file)
        # Convertir la imagen a modo RGBA si no lo esta
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        width, height = image.size
        for x in range(width):
            for y in range(height):
                r, g, b, a = image.getpixel((x, y))
                if a > 0:
                    image.putpixel((x, y), hex_color)

        image.save(output_file, "PNG")
        print(f"La imagen se ha guardado en {output_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cambiar el color de una imagen PNG")
    parser.add_argument("input_file", help="Ruta de la imagen de entrada (PNG)")
    parser.add_argument("output_file", help="Ruta de la imagen de salida (PNG)")
    parser.add_argument("hex_color", help="Color en formato hexadecimal (ejemplo: #FF0000)")

    args = parser.parse_args()

    # Validar el formato del color hex
    if not re.match(r'^#(?:[0-9a-fA-F]{6})$', args.hex_color):
        print("Error: El formato del color hexadecimal debe ser '#RRGGBB'")
        exit(1)

    hex_color = hex_to_rgba(args.hex_color)

    cambiar_color(args.input_file, args.output_file, hex_color)
