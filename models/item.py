import sqlite3
from db import db


class ItemModel(db.Model):
    # TABLE_NAME = "items"
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return cls(*row)
        return ItemModel.query.filter_by(name=name).first()

    def save_to_db(self):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "INSERT INTO {table} VALUES(?, ?)".format(table=self.TABLE_NAME)
        # cursor.execute(query, (self.name, self.price))

        # connection.commit()
        # connection.close()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "UPDATE {table} SET price=? WHERE name=?".format(table=self.TABLE_NAME)
        # cursor.execute(query, (self.price, self.name))

        # connection.commit()
        # connection.close()
        db.session.delete(self)
        db.session.commit()
