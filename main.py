from app.services import table_logic as tl
from app.services import menu_logic as mu
from app.services import order_logic as ord
from app.utils import show
from app.utils.validators import get_input, get_valid_choice

def manage_restaurant():
    while True:
        print("\n--- Restaurant Management ---")
        print("1. View all tables")
        print("2. Add a new table")
        print("3. Change table status")
        print("4. Remove a table")
        print("5. Show Menu")
        print("6. Add menu item")
        print("7. Change in item prices")
        print("8. Remove item from menu")
        print("9. Back to main menu")
        
        print()
        choice = get_input(int, "Enter your choice: ")
        print()

        if choice == 1:
            show.print_table(tl)
            print()
            input("Enter to return...")

        elif choice == 2:
            show.print_table(tl)
            print()
            t_num = get_input(int, "Enter new table number: ")
            result, text = tl.add_table(t_num)
            print(text)
            print()
            input("Enter to return...")
            
        elif choice == 3:
            show.print_table(tl)
            print()
            t_number = get_input(int, "Enter table number: ")
            new_status = get_valid_choice(['available', 'occupied'], "Enter new table status('available', 'occupied'): ")
            result, text = tl.update_table_status(t_number, new_status)
            print(text)
            print()
            input("Enter to return...")

        elif choice == 4:
            show.print_table(tl)
            print()
            t_num = get_input(int, "Enter table number to remove: ")
            result, text = tl.remove_table(t_num)
            print(text)
            print()
            input("Enter to return...")

        elif choice == 5:
            show.print_menu(mu)
            print()
            input("Enter to return...")

        elif choice == 6:
            show.print_menu(mu)
            print()            
            name = get_input(str, "Please enter the name of the item: ")
            price = get_input(float, "Please enter the price (example: 100.00): ")
            if price > 0.0:
                result, text = mu.add_menu_item(name, price)
                print(text)
                print()
                input("Enter to return...")
            else:
                print("Price cannot be negative or zero.")

        elif choice == 7:
            show.print_menu(mu)
            print()            
            name = get_input(str, "Please enter the name of the item: ")
            price = get_input(float, "Please enter the new price (example: 100.00): ")
            if price > 0.0:
                result, text = mu.edit_menu_item_price(name, price)
                print(text)
                print()
                input("Enter to return...")
            else:
                print("Price cannot be negative or zero.")
        
        elif choice == 8:
            show.print_menu(mu)
            print()
            name = get_input(str, "Please enter the name of the item: ")
            result, text = mu.remove_item(name)
            print(text)
            print()
            input("Enter to return...")
        
        elif choice == 9:
            break

        else:
            print("Invalid choice!")

def main_menu():
    while True:
        print("\n=== Restaurant Management System ===")
        print("1. Show Menu")
        print("2. Show Table Status")
        print("3. Add New Order")
        print("4. View active orders")
        print("5. Update Order Status")
        print("6. View Order Details with ID")
        print("7. Show Daily Sales Report")
        print("8. Manage Restaurant")
        print("9. Exit")
        
        print()
        choice = get_input(int, "Enter your choice: ")
        print()

        if choice == 1:
            show.print_menu(mu)
            print()
            input("Enter to return...")

        elif choice == 2:
            show.print_table(tl)
            print()
            input("Enter to return...")

        elif choice == 3:
            show.print_table(tl)
            print()
            t_num = get_input(int,"Enter table number: ")
            result, order_id = ord.add_order(t_num)
            if result:
                print(f"Order created with ID: {order_id}")
                flag = True
                print("-|"*30)
                show.print_menu(mu)
                print("-|"*30)
                while flag:
                    print("What item can you add to this order?")
                    item_id = get_input(int, "Please enter the desired item ID: ")
                    quantity = get_input(int, "Please enter the number of items you want: ")
                    if quantity > 0:
                        result,text = ord.add_item_to_order(order_id, item_id, quantity)
                        print(text)
                        continue_status = get_input(str, "Do you want to add another item?[Y/N] ").upper()
                        if continue_status in ["N", "NO", "NA", "NAKHER"]:
                            flag = False
                            input("Enter to return...")
                    else:
                        print("The number of items cannot be negative or zero.")

            else:
                print(order_id)

        elif choice == 4:
            show.print_unpaid_orders(ord)
            print()
            input("Enter to return...")

        elif choice == 5:
            show.print_unpaid_orders(ord)
            print()
            t_num = get_input(int,"Enter the desired table number: ")
            new_status = get_valid_choice(['received','cancelled', 'preparing', 'ready', 'paid'], "Enter new status (received, cancelled, preparing, ready, paid):")
            result, text = ord.update_order_status(t_num, new_status)
            print(text)
            input("Enter to return...")

        elif choice == 6:
            o_id = get_input(int, "Enter Order ID to view details: ")
            result_bool, result = ord.show_order_details(o_id)
            if result_bool:
                print("+"*20)
                for name, quantity in result:
                    print(f"{name} --> {quantity}")
                print("+"*20)
                print()
                input("Enter to return...")

            else:
                print(result)
                print()
                input("Enter to return...")                

        elif choice == 7:
            show.print_daily_sales_report(ord)
            input("Enter to return...")


        elif choice == 8:
            manage_restaurant()

        elif choice == 9:
            print("I'm not saying goodbye because I want to see you again.😙")
            print()
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()