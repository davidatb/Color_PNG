from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png'}

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        hex_color = request.form['hex_color']

        if not re.match(r'^#(?:[0-9a-fA-F]{6})$', hex_color):
            return "Error: El formato del color hexadecimal debe ser '#RRGGBB'", 400

        rgba_color = hex_to_rgba(hex_color)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], "output_" + filename)
            cambiar_color(input_path, output_path, rgba_color)
            return send_from_directory(app.config['UPLOAD_FOLDER'], "output_" + filename, as_attachment=True)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Carga una imagen PNG</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file><br>
      Color HEX: <input type=text name=hex_color placeholder="#RRGGBB"><br>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
