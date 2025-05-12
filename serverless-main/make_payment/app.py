# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import logging
import os
from typing import Dict

from flask import Flask, render_template, request, Response

import sqlalchemy
from connect_unix import connect_unix_socket
from models import Base, User, Account, Invoice, InvoiceItem
from sqlalchemy.orm import Session

app = Flask(__name__)

logger = logging.getLogger()


def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    # use a Unix socket when INSTANCE_UNIX_SOCKET (e.g. /cloudsql/project:region:instance) is defined
    if os.environ.get("INSTANCE_UNIX_SOCKET"):
        return connect_unix_socket()

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )


def make_payment(db: sqlalchemy.engine.base.Engine, account_id, order_id, items) -> None:
    with Session(db) as session:
        total_price = sum(item["price"] for item in items)
        account = session.query(Account).filter_by(id=account_id).first()
        if account.balance >= total_price:
            account.balance = account.balance - total_price
            session.commit()
            invoice_items = [InvoiceItem(quantity=item["quantity"], price=item["price"], product=item["product"]) for item in items]
            invoice = Invoice(account_id=account_id, order_id=order_id, items=invoice_items)
            session.add(invoice)
            session.commit()

