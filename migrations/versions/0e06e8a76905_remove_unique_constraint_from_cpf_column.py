"""remove_unique_constraint_from_cpf_column

Revision ID: 0e06e8a76905
Revises: ea0e664c46ef
Create Date: 2024-09-22 20:41:32.918687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e06e8a76905'
down_revision = 'ea0e664c46ef'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('uq_owners_cpf', 'owners', type_='unique')


def downgrade():
    op.create_unique_constraint('uq_owners_cpf', 'owners', ['cpf'])
