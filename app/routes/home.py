from datetime import datetime

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..models.intern import Intern

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@login_required
def home():
    interns = Intern.query.filter(Intern.head_teacher == current_user.name)

    count_pending_interns = interns.filter(Intern.status == 'Ожидает подтверждения').count()
    count_confirmed_interns = interns.filter(Intern.status == 'Подтвержден').count()

    return render_template(
        'home/home.html',
        pending_interns=count_pending_interns,
        interns_with_request=count_confirmed_interns + count_pending_interns,
        all=interns.count()
    )