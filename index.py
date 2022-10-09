from flask import Flask, render_template
from flask import request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'noticias libres'

class NameForm(FlaskForm):
    name = StringField('Link de la noticia', validators=[DataRequired()])
    submit = SubmitField('Leer')
    
@app.route('/',methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    cuerpo = ''
    titulo = ''
    subtitulo= ''
    encabezado= ''
    imagen = ''
    if form.validate_on_submit():
        name = form.name.data
        try:
            response = urlopen(name)
            page_source = BeautifulSoup(response.read(),features="lxml")
            elemento=page_source.findAll('script',{"type":"application/ld+json"})#.text
            if "gestion.pe" in name:
                noticia = json.loads(elemento[1].text)
            elif "elcomercio.pe" in name:
                noticia = json.loads(elemento[3].text)
            print(noticia.keys())
            titulo = noticia['headline']
            subtitulo= noticia['alternativeHeadline']
            encabezado= noticia['description']
            cuerpo = noticia['articleBody']
            imagen = noticia['image']['url']
            form.name.data = ''
        except:
            form.name.data = ''
    return render_template('home.html',imagen=imagen,form=form, name=name,cuerpo=cuerpo,titulo=titulo, subtitulo=subtitulo,encabezado=encabezado)


if __name__ == '__main__':
    app.run(debug=True)