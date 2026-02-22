from tabulate import tabulate
from app.services import table_logic as tl

def print_menu(mu):
    result = mu.show_menu()
    if result:
        print(tabulate(result, headers=["ID", "Name", "Price"], tablefmt="grid"))
    else:
        print("Menu is empty!")

def print_table(tl):
    result = tl.show_table_status()
    if result:
        print(tabulate(result, headers=["ID", "Table Number", "Status"], tablefmt="pipe",colalign=("left", "center", "right")))
    else:
        print("There is no table")

def print_unpaid_orders(ord):
    result = ord.get_unpaid_orders()
    if result is None:
        print("There are no unpaid orders.")
        return
    for table_number, order_id,ord_status, item_list in result:
        print(f"Table Number: {table_number} - Order ID: {order_id} - Order Status: {ord_status}")
        print(tabulate(item_list, headers=["Item", "Quantity"], tablefmt="grid"))

def print_daily_sales_report(ord):
    result, total_price = ord.get_daily_sales_report()
    if not result:
        print("No orders have been placed for today.")
        return
    for order_id, items in result:
        print(f"\nOrder ID: {order_id}")
        print(tabulate(items, headers=["Name", "Price", "Quantity", "Sub Total"], tablefmt="grid"))
    final_total = total_price[0] if total_price and total_price[0] else 0
    print(f"\n>>> TOTAL SALES TODAY: {final_total} <<<")
