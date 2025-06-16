from flask import Flask, render_template, request,session, redirect
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from random import randint
import sqlite3 

app = Flask(__name__)
app.secret_key = 'your-secret-key'
# --- Flask-Mail Config ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'zahmouldhia@gmail.com'
app.config['MAIL_PASSWORD'] = 'boye tbbt sdra bsod'  # Replace with a safe app password!
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['DATABASE']="database.sqlite"




def get_db_connection():
    conn = sqlite3.connect('database.sqlite')  # Path to your DB file
    conn.row_factory = sqlite3.Row  # Optional: to get rows as dict-like objects
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

def add_user_to_db():
    
    conn= get_db_connection()
    cursor=conn.cursor()
    cursor.execute('''
        INSERT INTO users (name,lname,email,password,gender)
        VALUES(?,?,?,?,?)
''',(request.form.get('name'),request.form.get('lname'),request.form.get('email'),request.form.get('password'),request.form.get('gender')))
    conn.commit()
    conn.close()

    msg = Message(
                subject="Account created",
                sender=app.config['MAIL_USERNAME'],
                recipients=[request.form.get("email")]
            )
    msg.body = """\
        Welcome to OmBurger!

        Your account has been successfully created. We’re excited to have you with us!

        If you have any questions or need help, feel free to reach out.

        Enjoy your journey with OmBurger!
    """
    mail.send(msg)



def add_order_to_db():
    conn=get_db_connection()
    cursor=conn.cursor()
    payment_method = request.form.get('payment_method')
    email = request.form.get('email')
    cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
    user_id=cursor.fetchone()
    user_id = user_id['user_id'] 

    order = {
            "Inta omri": request.form.get('Inta_omri_qty'),
            "Sirit lhob": request.form.get('Sirit_Lhob_qty'),
            "Alf lila w lila": request.form.get('Alf_lila_qty'),
            "Mama zamanha gaya": request.form.get('Mama_qty')
        }

        
    order = {k: int(v) for k, v in order.items() if v and int(v) > 0}
    order=str(order)

    order_time = datetime.now()
    order_number = f"{randint(0, 9999):04d}"
    cursor.execute('''
        INSERT INTO orders(payment_method,order_details,order_time,user_id)
                   values(?,?,?,?)
''',(str(payment_method),str(order),str(order_time),user_id))
    conn.commit()
    conn.close()



def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            gender TEXT NOT NULL
        )
    ''')

    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_method TEXT NOT NULL,
            order_details TEXT NOT NULL,
            order_time TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


mail = Mail(app)





# --- Home Route: Handles Contact Form (form1) ---
@app.route('/', methods=['GET', 'POST'])
def home():
    
    if 'user_id' not in session:
        return redirect('/login')
    

    if request.method == 'POST':
        formID = request.form.get('form_id')
        if formID == 'form1':
            name = request.form.get('name')
            lname = request.form.get('lname')
            gender = request.form.get('gender')
            email = request.form.get('email')
            message = request.form.get('message')
            


            # Send confirmation email
            msg = Message(
                subject="New Feedback Received",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.body = f"""
            Hello {name} {lname},

            Thank you for your message!

            Gender: {gender}
            Email: {email}
            Message: {message}
            """
            mail.send(msg)
            return render_template("thanks.html", user_name=name)

    return render_template("resto.html",user_name=name,user_email=email,gender=gender,last_name=lname)




# --- Order Route: Handles Order Form (form2) ---
@app.route('/order', methods=['POST'])
def order():
    formID = request.form.get('form_id')
    if formID == 'form2':
        name = request.form.get('name')
        lname = request.form.get('lname')
        payment_method = request.form.get('payment_method')
        email = request.form.get('email')

        order = {
            "Inta omri": request.form.get('Inta_omri_qty'),
            "Sirit lhob": request.form.get('Sirit_Lhob_qty'),
            "Alf lila w lila": request.form.get('Alf_lila_qty'),
            "Mama zamanha gaya": request.form.get('Mama_qty')
        }

        # Clean up empty/zero values and convert to int
        order = {k: int(v) for k, v in order.items() if v and int(v) > 0}

        order_time = datetime.now()
        order_arrival = order_time + timedelta(minutes=30)
        order_number = f"{randint(0, 9999):04d}"  # e.g. '0034'
        msg = Message(
                subject="Order Confirmation",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )
        msg.body = f'''
            Hello {name} {lname},

            Thank you for placing your order with Om Burger!

            We have received your order and it's being prepared with care. Here are the details:

            - Payment Method: {payment_method}
            - Email: {email}

            Your order summary:
            '''
        for item, qty in order.items():
            msg.body += f"- {item.replace('_', ' ').title()}: {qty}\n \t"

        msg.body += f'''

            Your order was placed at {order_time.strftime('%H:%M:%S')} and should arrive by {order_arrival.strftime('%H:%M:%S')}.

            If you have any questions or would like to modify your order, please contact us through the support section on our website.

            Bon appétit!

            – The Om Burger Team
        '''
        mail.send(msg)
        add_order_to_db()



        return render_template(
            "order.html",
            user_name=name,
            last_name=lname,
            email=email,
            payment_method=payment_method,
            order_number=order_number,
            order_details=order,
            time_ordered=order_time.strftime("%H:%M"),
            time=order_arrival.strftime("%H:%M")
        )
    else:
        return "Invalid form submission", 400
    


#------login page------
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method== 'GET':
        return render_template('login.html')
    else:
        user_name= request.form.get('username')
        password=request.form.get('password')
        conn=get_db_connection()
        cursor= conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (user_name,))
        row= cursor.fetchone()
        conn.close()
        if row and row["password"]==password:
            session['user_id'] = row['user_id']
            conn=get_db_connection()
            cursor=conn.cursor()
            cursor.execute('''
                           SELECT email FROM USERS WHERE user_id = ? ''',(session['user_id'],))
            

            email=cursor.fetchone()
            email=email['email']
            cursor.execute('SELECT name, lname, email, gender FROM users WHERE user_id = ?', (session['user_id'],))
            user_row = cursor.fetchone()
            name = user_row['name']
            lname = user_row['lname']
            email = user_row['email']
            gender = user_row['gender']
            return render_template("resto.html",user_name=name,user_email=email,gender=gender,last_name=lname)
        else:
            return '''Password incorrect.Try again'''


 #-------signup page--------   
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        add_user_to_db()
        return redirect('/login')  # or render_template('login.html')
    else:
        return render_template('signup.html')  # show sign-up form


@app.route('/porders')
def porders():
    conn=get_db_connection()
    cursor=conn.cursor()
    user_id=session['user_id']
    cursor.execute('''
    SELECT * FROM orders WHERE user_id = ?
''',(user_id,))
    orders=cursor.fetchall()
    conn.close()
    return render_template('porders.html',orders=orders)



    
# --- Run the app ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
