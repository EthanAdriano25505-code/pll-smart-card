import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect('agencies.db')
c = conn.cursor()

# Create the agencies table with specified fields
c.execute('''
    CREATE TABLE IF NOT EXISTS agencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        စက်ရုံအမည် TEXT NOT NULL,
        အေးဂျင့်အမည် TEXT NOT NULL,
        အလုပ်သမားများအမည် TEXT NOT NULL,
        မူဆယ်ရောက်ပြီးလူစာရင်း TEXT,
        တရုတ်ပြည်ရောက်ပြီးလူစာရင်း TEXT
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()
