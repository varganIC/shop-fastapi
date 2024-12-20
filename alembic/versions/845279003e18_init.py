"""init

Revision ID: 845279003e18
Revises:
Create Date: 2024-10-28 20:11:18.987493

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '845279003e18'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('slug', sa.Text(), nullable=False),
    sa.Column('image', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__category')),
    sa.UniqueConstraint('slug', name=op.f('uq__category__slug'))
    )
    op.create_index(op.f('ix__category__id'), 'category', ['id'], unique=False)
    op.create_index(op.f('ix__category__name'), 'category', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('hashed_password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__user'))
    )
    op.create_index(op.f('ix__user__id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix__user__username'), 'user', ['username'], unique=True)
    op.create_table('subcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('slug', sa.Text(), nullable=False),
    sa.Column('image', sa.Text(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name=op.f('fk__subcategory__category_id__category'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__subcategory')),
    sa.UniqueConstraint('slug', name=op.f('uq__subcategory__slug'))
    )
    op.create_index(op.f('ix__subcategory__category_id'), 'subcategory', ['category_id'], unique=False)
    op.create_index(op.f('ix__subcategory__id'), 'subcategory', ['id'], unique=False)
    op.create_index(op.f('ix__subcategory__name'), 'subcategory', ['name'], unique=True)
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('slug', sa.Text(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('image_small', sa.Text(), nullable=False),
    sa.Column('image_medium', sa.Text(), nullable=False),
    sa.Column('image_large', sa.Text(), nullable=False),
    sa.Column('subcategory_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subcategory_id'], ['subcategory.id'], name=op.f('fk__product__subcategory_id__subcategory'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__product'))
    )
    op.create_index(op.f('ix__product__id'), 'product', ['id'], unique=False)
    op.create_index(op.f('ix__product__name'), 'product', ['name'], unique=False)
    op.create_index(op.f('ix__product__slug'), 'product', ['slug'], unique=True)
    op.create_index(op.f('ix__product__subcategory_id'), 'product', ['subcategory_id'], unique=False)
    op.create_table('bucket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name=op.f('fk__bucket__product_id__product'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk__bucket__user_id__user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__bucket'))
    )
    op.create_index(op.f('ix__bucket__id'), 'bucket', ['id'], unique=False)
    op.create_index(op.f('ix__bucket__product_id'), 'bucket', ['product_id'], unique=False)
    op.create_index(op.f('ix__bucket__user_id'), 'bucket', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix__bucket__user_id'), table_name='bucket')
    op.drop_index(op.f('ix__bucket__product_id'), table_name='bucket')
    op.drop_index(op.f('ix__bucket__id'), table_name='bucket')
    op.drop_table('bucket')
    op.drop_index(op.f('ix__product__subcategory_id'), table_name='product')
    op.drop_index(op.f('ix__product__slug'), table_name='product')
    op.drop_index(op.f('ix__product__name'), table_name='product')
    op.drop_index(op.f('ix__product__id'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix__subcategory__name'), table_name='subcategory')
    op.drop_index(op.f('ix__subcategory__id'), table_name='subcategory')
    op.drop_index(op.f('ix__subcategory__category_id'), table_name='subcategory')
    op.drop_table('subcategory')
    op.drop_index(op.f('ix__user__username'), table_name='user')
    op.drop_index(op.f('ix__user__id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix__category__name'), table_name='category')
    op.drop_index(op.f('ix__category__id'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
