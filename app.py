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
                
            finally:
                cur.close()
                conn.close()
    return wrapper

@manager_connection
def add_menu_item(cur, name:str, price:float) -> None:
    name = name.capitalize()
    cur.execute(
        "INSERT INTO menu_items (name, price) VALUES (%s, %s)",
        (name, price)
        )

@manager_connection
def edit_menu_item_price(cur, name:str, price) -> None:
    name = name.capitalize()
    cur.execute(
        "UPDATE menu_items  SET price = %s WHERE name = %s",
        (price, name)
    )

@manager_connection
def show_menu(cur) -> None:
    cur.execute("SELECT id, name, price FROM menu_items ORDER BY id")
    menu = cur.fetchall()
    for item in menu:
        print(f"ID: {item[0]} | Name: {item[1]} | Price: {item[2]}")

@manager_connection
def show_table_status(cur) -> None:
        cur.execute("SELECT * FROM tables")
        tables = cur.fetchall()
        for table in tables:
            print(f"ID: {table[0]} | table_number: {table[1]} | status: {table[2]}")

@manager_connection
def add_table(cur, table_number:int) -> None:
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
def remove_table(cur, table_number:int) -> None:
    cur.execute(
        "DELETE FROM tables WHERE table_number = %s",
        (table_number,)
    )

@manager_connection
def add_order(cur, table_number:int) -> None | int:
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
def update_order_status(cur, order_id:int, new_status:str) -> None:
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
def show_order_details(cur, order_id:int) -> None:
     cur.execute(
          "SELECT menu_items.name FROM orders INNER JOIN order_details ON orders.id = order_details.order_id INNER JOIN menu_items ON order_details.item_id = menu_items.id WHERE orders.id = %s",
          (order_id,)
     )
     items = cur.fetchall()
     for index, item in enumerate(items, start=1):
          print(f"{index} : {item[0]}")

@manager_connection
def get_daily_sales_report(cur) -> None:
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

def get_input(type_value:object, prompt: str = "Please enter value: ") -> int | float | str:
    ''' This function takes input and checks its type. '''
    while True:
        try:
            user_input = input(prompt)
            check = user_input.replace(" ","")

            if not user_input:
                print("Input cannot be empty!")
                input(...)
                continue

            if type_value == int or type_value == float:
                return type_value(check)
            
            if type_value == str:
                if check.isalpha():
                    return user_input
                else:
                    print("Invalid input! Please use only letters.")
                    input("...")
                    continue
        except:
            print("Invalid value. Please enter the correct value!")
            input("...")

def manage_restaurant():
    while True:
        print("\n--- Restaurant Management ---")
        print("1. Add a new table")
        print("2. Change table status")
        print("3. Remove a table")
        print("4. Add menu item")
        print("5. Change in item prices")
        print("6. Back to main menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            t_num = get_input(int, "Enter new table number: ")
            add_table(t_num)
            
        elif choice == "2":
            t_number = get_input(int, "Enter table number: ")
            new_status = get_input(str, "Enter new table status: ")
            update_table_status(t_number, new_status)
            input("...")

        elif choice == "3":
            t_num = get_input(int, "Enter table number to remove: ")
            remove_table(t_num)
            input("...")

        elif choice == "4":
            name = get_input(str, "Please enter the name of the food: ")
            price = get_input(float, "Please enter the price (example: 100.00)")
            add_menu_item(name, price)
            input("...")

        elif choice == "5":
            name = get_input(str, "Please enter the name of the food: ")
            price = get_input(float, "Please enter the new price (example: 100.00)")
            edit_menu_item_price(name, price)
            input("...")
        
        elif choice == "6":
            break

        else:
            print("Invalid choice!")

def main_menu():
    while True:
        print("\n=== Restaurant Management System ===")
        print("1. Show Menu")
        print("2. Show Table Status")
        print("3. Add New Order")
        print("4. Update Order Status")
        print("5. View Order Details")
        print("6. Show Daily Sales Report")
        print("7. Manage Restaurant")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_menu()
            input("...")

        elif choice == "2":
            show_table_status()
            input("...")

        elif choice == "3":
            t_num = get_input(int,"Enter table number: ")
            order_id = add_order(t_num)
            if not order_id == None:
                print(f"Order created with ID: {order_id}")
                flag = True
                while flag:
                    print("-"*30)
                    show_menu()
                    print("-"*30)
                    print("What item can you add to this order?")
                    item_id = get_input(int, "Please enter the desired item ID: ")
                    quantity = get_input(int, "Please enter the number of items you want: ")
                    add_item_to_order(order_id, item_id, quantity)
                    continue_status = get_input(str, "Do you want to add another item?[Y/N]").upper()
                    if continue_status in ["N", "NO", "NA", "NAKHER"]:
                        flag = False
                        input("...")
                    input("...")

        elif choice == "4":
            o_id = get_input(int,"Enter Order ID: ")
            status = get_input(str,"Enter new status (received, preparing, ready, paid): ")
            update_order_status(o_id, status)

        elif choice == "5":
            o_id = get_input(int, "Enter Order ID to view details: ")
            show_order_details(o_id)

        elif choice == "6":
            get_daily_sales_report()

        elif choice == "7":
            manage_restaurant()

        elif choice == "8":
            print("Goodbye!")
            input("...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()
     