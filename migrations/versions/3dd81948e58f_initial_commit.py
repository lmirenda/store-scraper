"""initial commit

Revision ID: 3dd81948e58f
Revises: 
Create Date: 2024-02-23 17:35:37.102803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '3dd81948e58f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_keys',
    sa.Column('api_key', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('api_key')
    )
    op.create_index(op.f('ix_api_keys_api_key'), 'api_keys', ['api_key'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_api_keys_api_key'), table_name='api_keys')
    op.drop_table('api_keys')
    # ### end Alembic commands ###
