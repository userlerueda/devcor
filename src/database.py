#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A simple Flask web app that demonstrates the Model View Controller
(MVC) pattern in a meaningful and somewhat realistic way.
"""

import json
import time

from sqlalchemy import (Column, Float, MetaData, String, Table, create_engine,
                        exc)


class Database:
    """
    Represent the interface to the data (model). Can read from a
    simple file such as JSON, YAML, or XML. Uses JSON by default.
    """

    def __init__(self, db_url, seed_path):
        """
        Constructor builds the object. Path determines what kind of SQL
        database should be used. Can be MySQL, sqlite, postgreSQL, etc.
        """

        for _ in range(10):
            try:
                self.engine = create_engine(db_url)
                self.meta = MetaData(self.engine)

                self.table = Table(
                    "accounts",
                    self.meta,
                    Column("acctid", String(15), primary_key=True),
                    Column("paid", Float, nullable=False),
                    Column("due", Float, nullable=False),
                )

                self.meta.create_all()
                self.connect()
                break

            except exc.SQLAlchemyError as err:
                print(f"Failed to connect to database: {err}")
                time.sleep(5)

        if not hasattr(self, "conn") or self.conn.closed:
            raise TimeoutError("Could not establish session to mysql_db")

        with open(seed_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        self.result = self.conn.execute(self.table.insert(), data)
        self.disconnect()

    def connect(self):
        """
        Open (connect) the connection to the database.
        """
        self.conn = self.engine.connect()
        if self.conn.closed:
            raise OSError("connect() succeeded but connection is still closed")

    def disconnect(self):
        """
        Close (disconnect) the connection to the database.
        """
        if hasattr(self, "conn") and not self.conn.closed:
            self.conn.close()
            if not self.conn.closed:
                raise OSError("disconnect() succeded but session is still open")

    def balance(self, acct_id):
        """
        Determines the customer balance by finding the difference between
        what has been paid and what is still owed on the account, The "model"
        can provide methods to help interface with the data; it is not
        limited to only storing data. A positive number means the customer
        owes us money and a negative number means they overpaid and have
        a credit with us.
        """
        selected_acct = self.table.select().where(
            self.table.c.acctid == acct_id.upper()
        )
        result = self.conn.execute(selected_acct)
        acct = result.fetchone()
        if acct:
            bal = float(acct["due"]) - float(acct["paid"])
            return f"{bal:.2f} USD"

        return None
