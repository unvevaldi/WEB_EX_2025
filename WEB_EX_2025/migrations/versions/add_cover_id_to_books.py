"""
Миграция Alembic: добавляет поле cover_id в таблицу books и внешний ключ на covers.
"""

from alembic import op
import sqlalchemy as sa

revision = 'add_cover_id'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('books') as batch_op:
        batch_op.add_column(sa.Column('cover_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_books_cover_id_covers', 'covers', ['cover_id'], ['id'], ondelete='SET NULL')

def downgrade():
    with op.batch_alter_table('books') as batch_op:
        batch_op.drop_constraint('fk_books_cover_id_covers', type_='foreignkey')
        batch_op.drop_column('cover_id')
