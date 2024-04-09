#!/usr/bin/env python3


""" Basic Flask app """

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict


class Config:
    """ Config class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)


babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(login_as) -> Union[Dict[str, Union[str, None]], None]:
    """ Get user """
    if login_as:
        try:
            return users[int(login_as)]
        except Exception:
            return None
    return None


@babel.localeselector
def get_locale() -> str:
    """ Get locale"""
    user = getattr(g, 'user', None)
    if user:
        locale = user.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.before_request
def before_request():
    """ Before request """
    g.user = get_user(request.args.get('login_as'))


# babel.init_app(app, locale_selector=get_locale)


@app.route('/', strict_slashes=False)
def hello() -> str:
    """ Hello world """
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run()
