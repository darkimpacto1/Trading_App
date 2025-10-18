import Database as db
import pandas as pd
def export_to_csv():
    print("\n🔽 Export Options:")
    print("1. Export by Symbol")
    print("2. Export by Operations (raw data)")
    print("3. Export by Week")
    print("4. Export by Month")
    print("5. Export by Year")
    print("6. Export by Day")
    choice = input("Select export type (1–6): ")

    symbol = input("Enter symbol (or leave blank for all): ").upper()
    filename = input("Enter filename (e.g., export.csv): ")

    # For grouped exports, get date range
    if choice in ["3", "4", "5", "6"]:
        start = input("Start date (YYYY-MM-DD): ")
        end = input("End date (YYYY-MM-DD): ")

    # Grouping expressions
    group_map = {
        "3": ("strftime('%Y-%W', date)", "Week"),
        "4": ("strftime('%Y-%m', date)", "Month"),
        "5": ("strftime('%Y', date)", "Year"),
        "6": ("strftime('%Y-%m-%d', date)", "Day"),
    }

    try:
        if choice == "1":  # Export by Symbol
            query = "SELECT * FROM stock WHERE symbol = ?" if symbol else "SELECT * FROM stock"
            df = pd.read_sql_query(query, db.conn, params=(symbol,) if symbol else ())

        elif choice == "2":  # Export all operations (raw data)
            df = pd.read_sql_query("SELECT * FROM stock", db.conn)

        elif choice in group_map:
            group_sql, label = group_map[choice]
            query = f"""
                SELECT 
                    symbol,
                    {group_sql} AS group_label,
                    AVG(open) AS avg_open,
                    AVG(high) AS avg_high,
                    AVG(low) AS avg_low,
                    AVG(close) AS avg_close,
                    SUM(volume) AS total_volume
                FROM stock
                WHERE date BETWEEN ? AND ?
                {"AND symbol = ?" if symbol else ""}
                GROUP BY symbol, group_label
                ORDER BY symbol, group_label
            """
            params = (start, end, symbol) if symbol else (start, end)
            df = pd.read_sql_query(query, db.conn, params=params)
            df.rename(columns={"group_label": label}, inplace=True)

        else:
            print("❌ Invalid option.")
            return

        df.to_csv(filename, index=False)
        print(f"✅ Data exported to '{filename}'")
    except Exception as e:
        print("❌ Export error:", e)