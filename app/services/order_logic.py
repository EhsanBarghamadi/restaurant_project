from utils.db_handler import get_connection,manager_connection

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
def update_order_status(cur, order_id:int, new_status:str) -> tuple[bool, str]:
    cur.execute(
        "SELECT id FROM orders WHERE id = %s",
        (order_id,)
    )
    result = cur.fetchone()
    if result is not None:
        cur.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (new_status, order_id)
        )
        if new_status == "paid":
            cur.execute(
                "UPDATE tables SET status = 'available' WHERE id = (SELECT table_id FROM orders WHERE id = %s)",
                (order_id,)
            )
        return True, "Order status changed successfully."
    return False, "Order not found!"

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
def get_daily_sales_report(cur) -> None | tuple:
    cur.execute(
          """
            SELECT SUM(menu_items.price*order_details.quantity) FROM orders
            INNER JOIN order_details
            ON orders.id = order_details.order_id
            INNER JOIN menu_items
            ON order_details.item_id = menu_items.id
            WHERE orders.status = 'paid' 
            AND orders.order_time::date = CURRENT_DATE; 
          """
     )
    result = cur.fetchone()
    return result
