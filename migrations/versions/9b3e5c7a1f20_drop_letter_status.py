"""Убраны письма и статусы заявок: удалены поля student.letter, student.message, student.status.

Revision ID: 9b3e5c7a1f20
Revises: 7c1f2a9d4e10
Create Date: 2026-11-15 12:00:00

"""
from alembic import op
import sqlalchemy as sa


revision = '9b3e5c7a1f20'
down_revision = '7c1f2a9d4e10'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_column('letter')
        batch_op.drop_column('message')
        batch_op.drop_column('status')


def downgrade():
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=True, server_default='Без заявки'))
        batch_op.add_column(sa.Column('message', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('letter', sa.String(length=200), nullable=True))
