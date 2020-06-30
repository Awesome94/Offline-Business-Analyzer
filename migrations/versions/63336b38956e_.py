"""empty message

Revision ID: 63336b38956e
Revises: facca51ef3c1
Create Date: 2020-06-29 23:00:57.201486

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '63336b38956e'
down_revision = 'facca51ef3c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=True),
    sa.Column('transaction', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('due_date', sa.String(), nullable=True),
    sa.Column('transaction_date', sa.String(), nullable=True),
    sa.Column('customer_or_supplier', sa.String(), nullable=True),
    sa.Column('item', sa.String(), nullable=True),
    sa.Column('quantity', sa.String(), nullable=True),
    sa.Column('unit_amount', sa.String(), nullable=True),
    sa.Column('total_transaction_amount', sa.String(), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('sample')
    op.drop_table('transaction_details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction_details',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('business_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('due_date', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_or_supplier', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('item', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('unit_amount', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('total_transaction_amount', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('transaction_date', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], name='transaction_details_business_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='transaction_details_pkey')
    )
    op.create_table('sample',
    sa.Column('Transaction', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('ID', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('Status', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('Transaction Date', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('Due Date', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('Customer or Supplier', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('Item', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('Quantity', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('Unit Amount', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('Total Transaction Amount', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    )
    op.drop_table('transactions')
    # ### end Alembic commands ###