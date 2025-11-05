from flask import Flask, render_template, redirect, url_for, session, request, flash
import mysql.connector
import os
app = Flask(__name__)
app.secret_key = "Gobiksk@31012006and20060131"

def db_connection():
    return mysql.connector.connect(
        host="e1tbew.h.filess.io",
        user="Flight_Ticket_App_universeup",
        password="4fa3a72d1a689a79dfe9186e8d5685f86b1845a4",
        database="Flight_Ticket_App_universeup",
        port=3307,
        autocommit=True)

@app.route('/')
def home():
    return render_template("login.html")

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
            return redirect(url_for('dashboard'))

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
        cursor.execute("SELECT * FROM Users WHERE username=%s AND password=%s",(username, password))
        result = cursor.fetchone()
        cursor.close()
        mydb.close()
        if result:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect Username Or Password", "danger")
    return render_template("login.html")

@app.route('/forget_password',methods=['GET','POST'])
def forget_password():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        con_password=request.form.get('con_password')
        mydb=db_connection()
        cursor=mydb.cursor()
        cursor.execute("select * from Users where email=%s",(email,))
        result=cursor.fetchone()
        if result:
            if password==con_password:
                cursor.execute("update Users set password=%s where email=%s",(password,email))
                mydb.commit()
                mydb.close()
                flash("Password Updated Successfully","success")
                return redirect(url_for('login'))
            else:
                flash("Mismatching Password","danger")
        else:
            flash("Incorrect Email","danger")
    return render_template("Forgrt_password.html")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html")

@app.route('/flight_search',methods=['GET','POST'])
def flight_search():
    return render_template('Flight_search.html')

@app.route('/flight_results',methods=['GET','POST'])
def flight_results():
    flights=None
    if request.method=='POST':
        Departure=request.form['Departure']
        Destination=request.form['Destination']
        mydb=db_connection()
        cursor=mydb.cursor(dictionary=True)
        cursor.execute("select Airways, Flight_number, Departure, Destination, Departure_time, Price from Flight_Details where Departure=%s and Destination=%s",(Departure,Destination))
        flights=cursor.fetchall()
        cursor.close()
        mydb.close()
    return render_template('Flight_result.html',flights=flights)

@app.route('/Booking',methods=['GET','POSt'])
def Booking():
    if request.method=='POST':
        passenger_name=request.form['passenger_name']
        Age=request.form['Age']
        Gender=request.form['Gender']
        Airways = request.args.get('Airways')
        Flight_number = request.args.get('Flight_number')
        Departure = request.args.get('Departure')
        Destination = request.args.get('Destination')
        Departure_time = request.args.get('Departure_time')
        Price = request.args.get('Price')
        Date=request.form['Date']

        mydb=db_connection()
        cursor=mydb.cursor(dictionary=True)
        cursor.execute("select * from Flight_Details where Flight_number=%s",(Flight_number,))
        flight=cursor.fetchone()
        if flight:
            cursor.execute("insert into Flight (passenger_name, Age, Gender, Airways, Flight_number, Departure, Destination, Departure_time, Price, Date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(passenger_name,Age,Gender,Airways,Flight_number,Departure,Destination,Departure_time,Price,Date))
            cursor.close()
            mydb.close()
            return redirect(url_for('Ticket_generate', Flight_number=Flight_number))
            #flash("Ticket Booked Successfully","success")
    return render_template('Booking.html')

@app.route('/Ticket_generate',methods=['GET'])
def Ticket_generate():
        Flight_number=request.args.get('Flight_number')
        mydb=db_connection()
        cursor=mydb.cursor(dictionary=True)
        cursor.execute("select * from Flight where Flight_number=%s ORDER BY Passenger_id DESC LIMIT 1",(Flight_number,))
        flights=cursor.fetchone()
        if not flights:
            return "No ticket found for this Flight Number!"
        cursor.close()
        mydb.close()
        return render_template("Ticket_generate.html",flights=flights)

@app.route('/flight_search1',methods=['GET','POST'])
def flight_search1():
    return render_template('Flight_search1.html')


@app.route('/show_flights',methods=['GET','POST'])
def show_flights():
    if request.method=='POST':
        passenger_name=request.form.get('passenger_name')
        mydb=db_connection()
        cursor=mydb.cursor(dictionary=True)
        cursor.execute("select * from Flight where passenger_name=%s",(passenger_name,))
        result=cursor.fetchall()
        cursor.close()
        mydb.close()
        return render_template('show_flights.html',result=result)

@app.route('/Update',methods=['GET','POST'])
def Update():
    if request.method=='POST':
        passenger_name=request.form['passenger_name']
        Age=request.form['Age']
        Gender=request.form['Gender']
        Passenger_id=request.args.get('Passenger_id')

        mydb=db_connection()
        cursor=mydb.cursor()
        cursor.execute("update Flight set passenger_name=%s, Age=%s,Gender=%s where Passenger_id=%s",(passenger_name,Age,Gender,Passenger_id))
        cursor.close()
        mydb.close()
        flash("Ticket Updated Successfully","success")
    return render_template('Update.html')

@app.route('/cancel_ticket',methods=['GET','POST'])
def cancel_ticket():
    if request.method=='POST':
        passenger_name=request.form['passenger_name']
        Passenger_id=request.form.get('Passenger_id')
        mydb=db_connection()
        cursor=mydb.cursor()
        cursor.execute("select * from Flight where passenger_id=%s" ,(Passenger_id,))
        result=cursor.fetchone()
        if result:
            cursor.execute("delete from Flight where passenger_id=%s ",(Passenger_id,))
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
    port = int(os.environ.get("PORT", 5000))   # Render gives PORT dynamically
    app.run(host="0.0.0.0", port=port)
