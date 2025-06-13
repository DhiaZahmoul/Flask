from flask import Flask, render_template, request
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from random import randint

app = Flask(__name__)

# --- Flask-Mail Config ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'zahmouldhia@gmail.com'
app.config['MAIL_PASSWORD'] = 'boye tbbt sdra bsod'  # Replace with a safe app password!
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# --- Home Route: Handles Contact Form (form1) ---
@app.route('/', methods=['GET', 'POST'])
def home():
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

    return render_template("resto.html")


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


# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)
