from flask import Flask, request, render_template, redirect, url_for
import mysql.connector as ms

app = Flask(__name__)

# Create a connection to the database
def get_db_connection():
    print('to be Connected....')
    try:
        conn = ms.connect(user='root',password='pwd',host='localhost',database='python01')
        print('Connected....')
        return conn
    except ms.Error as err:
        print('Error:',err)
        return None



# Initialize the database
def init_db():
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute('select * from users;')
    res=mycursor.fetchall()
    for user in res:
        print(user)

    conn.close()

init_db()

# Route for the home page with the form
@app.route('/', methods=('GET', 'POST'))
def index():
    print("esfawsf",request.form)
    print("method", request.method)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        #dob = request.form['dateofbirth']
        dob='2024-10-16'





        # Insert the data into the database
        conn = get_db_connection()
        mycursor = conn.cursor()


        mycursor.execute("SELECT count(username) from users where username='"+name+"'")
        x=mycursor.fetchone()

        print("count=",x[0])
        if(x[0]>=1):
            print("user already exists")
            return redirect(url_for('already'))




        mycursor.execute("INSERT INTO users(username, email,dob,status) VALUES (%s,%s, %s,'Active')", (name, email,dob))
        conn.commit()
        mycursor.close()
       # conn.commit()
        conn.close()

        return redirect(url_for('userlist'))
    else:
        return render_template('index.html')


# Route to display success message
@app.route('/success')
def success():
    return 'Data successfully submitted!'



@app.route('/already')
def already():
    return 'user already exists!'


# Route to display success message
@app.route('/userlist')
def userlist():
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute('select * from users;')
    users = mycursor.fetchall()

    mycursor.close()
    # conn.commit()
    conn.close()
    return render_template('userlist.html',users=users)

if __name__ == '__main__':
    app.run()