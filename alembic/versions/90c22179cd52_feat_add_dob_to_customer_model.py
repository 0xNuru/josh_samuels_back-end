"""feat: add dob to customer model

Revision ID: 90c22179cd52
Revises: 0e8e293508c1
Create Date: 2024-08-25 18:31:30.359030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90c22179cd52'
down_revision: Union[str, None] = '0e8e293508c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('date_of_birth', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customers', 'date_of_birth')
    # ### end Alembic commands ###
