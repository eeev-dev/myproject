from datetime import datetime

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..models.intern import Intern
from ..models.graduate import Graduate

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@login_required
def home():
    interns = Intern.query.filter(Intern.head_teacher == current_user.name)

    intern_pending = interns.filter(Intern.status == 'Ожидает подтверждения').count()
    intern_requests = intern_pending + interns.filter(Intern.status == 'Подтвержден').count()
    intern_all = interns.count()

    graduates = Graduate.query.filter(Graduate.supervisor == current_user.name)

    vkr_pending = graduates.filter(Graduate.status == 'Ожидает проверки').count()
    vkr_requests = vkr_pending + graduates.filter(Graduate.status == 'Проверка пройдена').count()
    vkr_all = graduates.count()

    return render_template(
        'home/home.html',
        intern_pending=intern_pending,
        intern_requests=intern_requests,
        intern_all=intern_all,
        vkr_pending=vkr_pending,
        vkr_requests=vkr_requests,
        vkr_all=vkr_all
    )