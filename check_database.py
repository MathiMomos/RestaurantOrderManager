# check_database.py INNECESARIO SI QUIEREN BORREN ESTE ARCHIVO YA QUE LO USE UN TOKERPARA CONFIRMAR EL DATABASE UWU

import sqlite3

def check_users():
    conn = sqlite3.connect('data/restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    print("Usuarios:")
    for user in users:
        print(user)
    conn.close()

def check_orders():
    conn = sqlite3.connect('data/restaurant.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT orders.id, users.username, orders.items, orders.status, orders.total 
        FROM orders 
        JOIN users ON orders.user_id = users.id
    """)
    orders = cursor.fetchall()
    print("\nPedidos:")
    for order in orders:
        print(order)
    conn.close()

if __name__ == "__main__":
    check_users()
    check_orders()
