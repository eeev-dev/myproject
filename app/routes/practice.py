"""API практики для мобильного приложения.

Все запросы — POST с JSON-телом, в котором есть "student_id".
Статуса практики нет: клиент определяет его по пустым (null) полям ответа.

POST /api/practice                 {"student_id"}               — состояние практики студента
POST /api/practice/place           {"student_id", "place_id"}   — выбрать место из предложенных
POST /api/practice/own-place       {"student_id", "title"}      — указать своё место практики
POST /api/practice/instruction     {"student_id"}               — инструкция для своего места (текст и список файлов)
POST /api/practice/instruction/file {"student_id", "name"}     — скачать файл инструкции (ответ — сам файл)

Ответ /api/practice (и /place, /own-place после сохранения):
{
  "success": true,
  "message": "Идёт выбор места практики. Выберите место до 18.11.2026.",  // текст о текущем этапе
  "practice": {                       // сроки; любое поле может быть null — ещё не указано
    "title": "Производственная практика",
    "apply_start": "2026-11-01",      // набор (выбор места)
    "apply_end": "2026-11-18",
    "practice_start": "2026-11-19",   // прохождение
    "practice_end": "2026-12-15"
  },
  "head_teacher": "Исраилова Н. А.",  // null — руководитель не назначен
  "place": {                          // null — место не выбрано
    "id": 3,                          // null для своего места
    "title": "ГП «Инфоцентр»",
    "own": false                      // true — студент нашёл место сам
  }
}

Ответ /api/practice/instruction:
{"success": true, "text": "...",
 "files": [{"name": "Приложение.docx",
            "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "size": 18432}]}          // байт

Ответ /api/practice/instruction/file — содержимое файла (Content-Type = mime,
Content-Disposition: attachment; filename=...). Ошибки — JSON, как у остальных запросов.

Ошибки: {"success": false, "message": "..."} с кодом 400 (неверный запрос), 403 (действие недоступно),
404 (студент или место не найдены), 409 (на предприятии не осталось мест).
"""
import mimetypes
import os
from datetime import date

from flask import Blueprint, request, jsonify, current_app, send_from_directory

from ..api_errors import ApiError, payload
from ..extensions import db
from ..models.student import Student
from ..models.group import Group
from ..models.place import Place
from ..models.deadline import Deadline
from .. import state
from ..state import OWN_PLACE

practice = Blueprint('practice', __name__, url_prefix='/api/practice')

_payload = payload


def _student(data):
    try:
        student_id = int(data.get('student_id'))
    except (TypeError, ValueError):
        raise ApiError("Не указан student_id", 400)
    student = Student.query.get(student_id)
    if not student:
        raise ApiError("Студент не найден", 404)
    return student


def _iso(d):
    return d.isoformat() if d else None


def _check_apply_open():
    """Выбирать место можно только в период набора (если его даты заданы)."""
    d = Deadline.current()
    today = date.today()
    if d and d.apply_start and today < d.apply_start:
        raise ApiError(f"Набор начнётся {d.apply_start:%d.%m.%Y}", 403)
    if d and d.apply_end and today > d.apply_end:
        raise ApiError("Набор на практику завершён", 403)


def _fmt(d):
    return f'{d:%d.%m.%Y}'


def _message(d, place):
    """Текст о текущем этапе практики для студента."""
    today = date.today()
    title = f'«{place["title"]}»' if place and place["title"] else ''
    own_hint = ' Ознакомьтесь с инструкцией для своего места практики.' if place and place["own"] else ''

    # 1. Сроков нет / набор ещё не начался
    if not (d and d.apply_set):
        return 'Набор на практику ещё не начался. Сроки появятся позже.'
    if today < d.apply_start:
        return f'Набор на практику начнётся {_fmt(d.apply_start)}.'

    # 2. Идёт набор
    if today <= d.apply_end:
        if place:
            return (f'Вы выбрали место практики {title}. '
                    f'Изменить выбор можно до {_fmt(d.apply_end)}.{own_hint}')
        if not Place.query.filter(Place.places > 0).count():
            return (f'Идёт выбор места практики до {_fmt(d.apply_end)}, но свободных мест на предприятиях не осталось. '
                    'Вы можете указать своё место практики.')
        return f'Идёт выбор места практики. Выберите место до {_fmt(d.apply_end)}.'

    # 3. Набор завершён, места нет
    if not place:
        return ('Набор на практику завершён, а место не выбрано. '
                'Кафедра подберёт вам место практики или продлит срок регистрации.')

    # 4. Набор завершён, место есть
    if d.practice_end and today > d.practice_end:
        return f'Практика в {title} завершена.'
    if d.practice_start and today >= d.practice_start:
        until = f' до {_fmt(d.practice_end)}' if d.practice_end else ''
        return f'Идёт практика в {title}{until}.{own_hint}'
    starts = f' Практика начнётся {_fmt(d.practice_start)}.' if d.practice_start else ''
    return f'Вы успешно зарегистрированы на практику в {title}.{starts}{own_hint}'


def _state(student):
    d = Deadline.current()
    group = Group.query.filter_by(title=student.group).first()

    place = None
    if student.place == OWN_PLACE:
        place = {"id": None, "title": student.title or None, "own": True}
    elif student.place:
        p = Place.query.filter_by(title=student.place).first()
        place = {"id": p.id if p else None, "title": student.place, "own": False}

    return jsonify({
        "success": True,
        "message": _message(d, place),
        "practice": {
            "title": d.title if d else None,
            "apply_start": _iso(d.apply_start) if d else None,
            "apply_end": _iso(d.apply_end) if d else None,
            "practice_start": _iso(d.practice_start) if d else None,
            "practice_end": _iso(d.practice_end) if d else None,
        },
        "head_teacher": (group.head_teacher or None) if group else None,
        "place": place,
    }), 200


@practice.route('/', methods=['POST'], strict_slashes=False)  # POST /api/practice
def get_state():
    return _state(_student(_payload()))


@practice.route('/place', methods=['POST'])
def choose_place():
    data = _payload()
    student = _student(data)
    _check_apply_open()

    try:
        place = Place.query.get(int(data.get('place_id')))
    except (TypeError, ValueError):
        raise ApiError("Не указан place_id", 400)
    if not place:
        raise ApiError("Место практики не найдено", 404)

    if student.place != place.title and (place.places or 0) <= 0:
        raise ApiError("Мест не осталось. Выберите другое предприятие", 409)

    student.place = place.title
    student.title = None
    state.recount_free_places()
    db.session.commit()
    return _state(student)


@practice.route('/own-place', methods=['POST'])
def choose_own_place():
    data = _payload()
    student = _student(data)
    _check_apply_open()

    title = str(data.get('title') or '').strip()
    if not title:
        raise ApiError("Укажите название места практики", 400)

    student.place = OWN_PLACE
    student.title = title[:70]
    state.recount_free_places()
    db.session.commit()
    return _state(student)


def _own_place_student(data):
    student = _student(data)
    if student.place != OWN_PLACE:
        raise ApiError("Инструкция доступна студентам, которые нашли место практики самостоятельно", 403)
    return student


def _mime(name):
    return mimetypes.guess_type(name)[0] or 'application/octet-stream'


@practice.route('/instruction', methods=['POST'])
def instruction():
    _own_place_student(_payload())
    folder = current_app.config['INSTRUCTION_PATH']
    files = [{"name": f['name'], "mime": _mime(f['name']),
              "size": os.path.getsize(os.path.join(folder, f['name']))}
             for f in state.instruction_files()]
    return jsonify({"success": True, "text": state.instruction_text(), "files": files}), 200


@practice.route('/instruction/file', methods=['POST'])
def instruction_file():
    data = _payload()
    _own_place_student(data)
    name = str(data.get('name') or '')
    # Отдаём только файлы из списка инструкции — никаких путей вида ../
    if name not in {f['name'] for f in state.instruction_files()}:
        raise ApiError("Файл не найден", 404)
    return send_from_directory(current_app.config['INSTRUCTION_PATH'], name,
                               as_attachment=True, mimetype=_mime(name))
