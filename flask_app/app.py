from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
from database import save_message, init_db, get_messages, delete_message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("fenomeno")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('frasermclauchlan18@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('axzg btvs nhkp cgyr')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('frasermclauchlan18@gmail.com')

mail = Mail(app)

ADMIN_USERNAME = os.getenv("admin")
ADMIN_PASSWORD_HASH = os.getenv("scrypt:32768:8:1$RiNQTOT4obUeIhov$cf4f1b011853dee986d44fa7ec898ce901a243aac3920d881e6745ee438f1b8563377beffc00c12cb4561135dd1194bb080b0ad357d5ea09ce561563039d353b")


init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        save_message(name, email, message)

        msg = Message("New Contact Form Submission", recipients=["frasermmclauchlan18@gmail.com"])
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        mail.send(msg)

        confirmation = Message(
            subject="Thanks for contacting us!",
            recipients=[email],
        )
        confirmation.body = f"""
Hi {name},

Thanks for reaching out! We've received your message and will reply soon.

📨 Your Message:
{message}

Best regards,
Your Website Team
"""
        mail.send(confirmation)

        return render_template('contact.html', success=True, name=name)

    return render_template('contact.html', success=False)


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["admin"] = True
            return redirect(url_for("admin_panel"))

        return render_template("admin_login.html", error=True)

    return render_template("admin_login.html", error=False)

@app.route('/admin/panel')
def admin_panel():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    messages = get_messages()
    return render_template("admin_panel.html", messages=messages)

@app.route('/admin/delete/<int:message_id>')
def delete(message_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    delete_message(message_id)
    return redirect(url_for("admin_panel"))

@app.route('/admin/logout')
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


@app.route('/adocado')
def ado():
    return render_template('ado.html')

@app.route('/uma')
def uma():
    return render_template('umamusume.html')

@app.route('/strive')
def strive():
    return render_template('strive.html')


if __name__ == '__main__':
    app.run(debug=True)