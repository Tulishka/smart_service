"""
Модуль, включающий в себя некоторые главные обработчики

Представлены обработчики:
- /: Главная страница
- /media/<filename>: Страница для раздачи файлов из папки media
- /forbidden: Страница, на которую перенаправляются пользователи в случае отказа доступа
"""


from flask import Blueprint, render_template, send_from_directory

from app.config import Config

bp = Blueprint("main", __name__, url_prefix="/", template_folder="templates")


@bp.route("/")
def index():
    """Обработчик главной страницы

    :return: HTML-страница с главным содержимым сайта
    """

    return render_template("main.html")


@bp.route('/media/<path:filename>')
def media_files(filename):
    """Обработчик для страницы раздачи файлов из папки media

    :param filename: Название файла
    :return: Файл из папки Media
    """
    return send_from_directory(Config.MEDIA_FOLDER, filename)


@bp.route("/forbidden")
def forbidden():
    """Обработчик для страницы с отказом в доступе

    :return: HTML-страница с сообщением об отказе в доступе
    """
    return render_template("403.html")

