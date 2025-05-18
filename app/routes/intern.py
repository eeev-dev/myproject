from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required

from ..models.intern import Intern
from ..extensions import db

intern = Blueprint('intern', __name__)


@intern.route('/intern/all', methods=['GET', 'POST'])
def all():
    interns = Intern.query.order_by(Intern.score).all()
    return render_template('intern/all.html', interns=interns)


@intern.route('/intern/create', methods=['POST'])
def create():
    intern = Intern(
        name=request.form['name'],
        group=request.form['group'],
        year=request.form['year'],
        head_teacher=request.form['head_teacher'],
        score=request.form['score'],
        place=request.form['place']
    )
    print(intern)

    try:
        db.session.add(intern)
        db.session.commit()
        return redirect('/intern/all')
    except Exception as e:
        print(str(e))

    return "", 200
