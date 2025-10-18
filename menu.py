import Database as db
import export_file as ef
def main_menu():
    while True:
        print("\n📂 STOCK DATA MENU")
        print("1. List Companies")
        print("2. View Stock Operations by Ticket")
        print("3. Filter Operations by Date Range")
        print("4. Export to CSV")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            db.list_companies()
        elif choice == "2":
            db.view_stock_operations()
        elif choice == "3":
            db.filter_by_date()
        elif choice == "4":
            ef.export_to_csv()
        elif choice == "5":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice, try again.")


