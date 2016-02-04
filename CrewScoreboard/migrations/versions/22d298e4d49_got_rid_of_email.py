"""Got rid of email

Revision ID: 22d298e4d49
Revises: 58eb8c49694
Create Date: 2016-02-03 20:39:07.832765

"""

# revision identifiers, used by Alembic.
revision = '22d298e4d49'
down_revision = '58eb8c49694'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('siteusers', 'email')
    op.drop_index('ix_siteusers_email', 'siteusers')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_siteusers_email', 'siteusers', ['email'], unique=1)
    op.add_column('siteusers', sa.Column('email', sa.VARCHAR(length=64), nullable=True))
    ### end Alembic commands ###