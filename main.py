from app.database.database_manager import DatabaseManager, SuperDatabaseManager
from app.services.user_manager import UserManager
from app.services.table_manager import TableManager
from app.services.menu_manager import MenuManager
from app.services.order_manager import OrderManager
from app.models.user import Users
from app.models.table import TableStatus
from app.models.orders import OrderStatus
from app.models.user import UserRoles
from app.utils.validators import get_input, get_valid_choice
from app.utils.show_logo import clear, show_start
from dotenv import load_dotenv
from tabulate import tabulate
import os
load_dotenv()

class DefaultAdmin:
    def __init__(self, username):
        self.username = username
        self.roles = UserRoles("admin")

def login(db_manager, us_manager):
    while True:
        username = get_input(str, "Please enter your username: ")
        password = get_input(str, "Please enter your password: ")
        def_user = os.getenv("DEFAULT_ADMIN_USERNAME")
        def_pass = os.getenv("DEFAULT_ADMIN_PASSWORD")
        if username ==  def_user and password == def_pass:
            print("Logged in as default admin.")
            input("\nPress Enter to continue...")
            clear()
            return True, DefaultAdmin(username)
        try:
            result, user_object, text = us_manager.login(username, password)
            if result:
                print(text)
                input("\nPress Enter to continue...")
                clear()
                return True, user_object
            else:
                print(text)
                choice = input("Will you try again?[Y/N]: ").strip().upper()
                if choice in ["N","NO", "NAKHER","NA"]:
                    clear()
                    return False, None
        except Exception as er:
            print(f"Error: {er}")
            input("\nPress Enter to continue...")
            clear()
            return False, None

def user_registration(us_manager: UserManager):
    while True:
        username = get_input(str, "Please enter a new username: ")
        password = get_input(str, "Please enter a new password: ")
        role = get_valid_choice(['admin', 'waiter'], "Please select a role (admin, waiter): ")
        clear()
        print(f"Username: {username} | Password: {password} | roles: {role}")
        wever = get_valid_choice(['y','n'], "Are you sure about adding user?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        role_obj = UserRoles(role)
        result, info = us_manager.register(username, password, role_obj)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            clear()
            return
        print(f"Username: {info.username} | ID {info.id}  was successfully added.")
        input("\nPress Enter to return...")
        clear()
        return

def delete_username(us_manager: UserManager):
    while True:
        username = get_input(str, "Please enter a username: ")
        wever = get_valid_choice(['y','n'], f"Are you sure about delete {username}?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        result, info = us_manager.delete_user(username)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return     

def change_password_password(us_manager: UserManager):
    while True:
        username = get_input(str, "Please enter a username: ")
        old_password = get_input(str, "Please enter a old password: ")
        new_password = get_input(str, "Please enter a new password: ")
        clear()
        wever = get_valid_choice(['y','n'], f"Are you sure about change password {username}?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        result, info = us_manager.change_password(username, old_password, new_password)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return

def show_assign_tables_all_waiter(us_manager: UserManager):
    result, data = us_manager.get_assign_tables_all_waiter()
    if not result:
        print(data)
        input("\nPress Enter to return...")
        clear()
        return
    for item in data:
        print(f"ID: {item.id}, Username: {item.username}, Roles: {item.roles.value}")
        table_data = [[item.id, item.table_number, item.status.value] for item in item.assigned_tables]
        headers = ["ID", "Table Number", "Status"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    input("\nPress Enter to return...")
    clear()

def add_assign_table_to_waiter(us_manager: UserManager, ta_manager: TableManager):
    while True:
        username = get_input(str, "Please enter a username: ")
        table_number = get_input(int, "Please enter the table number: ")
        wever = get_valid_choice(['y','n'], f"Are you sure about assign table {table_number} to {username}?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        result, obj = ta_manager.existence_table(table_number)
        if not result:
            print("The requested table was not found.")
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        res, info = us_manager.assign_table_to_waiter(username, obj.id)
        if not res:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return

def remove_assign_tables_all_waiter(us_manager: UserManager, ta_manager: TableManager):
    while True:
        username = get_input(str, "Please enter a username: ")
        table_number = get_input(int, "Please enter the table number: ")
        wever = get_valid_choice(['y','n'], f"Are you sure about remove table {table_number} assign {username}?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        result, obj = ta_manager.existence_table(table_number)
        if not result:
            print("The requested table was not found.")
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        res, info = us_manager.remove_table_from_waiter(username, obj.id)
        if not res:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return

def show_all_tables(ta_manager: TableManager):
    result , info = ta_manager.get_all_tables()
    if not result:
        print(info)
        input("\nPress Enter to return...")
        clear()
        return
    table_data = [[item.id, item.table_number, item.status.value] for item in info]
    headers = ["ID", "Table Number", "Status"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    input("\nPress Enter to return...")
    clear()

def show_tables_by_status(ta_manager: TableManager):
    status = get_valid_choice(["available", "occupied"], "Please select a status tables (available, occupied): ")
    status_obj = TableStatus(status)
    result, info = ta_manager.get_tables_by_status(status_obj)
    if not result:
        print(info)
        input("\nPress Enter to return...")
        clear()
        return
    table_data = [[item.id, item.table_number, item.status.value] for item in info]
    headers = ["ID", "Table Numbre", "Status"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    input("\nPress Enter to return...")
    clear()

def add_table(ta_manager: TableManager):
    while True:
        table_number = get_input(int, "Please enter new table number: ")
        res, text = ta_manager.add_table(table_number)
        if not res:
            print(text)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(text)
        input("\nPress Enter to return...")
        clear()
        return
    
def change_table_status(ta_manager: TableManager):
    while True:
        table_number = get_input(int, "Please enter table number: ")
        new_status = get_valid_choice(["available", "occupied"], "Please select a status tables (available, occupied): ")
        wever = get_valid_choice(['y','n'], f"Are you sure about change table {table_number} to {new_status} ?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        status_obj = TableStatus(new_status)
        result, info = ta_manager.change_status_table(table_number, status_obj)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return

def delete_table(ta_manager: TableManager):
    while True:
        table_number = get_input(int, "Please enter table number: ")
        wever = get_valid_choice(['y','n'], f"Are you sure about delete table {table_number}?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        result, info = ta_manager.delete_table(table_number)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return

def show_all_items(me_manager: MenuManager, direct: bool= True):
    result, data = me_manager.get_all_items()
    if not result:
        print(data)
        input("\nPress Enter to return...")
        clear()
        return
    item_data = [[item.id, item.name, item.price, item.portions_left] for item in data]
    header = ['ID', 'Name', 'Price', 'Protions Left']
    print(tabulate(item_data, headers=header, tablefmt='grid'))
    if direct:
        input("\nPress Enter to return...")
        clear()

def add_item(me_manager: MenuManager):
    while True:
        name = get_input(str, "Please enter the item name: ")
        price = get_input(float, "Please enter the item price: ")
        portions_left = get_input(int, "Please enter the porsions left: ")
        clear()
        wever = get_valid_choice(['y','n'], f"Are you sure about adding {name} | {price} | {portions_left} ?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        result, info = me_manager.add_item(name, price, portions_left)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return

def change_price_item(me_manager: MenuManager):
    while True:
        name = get_input(str, "Please enter the item name: ")
        new_price = get_input(float, "Please enter the new price: ")
        wever = get_valid_choice(['y','n'], f"Are you sure about changing {name} to {new_price}?[Y/N] ")
        if not wever:
            clear()
            continue
        result, info = me_manager.change_price(name, new_price)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return

def change_portions_left_item(me_manager: MenuManager):
    while True:
        name = get_input(str, "Please enter the item name: ")
        new_portions_left = get_input(int, "Please enter the new porsions left: ")
        clear()
        wever = get_valid_choice(['y','n'], f"Are you sure about changing portions left {name} to {new_portions_left}?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        result, info = me_manager.change_portions_left(name, new_portions_left)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return

def delete_item(me_manager: MenuManager):
    while True:
        name = get_input(str, "Please enter the item name: ")
        wever = get_valid_choice(['y','n'], f"Are you sure about delete {name}?[Y/N] ")
        if wever == 'n':
            clear()
            continue
        result, info = me_manager.delete_item(name)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(info)
        input("\nPress Enter to return...")
        clear()
        return

def show_waiter_orders(user_obj: Users, or_manager: OrderManager):
    result, info = or_manager.get_waiter_orders(user_obj.username)
    if not result:
        print(info)
        input("\nPress Enter to return...")
        clear()
        return
    if not info:
        print("No order has been registered to you today.")
        input("\nPress Enter to return...")
        clear()
        return
    for order_obj in info:
        print(f"ID: {order_obj.id} | Table: {order_obj.table.table_number} | Status: {order_obj.status.value} | Time: {order_obj.order_time}")
        print("--"*20)
        item_data = [[orderitem_obj.menu_item.name, orderitem_obj.quantity, orderitem_obj.menu_item.price, orderitem_obj.menu_item.portions_left] for orderitem_obj in order_obj.items]
        header = ['Name', 'Quantity', 'Price', 'Protions Left']
        print(tabulate(item_data, headers=header, tablefmt='grid'))
        print("--"*20)
    input("\nPress Enter to return...")
    clear()

def add_Order(user_obj: Users, or_manager: OrderManager, me_manager: MenuManager):
    while True:
        username = get_input(str, "Please enter a username: ")
        table_number = get_input(int, "Please enter the table number: ")
        result, data = or_manager.add_order(username, table_number)
        if not result:
            print(data)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        clear()
        while True:
            show_all_items(me_manager, direct=False)
            name_item = get_input(str, "Please enter the item name: ")
            quantity_item = get_input(int, "Please enter the quantity item: ")
            result, info = or_manager.add_item_to_order(data, name_item, quantity_item)
            print(info)
            choi = get_valid_choice(['y','n'], "do you add another item?[Y/N] ")
            if choi == 'n':
                input("\nPress Enter to return...")
                clear()
                return
            clear()

def change_order_status(user_obj: Users, or_manager: OrderManager):
    while True:
        order_id = get_input(int, "Please enter the order id: ")
        result, info = or_manager.existence_order(order_id)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        status = get_valid_choice(['received','cancelled', 'preparing', 'ready', 'paid'], "Please enter the order id (received, cancelled, preparing, ready, paid): ")
        new_status = OrderStatus(status)
        resul, text = or_manager.update_order_status(info, new_status)
        if not resul:
            print(text)
            wever = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if wever == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        print(text)
        input("\nPress Enter to return...")
        clear()
        return

def add_items_from_order(or_manager: OrderManager, me_manager: MenuManager):
    while True:
        order_id = get_input(int, "Please enter the order id: ")
        result, info = or_manager.existence_order(order_id)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        clear()
        while True:
            show_all_items(me_manager, direct=False)
            name_item = get_input(str, "Please enter the item name: ")
            quantity_item = get_input(int, "Please enter the quantity item: ")
            result, text = or_manager.add_item_to_order(info, name_item, quantity_item)
            if not result:
                print(text)
                wever = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
                if wever == 'y':
                    clear()
                    continue
                input("\nPress Enter to return...")
                clear()
                return
            print(text)
            que = get_valid_choice(['y','n'], "Add another item to the order?[Y/N] ")
            if que == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return

def update_item_quantity_from_order(or_manager: OrderManager):
    while True:
        order_id = get_input(int, "Please enter the order id: ")
        result, info = or_manager.existence_order(order_id)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        while True:
            name_item = get_input(str, "Please enter the item name: ")
            new_quantity = get_input(int, "Please enter the new quantity item: ")
            resul, text = or_manager.update_item_quantity(info, name_item, new_quantity)
            if not resul:
                print(text)
                ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
                if ques == 'y':
                    clear()
                    continue
                input("\nPress Enter to return...")
                clear()
                return
            print(text)
            input("\nPress Enter to return...")
            clear()
            return

def remove_item_from_order(or_manager: OrderManager):
    while True:
        order_id = get_input(int, "Please enter the order id: ")
        result, info = or_manager.existence_order(order_id)
        if not result:
            print(info)
            ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
            if ques == 'y':
                clear()
                continue
            input("\nPress Enter to return...")
            clear()
            return
        while True:
            name_item = get_input(str, "Please enter the item name: ")
            resu, text = or_manager.remove_item_from_order(info, name_item)
            if not resu:
                print(text)
                ques = get_valid_choice(['y','n'], "Are you trying again?[Y/N] ")
                if ques == 'y':
                    clear()
                    continue
                input("\nPress Enter to return...")
                clear()
                return
            print(text)
            input("\nPress Enter to return...")
            clear()
            return

def export_invoice_from_order(or_manager: OrderManager):
    order_id = get_input(int, "Please enter the order id: ")
    result, order_obj = or_manager.existence_order(order_id)
    if not result:
        print(order_obj)
        input("\nPress Enter to return...")
        clear()
    print(f"ID: {order_obj.id} Table: {order_obj.table.table_number} Status: {order_obj.status.value} Time: {order_obj.order_time}")
    order_item = [[orderitem_obj.menu_item.name, orderitem_obj.quantity, orderitem_obj.menu_item.price, orderitem_obj.menu_item.portions_left] for orderitem_obj in order_obj.items]
    header = ['Name', 'Quantity', 'Price', 'Portions left']
    print(tabulate(order_item, headers=header, tablefmt='grid'))
    print("+-"*20)
    print(f"Total amount>>> {or_manager.get_invoice(order_obj)} <<<")
    input("\nPress Enter to return...")
    clear()

def restaurant_menu(us_manager: UserManager, ta_manager: TableManager, me_manager: MenuManager):
    actions = {
    "1": ("Add a new username", lambda: user_registration(us_manager)),
    "2": ("Delete a username", lambda: delete_username(us_manager)),
    "3": ("Change username's password", lambda: change_password_password(us_manager)),
    "4": ("View tables assigned to all waiters", lambda: show_assign_tables_all_waiter(us_manager)),
    "5": ("Add Assign table to waiter", lambda: add_assign_table_to_waiter(us_manager, ta_manager)),
    "6": ("Remove Assign table to waiter", lambda: remove_assign_tables_all_waiter(us_manager, ta_manager)),
    "7": ("View all the tables", lambda: show_all_tables(ta_manager)),
    "8": ("View all the tables by status", lambda: show_tables_by_status(ta_manager)),
    "9": ("Add table", lambda: add_table(ta_manager)),
    "10": ("Change table status", lambda: change_table_status(ta_manager)),
    "11": ("Remove a table", lambda: delete_table(ta_manager)),
    "12": ("View all item menu", lambda: show_all_items(me_manager)),
    "13": ("Add item", lambda: add_item(me_manager)),
    "14": ("Change price iteme", lambda: change_price_item(me_manager)),
    "15": ("Change portions left iteme", lambda: change_portions_left_item(me_manager)),
    "16": ("Remove a item", lambda: delete_item(me_manager)),
    "0": ("Exit",""),
    }
    while True:
        print("+-"*20)
        for key, (title, _) in actions.items():
            print(f"{key}. {title}")
        print("+-"*20)
        choice = input("Select: ")

        if choice == "0":
            clear()
            break

        action_data = actions.get(choice)

        if action_data:
            _,action_fun = action_data
            clear()
            action_fun()
        else:
            print("Invalid option")

def waiter_menu(user_obj: Users, or_manager: OrderManager, me_manager: MenuManager):
    actions = {
        "1": ("Show all orders", lambda: show_waiter_orders(user_obj, or_manager)),
        "2": ("Add a new order", lambda: add_Order(user_obj, or_manager, me_manager)),
        "3": ("Change order status", lambda: change_order_status(user_obj, or_manager)),
        "4": ("Add item from order", lambda: add_items_from_order(or_manager, me_manager)),
        "5": ("Update item quantity from order", lambda: update_item_quantity_from_order(or_manager)),
        "6": ("Remove item from order", lambda: remove_item_from_order(or_manager)),
        "7": ("Export invoice order", lambda: export_invoice_from_order(or_manager)),
        "0": ("Exit", "")
    }

    while True:
        print("-+"*20)
        for key, (title, _) in actions.items():
            print(f"{key}. {title}")
        print("-+"*20)
        choice = input("Select: ")

        if choice == "0":
            clear()
            break

        action_data = actions.get(choice)

        if action_data:
            _,action_fun = action_data
            clear()
            action_fun()
        else:
            print("Invalid option")

def database_menu(db_manager: DatabaseManager):
    sdb_manager = SuperDatabaseManager()
    re, info = sdb_manager.create_database()
    print("-"*20)
    print(info)
    print("-"*20)
    if not re:
        input("\nPress Enter to return...")
        clear()
        return False
    input("\nPress Enter to continue...")
    clear()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(BASE_DIR, "database", "schema.sql")
    res = db_manager.run_script_file(schema_path)
    if not res:
        print("Tables could not be created")
        input("\nPress Enter to return...")
        clear()
        return False
    trigger_path = os.path.join(BASE_DIR, "database", "triggers.sql")
    print("="*20)
    print("Tables were created")
    print("="*20)
    input("\nPress Enter to continue...")
    clear()
    resu = db_manager.run_script_file(trigger_path)
    if not resu:
        print("Triggers were not created.")
        input("\nPress Enter to return...")
        clear()
        return False
    print("*"*20)
    print("Triggers were successfully created.")    
    print("*"*20)
    input("\nPress Enter to return...")
    clear()


def main_menu(flag):
    db_manager = DatabaseManager()
    us_manager = UserManager(db_manager)
    ta_manager = TableManager(db_manager)
    me_manager = MenuManager(db_manager)
    or_manager = OrderManager(db_manager, us_manager,me_manager,ta_manager)
    logged_in, user_obj = login(db_manager, us_manager)
    if not logged_in:
        return
    
    while True:
        result, info = db_manager.get_connect()
        if result and flag:
            show_start()
        flag= False
        print(20*"=|")
        print("1. Restaurant Management")
        print("2. Waiter Orders")
        print("3. Database Management")
        print("0. Exit")
        print(20*"=|")
        if not result:
            print("\nWarning: for the lack of the database or not making tables,\nPlease manually choose ( 3 ) to make the database or  act manually.\n")

        choice = input("Select: ")
        print()
        
        
        match choice:
            case "1":
                if not result:
                    print("First, create the database in option 3.")
                    input("\nPress Enter to continue...")
                    clear()
                    continue
                if user_obj.roles.value == "admin":
                    clear()
                    restaurant_menu(us_manager, ta_manager, me_manager)
                else:
                    print("You do not have access to this section.")
                    input("\nPress Enter to continue...")
                    clear()

            case "2":
                if not result:
                    print("First, create the database in option 3.")
                    input("\nPress Enter to continue...")
                    clear()
                    continue
                clear()
                waiter_menu(user_obj, or_manager, me_manager)

            case "3":
                if user_obj.roles.value == "admin" and not result:
                    clear()
                    database_menu(db_manager)
                print("Database , Tables , and Trigger are already built")
                input("\nPress Enter to continue...")
                flag = False
                clear()

            case "0":
                print("I don 't say goodbye because i like to see you again .")
                input("...")
                clear()
                break

            case _:
                print("Invalid option")
                input("\nPress Enter to continue...")
                clear()

if __name__ == "__main__":
    main_menu(flag=True)