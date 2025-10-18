from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, ForeignKey('users.email'), nullable=False)
    room_id = Column(String, nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    guests = Column(Integer, default=1)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default='pending')
    payment_status = Column(String, default='unpaid')
    payment_method = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship('User', back_populates='bookings')
