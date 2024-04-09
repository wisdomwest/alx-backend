#!/usr/bin/env python3

""" Basic Flask app """

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """ Config class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)


babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """ Get locale"""
    locale = request.args.get('locale', '').strip()
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# babel.init_app(app, locale_selector=get_locale)
@app.route('/', strict_slashes=False)
def hello() -> str:
    """ Hello world """
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run()
