from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    email: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    accounts: Mapped[List["Account"]] = relationship(back_populates="user")


class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="accounts")

class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[int]

class Invoice(Base):
    __tablename__ = "invoice"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int]
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    items: Mapped["InvoiceItem"] = relationship(back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = "invoice_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    price: Mapped[int]
    product: Mapped[str]
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoice.id"))
    invoice: Mapped["Invoice"] = relationship(back_populates="items")