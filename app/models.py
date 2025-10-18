
import enum
import uuid
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
from app.db import Base


class BookingStatus(str, enum.Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    cancelled = 'cancelled'
    completed = 'completed'


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.Text, unique=True, nullable=False)
    password_hash = sa.Column(sa.Text, nullable=False)
    full_name = sa.Column(sa.Text)
    role = sa.Column(sa.Text, server_default='user')
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now())


class Resource(Base):
    __tablename__ = 'resources'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.Text, nullable=False)
    capacity = sa.Column(sa.Integer, server_default='1')
    resource_metadata = sa.Column(JSONB, server_default='{}')
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now())


class Booking(Base):
    __tablename__ = 'bookings'

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    resource_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey('resources.id', ondelete='CASCADE'),
        nullable=False
    )
    start_at = sa.Column(sa.DateTime(timezone=True), nullable=False)
    end_at = sa.Column(sa.DateTime(timezone=True), nullable=False)
    status = sa.Column(
        ENUM(BookingStatus, name='booking_status'),
        server_default='pending'
    )
    total_price = sa.Column(sa.Numeric(10, 2), nullable=False, server_default='0')
    currency = sa.Column(sa.String(3), server_default='USD')
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    # period column will be added by migration (tsrange)
