"""category i18n name (name -> name_ru / name_en)

Revision ID: f1a2b3c4d5e6
Revises: e214d0b0456f
Create Date: 2026-06-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, Sequence[str], None] = 'e214d0b0456f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем колонки nullable, чтобы заполнить существующие строки из старого name
    op.add_column('category', sa.Column('name_ru', sa.String(length=100), nullable=True))
    op.add_column('category', sa.Column('name_en', sa.String(length=100), nullable=True))

    # Переносим данные: старое name становится и русским, и английским названием
    # (английский перевод можно отредактировать позже через update_category)
    op.execute('UPDATE category SET name_ru = name, name_en = name')

    # Теперь делаем колонки обязательными и убираем старый name
    op.alter_column('category', 'name_ru', nullable=False)
    op.alter_column('category', 'name_en', nullable=False)
    op.drop_column('category', 'name')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('category', sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.execute('UPDATE category SET name = name_ru')
    op.alter_column('category', 'name', nullable=False)
    op.drop_column('category', 'name_en')
    op.drop_column('category', 'name_ru')
