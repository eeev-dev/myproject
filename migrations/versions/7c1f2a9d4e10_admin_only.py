"""Только администратор: убраны ВКР, преподаватели, интерны, расписание, пользователи;
поля интерна перенесены в student, добавлена таблица deadline.

Revision ID: 7c1f2a9d4e10
Revises: 436be745dcd6
Create Date: 2026-11-15 05:00:00

"""
from alembic import op
import sqlalchemy as sa


revision = '7c1f2a9d4e10'
down_revision = '436be745dcd6'
branch_labels = None
depends_on = None


def upgrade():
    # Новые поля студента (бывшие поля интерна)
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('place', sa.String(length=70), nullable=True))
        batch_op.add_column(sa.Column('title', sa.String(length=70), nullable=True))
        batch_op.add_column(sa.Column('letter', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=True, server_default='Без заявки'))
        batch_op.add_column(sa.Column('message', sa.String(length=200), nullable=True))

    # Переносим заявки из intern в student (если таблица ещё есть)
    op.execute("""
        UPDATE student s
        SET place = i.place, title = i.title, letter = i.letter,
            status = COALESCE(i.status, 'Без заявки'), message = i.message
        FROM intern i
        WHERE i.student_id = s.id
    """)
    op.execute("UPDATE student SET status = 'Без заявки' WHERE status IS NULL")

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_column('score')

    op.create_table(
        'deadline',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=150), nullable=True),
        sa.Column('apply_start', sa.Date(), nullable=True),
        sa.Column('apply_end', sa.Date(), nullable=True),
        sa.Column('practice_start', sa.Date(), nullable=True),
        sa.Column('practice_end', sa.Date(), nullable=True),
    )

    for table in ('graduate', 'intern', 'schedule', 'teacher', 'topic', 'standart', 'user'):
        op.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')


def downgrade():
    op.drop_table('deadline')
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('score', sa.Numeric(8, 6), nullable=True))
        batch_op.drop_column('message')
        batch_op.drop_column('status')
        batch_op.drop_column('letter')
        batch_op.drop_column('title')
        batch_op.drop_column('place')

    op.create_table('user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(50)), sa.Column('login', sa.String(50)),
        sa.Column('password', sa.String(200)), sa.Column('practice_deadline', sa.DateTime()),
        sa.Column('vkr_deadline', sa.DateTime()), sa.Column('supervisor_deadline', sa.DateTime()),
        sa.Column('role', sa.String(50)))
    op.create_table('intern',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer()), sa.Column('name', sa.String(50)),
        sa.Column('place', sa.String(70)), sa.Column('title', sa.String(70)),
        sa.Column('group', sa.String(50)), sa.Column('year', sa.Integer()),
        sa.Column('head_teacher', sa.String(50)), sa.Column('score', sa.Numeric(8, 6)),
        sa.Column('letter', sa.String(200)), sa.Column('status', sa.String(50)),
        sa.Column('message', sa.String(200)),
        sa.UniqueConstraint('student_id', 'name', 'group', 'year', name='uq_intern_student_group_year'))
    op.create_table('graduate',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer()), sa.Column('name', sa.String(50)),
        sa.Column('group', sa.String(50)), sa.Column('topic', sa.String(200)),
        sa.Column('supervisor', sa.String(50)), sa.Column('status', sa.String(50)),
        sa.Column('message', sa.String(200)))
    op.create_table('schedule',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(100)), sa.Column('type', sa.String(3)),
        sa.Column('teacher', sa.String(50)), sa.Column('group', sa.String(50)),
        sa.Column('term', sa.Integer()), sa.Column('day', sa.String(20)),
        sa.Column('time', sa.String(20)), sa.Column('parity', sa.String(10)),
        sa.Column('is_online', sa.Integer()), sa.Column('room', sa.String(20)))
    op.create_table('teacher',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(50)), sa.Column('url', sa.String(200)))
    op.create_table('topic',
        sa.Column('id', sa.Integer(), primary_key=True), sa.Column('title', sa.String(100)))
    op.create_table('standart',
        sa.Column('id', sa.Integer(), primary_key=True), sa.Column('title', sa.String(100)),
        sa.Column('taken', sa.Integer()))
