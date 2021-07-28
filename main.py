import sys
import json
from jsonschema import validate, ValidationError, SchemaError
import sqlite3
from sqlite3 import Cursor, Connection


def open_json(file: str) -> dict:
    """Функция, считывающая данные из JSON."""
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


def goods_update(connection: Connection, cur: Cursor, goods_d: dict) -> None:
    """Функция, осуществляющая запись данных в таблицу goods."""
    cur.execute("""SELECT id FROM GOODS WHERE id= ? ;""", (goods_d["id"],))
    connection.commit()
    value = cur.fetchall()
    if value:
        cur.execute(
            """ UPDATE goods SET name = ? , package_height = ? , package_width = ? WHERE id = ?""",
            (goods_d["name"], goods_d["package_params"]["height"], goods_d["package_params"]["width"],
             goods_d["id"]),
        )
        connection.commit()
    else:
        cur.execute(
            """INSERT INTO goods(id, name, package_height, package_width)
                   VALUES( ? , ?, ?, ?);""",
            (goods_d["id"], goods_d["name"], goods_d["package_params"]["height"],
             goods_d["package_params"]["width"]), )
        connection.commit()


def shop_update(connection: Connection, cur: Cursor, goods_d: dict) -> None:
    """Функция, осуществляющая запись данных в таблицу ырщз_goods."""
    for key in goods_d["location_and_quantity"]:
        cur.execute(
            """SELECT good_id, location FROM shops_goods
                WHERE good_id = ? AND location= ?""",
            (goods_d["id"], key["location"]))
        value = cur.fetchall()
        if value:
            cur.execute(
                """ UPDATE shops_goods SET amount = ?
                    WHERE location = ? AND good_id = ?""",
                (goods_d["id"], key["location"], key["amount"]))
            connection.commit()
        else:
            cur.execute(
                """INSERT INTO shops_goods(good_id, location, amount)
                    VALUES( ? , ?, ?);""",
                (goods_d["id"], key["location"], key["amount"]))
            connection.commit()


def app() -> None:
    """Основная функция программы."""
    goods_schema = open_json('goods.schema.json')
    goods_data = open_json('goods.data.json')

    try:
        validate(goods_data, goods_schema)
    except SchemaError:
        print("Ошибка данных! Используемая схема недействительна.")
        sys.exit()
    except ValidationError:
        print("Ошибка данных! JSON не действителен.")
        sys.exit()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.executescript("""
                    CREATE TABLE IF NOT EXISTS goods (
                        id INTEGER NOT NULL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        package_height FLOAT NOT NULL,
                        package_width FLOAT NOT NULL);
                    CREATE TABLE IF NOT EXISTS shops_goods (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        good_id INTEGER NOT NULL,
                        location VARCHAR(255) NOT NULL,
                        amount INTEGER NOT NULL,
                        FOREIGN KEY (good_id) references goods(id));""")
    conn.commit()
    goods_update(conn, cursor, goods_data)
    shop_update(conn, cursor, goods_data)
    conn.cursor().close()
    conn.close()


if __name__ == "__main__":
    app()
