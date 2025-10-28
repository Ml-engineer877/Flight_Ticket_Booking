from flask import Flask, render_template, redirect, url_for, session, request, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "Gobiksk@31012006and20060131"

def db_connection():
    return mysql.connector.connect(
        host="e1tbew.h.filess.io",
        user="Flight_Ticket_App_universeup",
        password="4fa3a72d1a689a79dfe9186e8d5685f86b1845a4",
        database="Flight_Ticket_App_universeup",
        port=3307,
        autocommit=True 
    )

@app.route('/')
def home():
    return render_template("dashboard.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        mydb = db_connection()
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM Users WHERE username=%s", (username,))
        result = cursor.fetchone()

        if result:
            flash("User Already Exists", "danger")
        else:
            cursor.execute("INSERT INTO Users(username,email,password) VALUES (%s,%s,%s)",
                           (username, email, password))
            mydb.commit()
            flash("Registered Successfully", "success")
            cursor.close()
            mydb.close()
            return redirect(url_for('login'))

        cursor.close()
        mydb.close()
    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        mydb = db_connection()
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM Users WHERE username=%s AND password=%s",
                       (username, password))
        result = cursor.fetchone()

        cursor.close()
        mydb.close()

        if result:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect Username Or Password", "danger")

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html")

@app.route('/Booking',methods=['GET','POSt'])
def Booking():
    if request.method=='POST':
        passenger_name=request.form['passenger_name']
        Age=request.form['Age']
        Gender=request.form['Gender']
        Airways=request.form['Airways']
        Flight_number=request.form['Flight_number']
        Departure=request.form['Departure']
        Destination=request.form['Destination']
        Departure_time=request.form['Departure_time']

        mydb=db_connection()
        cursor=mydb.cursor()
        cursor.execute("insert into Flight (passenger_name, Age, Gender, Airways, Flight_number, Departure, Destination, Departure_time) values (%s,%s,%s,%s,%s,%s,%s,%s)",(passenger_name,Age,Gender,Airways,Flight_number,Departure,Destination,Departure_time))
        cursor.close()
        mydb.close()
        flash("Ticket Booked Successfully","success")
    return render_template('Booking.html')

@app.route('/Update',methods=['GET','POST'])
def Update():
    if request.method=='POST':
        passenger_name=request.form['passenger_name']
        Age=request.form['Age']
        Gender=request.form['Gender']
        Airways=request.form['Airways']
        Flight_number=request.form['Flight_number']
        Departure=request.form['Departure']
        Destination=request.form['Destination']
        Departure_time=request.form['Departure_time']

        mydb=db_connection()
        cursor=mydb.cursor()
        cursor.execute("update Flight set Age=%s,Gender=%s,Airways=%s,Flight_number=%s,Departure=%s,Destination=%s,Departure_time=%s where passenger_name=%s",(Age,Gender,Airways,Flight_number,Departure,Destination,Departure_time,passenger_name))
        cursor.close()
        mydb.close()
        flash("Ticket Updated Successfully","success")
    return render_template('Update.html')

@app.route('/cancel_ticket',methods=['GET','POST'])
def cancel_ticket():
    if request.method=='POST':
        passenger_name=request.form['passenger_name']
        Flight_number=request.form['Flight_number']
        mydb=db_connection()
        cursor=mydb.cursor()
        cursor.execute("select * from Flight where passenger_name=%s and Flight_number=%s",(passenger_name,Flight_number))
        result=cursor.fetchone()
        if result:
            cursor.execute("delete from Flight where passenger_name=%s and Flight_number=%s",(passenger_name,Flight_number))
            flash("Ticket Cancelled Successfully","success")
            mydb.commit()
        else:
            flash("Invalid User","danger")
        cursor.close()
        mydb.close()
    return render_template("Cancel.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
