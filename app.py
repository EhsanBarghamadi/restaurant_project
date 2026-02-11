import psycopg2

def get_connection():
    '''
    This function is for connecting to the database.
    '''
    try:
        connection = psycopg2.connect(
            dbname="restaurant_db",
            user="postgres",
            password="pass",
            host="localhost",
            port="5432"
        )
        return connection
    
    except Exception as error:
        print(f"Error in connection:\n {error}")
        return None

def manager_connection(fun):
    def wrapper(*args, **kwargs):
        conn = get_connection()
        if conn:
            try:
                cur = conn.cursor()
                result = fun(cur, *args, **kwargs)
                conn.commit()
                return result
            
            except Exception as error:
                conn.rollback()
                print(f"Error: {error}")
                raise

            finally:
                cur.close()
                conn.close()
    return wrapper

@manager_connection
def add_menu_item(cur, name:str, price:float):
    name = name.capitalize()
    cur.execute(
        "INSERT INTO menu_items (name, price) VALUES (%s, %s)",
        (name, price)
        )

@manager_connection
def edit_menu_item_price(cur, name:str, price):
    cur.execute(
        "UPDATE menu_items  SET price = %s WHERE name = %s",
        (price, name)
    )

@manager_connection
def show_menu(cur):
    cur.execute("SELECT id, name, price FROM menu_items ORDER BY id")
    menu = cur.fetchall()
    for item in menu:
        print(f"ID: {item[0]} | Name: {item[1]} | Price: {item[2]}")

@manager_connection
def show_table_status(cur):
        cur.execute("SELECT * FROM tables")
        tables = cur.fetchall()
        for table in tables:
            print(f"ID: {table[0]} | table_number: {table[1]} | status: {table[2]}")

@manager_connection
def add_table(cur, table_number):
        cur.execute(
            "INSERT INTO tables (table_number) VALUES (%s)",
            (table_number,)
            )
        
@manager_connection
def update_table_status(cur, table_number:int, new_status:str):
    cur.execute(
        "UPDATE tables SET status = %s WHERE table_number = %s",
        (new_status,table_number)
    )

@manager_connection
def remove_table(cur,table_number:int):
    cur.execute(
        "DELETE FROM tables WHERE table_number = %s",
        (table_number,)
    )

@manager_connection
def add_order(cur, table_number):
    cur.execute(
        "SELECT id FROM tables WHERE table_number = %s",
        (table_number,)
    )
    table_data = cur.fetchone()
    if not table_data:
            print(f"Table {table_number} not found!")
            return None
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
    return order_id

@manager_connection
def update_order_status(cur, order_id:int, new_status:str):
    cur.execute(
         "UPDATE orders SET status = %s WHERE id = %s",
         (new_status, order_id)
    )
    if new_status == "paid":
         cur.execute(
              "UPDATE tables SET status = 'available' WHERE id = (SELECT table_id FROM orders WHERE id = %s)",
              (order_id,)
         )

@manager_connection
def show_active_orders(cur):
    cur.execute(
          "SELECT orders.id, tables.table_number, orders.status from tables INNER JOIN 	orders ON tables.id = orders.table_id WHERE orders.status != 'paid';"
    )
    items = cur.fetchall()
    for item in items:
         print(f"Order ID: {item[0]} | Table Number: {item[1]} | Order status: {item[2]}")

@manager_connection
def show_order_details(cur, order_id):
     cur.execute(
          "SELECT menu_items.name FROM orders INNER JOIN order_details ON orders.id = order_details.order_id INNER JOIN menu_items ON order_details.item_id = menu_items.id WHERE orders.id = %s",
          (order_id,)
     )
     items = cur.fetchall()
     for index, item in enumerate(items, start=1):
          print(f"{index} : {item[0]}")

@manager_connection
def get_daily_sales_report(cur):
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
    print(f"Daily sales report => {result[0]}")

@manager_connection
def add_item_to_order(cur, order_id, item_id, quantity):
     cur.execute(
          """
            INSERT INTO order_details(order_id, item_id, quantity)
            VALUES
            (%s,%s,%s)
        """,
        (order_id, item_id, quantity)
     )
     