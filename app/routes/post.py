from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required

from ..extensions import db
from ..models.post import Post

post = Blueprint('post', __name__)


@post.route('/', methods=['GET', 'POST'])
def all():
    posts = Post.query.order_by(Post.date).all()
    return render_template('post/all.html', posts=posts)


@post.route('/post/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        teacher = request.form['teacher']
        subject = request.form['subject']
        student = request.form['student']
        post = Post(teacher=teacher, subject=subject, student=student)
        print(post)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
    else:
        return render_template('post/create.html')


@post.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.teacher = request.form['teacher']
        post.subject = request.form['subject']
        post.student = request.form['student']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
    else:
        return render_template('post/update.html', post=post)


@post.route('/post/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(str(e))
        return(str(e))


@post.route('/api/posts', methods=['POST'])
@login_required
def api_create_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    teacher = data.get('teacher')
    subject = data.get('subject')
    student = data.get('student')

    if not all([teacher, subject, student]):
        return jsonify({"error": "Missing fields"}), 400

    new_post = Post(teacher=teacher, subject=subject, student=student)
    try:
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"message": "Post created successfully", "id": new_post.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
