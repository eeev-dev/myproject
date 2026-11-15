"""Состояние кабинета: шаги настройки, данные бокового меню, файлы инструкции и приложения."""
import os

from flask import current_app
from sqlalchemy import func

from .extensions import db
from .models.student import Student
from .models.group import Group
from .models.place import Place
from .models.review import Review
from .models.deadline import Deadline

OWN_PLACE = 'Свое место практики'

INSTRUCTION_TEXT_FILE = 'instruction.txt'
APP_SENT_FLAG = 'sent.flag'
APP_EXTENSIONS = ('.apk', '.aab')

STEP_LABELS = [
    'Загрузить студентов',
    'Руководители групп',
    'Сроки практики',
    'Инструкция для своего места',
    'Места практики',
    'Приложение студентам',
]


def ensure_dirs():
    cfg = current_app.config
    for key in ('UPLOAD_PATH', 'INSTRUCTION_PATH', 'APP_PATH'):
        os.makedirs(cfg[key], exist_ok=True)


# --- Шаг 4: инструкция (папка app/instruction) ---

def instruction_text():
    path = os.path.join(current_app.config['INSTRUCTION_PATH'], INSTRUCTION_TEXT_FILE)
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    return ''


def save_instruction_text(text):
    ensure_dirs()
    path = os.path.join(current_app.config['INSTRUCTION_PATH'], INSTRUCTION_TEXT_FILE)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def instruction_files():
    folder = current_app.config['INSTRUCTION_PATH']
    if not os.path.isdir(folder):
        return []
    files = []
    for name in sorted(os.listdir(folder)):
        full = os.path.join(folder, name)
        if name == INSTRUCTION_TEXT_FILE or name.startswith('.') or not os.path.isfile(full):
            continue
        files.append({'name': name, 'size': human_size(os.path.getsize(full)),
                      'type': os.path.splitext(name)[1].lstrip('.').upper() or 'FILE'})
    return files


# --- Шаг 6: приложение (папка static/app) ---

def app_file():
    folder = current_app.config['APP_PATH']
    if not os.path.isdir(folder):
        return None
    for name in sorted(os.listdir(folder)):
        if name.lower().endswith(APP_EXTENSIONS):
            full = os.path.join(folder, name)
            return {'name': name, 'size': human_size(os.path.getsize(full))}
    return None


def app_sent():
    return os.path.exists(os.path.join(current_app.config['APP_PATH'], APP_SENT_FLAG))


def set_app_sent(value):
    ensure_dirs()
    path = os.path.join(current_app.config['APP_PATH'], APP_SENT_FLAG)
    if value:
        open(path, 'w').close()
    elif os.path.exists(path):
        os.remove(path)


def human_size(n):
    if n < 1024:
        return f'{n} Б'
    if n < 1024 * 1024:
        return f'{round(n / 1024)} КБ'
    return f'{n / 1024 / 1024:.1f} МБ'.replace('.', ',')


# --- Сроки ---

def short_range(start, end):
    if not (start and end):
        return None
    return f'{start:%d.%m}–{end:%d.%m}'


# --- Шаги ---

def steps_state():
    d = Deadline.current()
    students = Student.query.count()
    groups = Group.query.all()

    s1 = 'done' if students else 'todo'
    if not groups:
        s2 = 'todo'
    elif all((g.head_teacher or '').strip() for g in groups):
        s2 = 'done'
    else:
        s2 = 'warn'
    if d and d.apply_set and d.practice_set:
        s3 = 'done'
    elif d and (d.apply_set or d.practice_set or d.title):
        s3 = 'warn'
    else:
        s3 = 'todo'
    s4 = 'done' if instruction_text().strip() else 'todo'
    s5 = 'done' if Place.query.count() else 'todo'
    if app_sent():
        s6 = 'done'
    elif app_file():
        s6 = 'warn'
    else:
        s6 = 'todo'
    states = [s1, s2, s3, s4, s5, s6]
    return [{'n': i + 1, 'label': STEP_LABELS[i], 'state': st} for i, st in enumerate(states)]


def nav_context():
    steps = steps_state()
    done = sum(1 for s in steps if s['state'] == 'done')
    d = Deadline.current()
    return {
        'nav_counts': {
            'students': Student.query.count(),
            'groups': Group.query.count(),
            'places': Place.query.count(),
            'reviews': Review.query.count(),
        },
        'nav_steps': steps,
        'nav_steps_done': done,
        'nav_apply': short_range(d.apply_start, d.apply_end) if d else None,
        'nav_practice': short_range(d.practice_start, d.practice_end) if d else None,
    }


def recount_free_places():
    """Пересчитать свободные места: место занимает каждый студент, который его выбрал."""
    taken = dict(db.session.query(Student.place, func.count(Student.id))
                 .group_by(Student.place).all())
    for p in Place.query.all():
        p.places = max(0, (p.max_places or 0) - taken.get(p.title, 0))
