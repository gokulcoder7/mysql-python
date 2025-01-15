from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database setup (creates the table if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')  # Replace 'mydatabase.db' with your desired name
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
''')
conn.commit()
conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()

        return "Data submitted successfully!"  # You might want a more sophisticated response

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)