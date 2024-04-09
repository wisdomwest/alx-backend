#!/usr/bin/env python3


""" Basic Flask app """

from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
from typing import Union, Dict
import pytz
import datetime

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
    locales = [
        request.args.get('locale', '').strip(),
        g.user.get('locale', None) if g.user else None,
        request.accept_languages.best_match(app.config['LANGUAGES']),
        app.config['BABEL_DEFAULT_LOCALE']
    ]
    for locale in locales:
        if locale and locale in app.config['LANGUAGES']:
            return locale


@babel.timezoneselector
def get_timezone() -> str:
    """ Get timezone """
    t_zone = request.args.get('timezone', '').strip()
    if not t_zone and g.user:
        t_zone = g.user['timezone']
    try:
        t_zone = pytz.timezone(t_zone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        t_zone = app.config['BABEL_DEFAULT_TIMEZONE']


@app.before_request
def before_request():
    """ Before request """
    g.user = get_user(request.args.get('login_as'))
    g.time = format_datetime(datetime.datetime.now()))

# babel.init_app(app, locale_selector=get_locale)


@app.route('/', strict_slashes=False)
def hello() -> str:
    """ Hello world """
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
