"""增加article table 并关联

Revision ID: 1404f74ac8a3
Revises: 
Create Date: 2021-04-28 23:52:12.408347

"""
from alembic import op
import sqlalchemy as sa
# from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1404f74ac8a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('user')
    # op.drop_table('test')
    # op.add_column('user',
    #     sa.orm.relationship('Article', backref = 'relate_user', lazy = 'dynamic')
    # )
    op.create_table('article',
        sa.Column('id', sa.Integer, primary_key = True, nullable = False),
        sa.Column('title', sa.String(20), nullable = False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('User.id')),
        sa.Column('create_time', sa.DateTime, default = sa.sql.func.now(), nullable = False),
        sa.Column('cover', sa.String(100), nullable = False),
        sa.Column('state', sa.String(20), nullable = False),
        sa.Column('tag', sa.String(20), nullable = True)
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article')
    op.drop_column('user', 'Article')
    
    # op.create_table('user',
    #     sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    #     sa.Column('name', mysql.VARCHAR(length=20), nullable=False),
    #     sa.Column('email', mysql.VARCHAR(length=20), nullable=True),
    #     sa.Column('phone', mysql.VARCHAR(length=20), nullable=True),
    #     sa.Column('password', mysql.VARCHAR(length=20), nullable=False),
    #     sa.Column('avatar', mysql.VARCHAR(length=100), nullable=True),
    #     sa.Column('roles', mysql.VARCHAR(length=20), nullable=True),
    #     sa.Column('introduction', mysql.VARCHAR(length=100), nullable=True),
    #     sa.Column('signup_time', mysql.DATETIME(), nullable=False),
    #     sa.PrimaryKeyConstraint('id'),
    #     mysql_default_charset='utf8',
    #     mysql_engine='InnoDB'
    # )
    # ### end Alembic commands ###
