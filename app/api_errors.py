"""Единый формат ошибок для мобильного API: {"success": false, "message": "..."}."""
from flask import jsonify, request
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from werkzeug.exceptions import HTTPException, InternalServerError

from .extensions import db

# Пути, по которым ходит мобильное приложение
API_PREFIXES = ('/api/', '/student/', '/review/', '/ping')

HTTP_MESSAGES = {
    400: "Некорректный запрос",
    401: "Требуется авторизация",
    403: "Доступ запрещён",
    404: "Запрашиваемый ресурс не найден",
    405: "Метод запроса не поддерживается",
    413: "Слишком большой запрос",
    415: "Неподдерживаемый формат данных, ожидается JSON",
    429: "Слишком много запросов, попробуйте позже",
    500: "Внутренняя ошибка сервера",
    502: "Сервер временно недоступен",
    503: "Сервис временно недоступен, попробуйте позже",
    504: "Сервер не ответил вовремя",
}


class ApiError(Exception):
    def __init__(self, message, code=400):
        super().__init__(message)
        self.message, self.code = message, code


def error(message, code):
    return jsonify({"success": False, "message": message}), code


def payload():
    """Тело запроса как dict, иначе ApiError 400."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data:
        raise ApiError("Нет данных в теле запроса или они не в формате JSON", 400)
    return data


def _is_api():
    return request.path.startswith(API_PREFIXES)


def register(app):
    @app.errorhandler(ApiError)
    def _api_error(e):
        return error(e.message, e.code)

    @app.errorhandler(HTTPException)
    def _http_error(e):
        if not _is_api():
            return e
        return error(HTTP_MESSAGES.get(e.code, e.description or "Ошибка запроса"), e.code)

    @app.errorhandler(OperationalError)
    def _db_unavailable(e):
        db.session.rollback()
        app.logger.exception("База данных недоступна")
        if not _is_api():
            return InternalServerError()
        return error("База данных недоступна, попробуйте позже", 503)

    @app.errorhandler(SQLAlchemyError)
    def _db_error(e):
        db.session.rollback()
        app.logger.exception("Ошибка базы данных")
        if not _is_api():
            return InternalServerError()
        return error("Ошибка базы данных", 500)

    @app.errorhandler(Exception)
    def _unexpected(e):
        db.session.rollback()
        app.logger.exception("Необработанная ошибка")
        if not _is_api():
            return InternalServerError()
        return error(HTTP_MESSAGES[500], 500)
