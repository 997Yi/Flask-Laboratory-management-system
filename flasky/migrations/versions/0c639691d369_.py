"""empty message

Revision ID: 0c639691d369
Revises: 
Create Date: 2020-07-18 22:02:32.848742

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0c639691d369'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('laboratories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('labNo', sa.Integer(), nullable=True),
    sa.Column('isUse', sa.Boolean(), nullable=True),
    sa.Column('labType', sa.String(length=12), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('labNo')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_table('stuLabs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comNo', sa.Integer(), nullable=True),
    sa.Column('isUse', sa.Boolean(), nullable=True),
    sa.Column('labNo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['labNo'], ['laboratories.labNo'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('comNo')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sno', sa.String(length=12), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    op.create_index(op.f('ix_users_sno'), 'users', ['sno'], unique=True)
    op.create_table('administrators',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('adminNo', sa.Integer(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('adminNo')
    )
    op.create_table('labAppoint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('howClass', sa.Integer(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('labNo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['labNo'], ['laboratories.labNo'], ),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stuLabAppoint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('startTime', sa.DateTime(), nullable=True),
    sa.Column('endTime', sa.DateTime(), nullable=True),
    sa.Column('useReason', sa.Text(length=200), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('labNo', sa.Integer(), nullable=True),
    sa.Column('comNo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comNo'], ['stuLabs.comNo'], ),
    sa.ForeignKeyConstraint(['labNo'], ['laboratories.labNo'], ),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('adminNo', sa.Integer(), nullable=True),
    sa.Column('labNo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['adminNo'], ['administrators.adminNo'], ),
    sa.ForeignKeyConstraint(['labNo'], ['laboratories.labNo'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(length=200), nullable=True),
    sa.Column('adminNo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['adminNo'], ['administrators.adminNo'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_users_name', table_name='users_copy1')
    op.drop_index('ix_users_sno', table_name='users_copy1')
    op.drop_table('users_copy1')
    op.drop_index('ix_roles_default', table_name='roles_copy2')
    op.drop_index('name', table_name='roles_copy2')
    op.drop_table('roles_copy2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles_copy2',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('default', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('permissions', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'roles_copy2', ['name'], unique=True)
    op.create_index('ix_roles_default', 'roles_copy2', ['default'], unique=False)
    op.create_table('users_copy1',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('sno', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('password_hash', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('role_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_users_sno', 'users_copy1', ['sno'], unique=True)
    op.create_index('ix_users_name', 'users_copy1', ['name'], unique=True)
    op.drop_table('notices')
    op.drop_table('admin')
    op.drop_table('stuLabAppoint')
    op.drop_table('labAppoint')
    op.drop_table('administrators')
    op.drop_index(op.f('ix_users_sno'), table_name='users')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_table('users')
    op.drop_table('stuLabs')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    op.drop_table('laboratories')
    # ### end Alembic commands ###
