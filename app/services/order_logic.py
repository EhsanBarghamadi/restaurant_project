from app.utils.db_handler import get_connection,manager_connection

@manager_connection
def add_order(cur, table_number:int) -> tuple[bool, str|int]:
    cur.execute(
        "SELECT id,status FROM tables WHERE table_number = %s",
        (table_number,)
    )
    table_data = cur.fetchone()
    if  table_data is None:
        return False, f"Table {table_number} not found!"
    
    elif table_data[1] == 'occupied':
        return False, "The requested table is occupied."
    
    table_id = table_data[0]

    cur.execute(
            "UPDATE tables SET status = 'occupied' WHERE id = %s",
            (table_id,)
            )
    cur.execute(
        "INSERT INTO orders(table_id, status) VALUES (%s, 'received') RETURNING id",
        (table_id,)
    )
    order_id = cur.fetchone()[0]
    return True, order_id

@manager_connection
def add_item_to_order(cur, order_id:int, item_id:int, quantity:int) -> tuple[bool, str]:
     cur.execute(
           "SELECT name FROM menu_items WHERE id = %s",
           (item_id,)
     )
     result = cur.fetchone()
     if result is not None:
        cur.execute(
            """
                INSERT INTO order_details(order_id, item_id, quantity)
                VALUES
                (%s,%s,%s)
            """,
            (order_id, item_id, quantity)
        )
        return True, f"The desired {result[0]} has been added to the order."
     return False, "The desired item was not found."

@manager_connection
def update_order_status(cur, table_number:int, new_status:str) -> tuple[bool, str]:
    cur.execute(
        """
        SELECT orders.id FROM tables
        INNER JOIN orders ON tables.id = orders.table_id
        WHERE tables.status = 'occupied'
        AND tables.table_number = %s
        """,
        (table_number,)
    )
    find_table = cur.fetchone()
    if find_table is not None:
        cur.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (new_status, find_table[0])
        )
        if new_status == "paid" or new_status == 'cancelled':
            cur.execute(
                "UPDATE tables SET status = 'available' WHERE table_number = %s",
                (table_number,)
            )
        return True, "Order status changed successfully."
    return False, "The requested table is not occupied.!"

@manager_connection
def show_order_details(cur, order_id:int) -> tuple[bool, str | list]:
     cur.execute(
          """SELECT menu_items.name, order_details.quantity FROM orders
            INNER JOIN order_details ON orders.id = order_details.order_id 
            INNER JOIN menu_items ON order_details.item_id = menu_items.id 
            WHERE orders.id = %s""",
          (order_id,)
     )
     items = cur.fetchall()
     if not items:
         return False, "Order not found"
     return True, items

@manager_connection
def get_daily_sales_report(cur) -> tuple:
        cur.execute(
        """
        SELECT id
        FROM orders
        WHERE DATE(order_time) = CURRENT_DATE
        AND status = 'paid'
        """
    )
        order_list = cur.fetchall()
        result = []
        if order_list:
            for (id_order,) in order_list:
                cur.execute(
                    """
                    SELECT meu.name, meu.price, ordd.quantity, meu.price*ordd.quantity
                    FROM orders ord
                    INNER JOIN order_details ordd ON ord.id = ordd.order_id
                    INNER JOIN menu_items meu ON ordd.item_id = meu.id
                    WHERE ord.id = %s
                    """,
                    (id_order,)
                )
                result.append((id_order, cur.fetchall()))

        cur.execute(
            """
            SELECT SUM(menu_items.price * order_details.quantity) 
            FROM orders
            INNER JOIN order_details ON orders.id = order_details.order_id
            INNER JOIN menu_items ON order_details.item_id = menu_items.id
            WHERE DATE(orders.order_time) = CURRENT_DATE 
            AND orders.status = 'paid'
            """
        )
        total_price = cur.fetchone()
        return result, total_price

@manager_connection
def get_unpaid_orders(cur) -> list:
    cur.execute(
        """
        SELECT ta.table_number, ord.id, ord.status
        FROM tables ta
        INNER JOIN orders ord ON ta.id = ord.table_id
        WHERE DATE(ord.order_time) = CURRENT_DATE
        AND ord.status != 'paid'
        AND ord.status != 'cancelled'
        AND ta.status = 'occupied'
        """
    )
    order_list = cur.fetchall()
    result = []
    if order_list:
        for table_number, order_id ,ord_status in order_list:
            cur.execute(
                """
                SELECT meu.name, ordd.quantity FROM orders ord
                INNER JOIN order_details ordd ON ord.id = ordd.order_id
                INNER JOIN menu_items meu ON ordd.item_id = meu.id
                WHERE ord.id = %s
                """,
                (order_id,)
            )
            result.append((table_number,order_id,ord_status, cur.fetchall()))
        return result


