import sqlite3

# Initialize database
conn = sqlite3.connect('familyguardian.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS known_faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL
)
''')
conn.commit()

# Add a known face
def add_face(name, encoding):
    cursor.execute("INSERT INTO known_faces (name, encoding) VALUES (?, ?)", (name, encoding))
    conn.commit()

# Example usage
add_face("Alice", known_face_encodings[0])
