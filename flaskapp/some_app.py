from flask import Flask
app = Flask(__name__)

from flask import render_template, request

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

from werkzeug.utils import secure_filename
import os

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "seckey"
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LfvPRgbAAAAADNED3uO5xbBAJo3Lo7LsMqmNIeZ"
app.config["RECAPTCHA_PRIVATE_KEY"]="6LfvPRgbAAAAAF0AxKU-muhLdXlrFhzHI3p81CXD"

app.config['UPLOAD_FOLDER'] = 'static/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

class Widgets(FlaskForm):
    recaptcha = RecaptchaField()
    upload_first = FileField('Загрузите изображение', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])

class ITask(FlaskForm):
    upload_file = FileField('Загрузите изображение', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')])
    height = StringField('Введите коэффициент для высоты', validators=[DataRequired()])
    width = StringField('Введите коэффициент для ширины', validators=[DataRequired()])

import neural

@app.route("/", methods=("GET", "POST"))
def home():
    form = Widgets()
    if request.method == "POST":
        if form.validate_on_submit():
            form.upload_first.data.save(app.config['UPLOAD_FOLDER'] + 'neural_img.png')
            image = neural.recognize(app.config['UPLOAD_FOLDER'] + 'neural_img.png')
            return render_template('start.html', form=form, img=app.config['UPLOAD_FOLDER'] + 'neural_img.png', neur=image)
    if request.method == "GET":
        return render_template("start.html", form=form)

import defs

@app.route('/load', methods=['GET', 'POST'])
def upload_file():
    form = ITask()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = app.config['UPLOAD_FOLDER'] + 'image_to_resize.png'

            form.upload_file.data.save(file)
            height = float(form.height.data)
            width = float(form.width.data)

            h, w = defs.resize_image(file, height, width)
            file_resized = app.config['UPLOAD_FOLDER'] + 'image_resized.png'

            return render_template('form.html', form = form, image_to_resize = file, image_resized = file_resized, height = h, width = w)

    return render_template('form.html', form = form)

@app.route('/graphs', methods=['GET', 'POST'])
def graph_page():
    # Графики
    defs.GRAPHS(app.config['UPLOAD_FOLDER'] + 'image_to_resize.png', app.config['UPLOAD_FOLDER'] + 'image_to_resize_graph.png', 'До изменения размера')
    defs.GRAPHS(app.config['UPLOAD_FOLDER'] + 'image_resized.png', app.config['UPLOAD_FOLDER'] + 'image_resized_graph.png', 'После изменения размера')

    img_1 = app.config['UPLOAD_FOLDER'] + 'image_to_resize_graph.png'
    img_2 = app.config['UPLOAD_FOLDER'] + 'image_resized_graph.png'

    return render_template('graphs.html', url = 'load', img_1 = img_1, img_2 = img_2)

if __name__ == "__main__":
  app.run(debug=True)
