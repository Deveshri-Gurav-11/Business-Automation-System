from flask import Flask, render_template, request, redirect
import os
import psycopg2
import pandas as pd


app = Flask(__name__)

# ================= CONFIG =================
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ================= DATABASE =================
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

# ================= CSV REPORT =================
def generate_csv():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM enquiries", conn)
    df.to_csv("enquiries_report.csv", index=False)
    conn.close()

# ================= ROUTES =================

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


# ================= CONTACT FORM =================
from email_sender import send_email

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        company = request.form['company']
        enquiry_type = request.form['enquiry_type']
        message = request.form['message']

        print("USER EMAIL:", email)

        import logging
        logging.info(f"New enquiry from {os.name}") 


        # ================= EMAIL TO USER =================
        send_email(
    receiver_email=email,   # ✅ USER EMAIL
    subject="Thank you for contacting us",
    body=f"""Hello {name},

Thank you for contacting us.

We have received your enquiry regarding "{enquiry_type}" and will get back to you shortly.


"""
)

        # ================= EMAIL TO ADMIN =================
        send_email(
    receiver_email=os.getenv("ADMIN_EMAIL"),   # ✅ YOUR EMAIL
    subject="New Enquiry Received",
    body=f"""New enquiry received:

Name: {name}
Phone: {phone}
Email: {email}
Company: {company}
Enquiry Type: {enquiry_type}

Message:
{message}
"""
)

        return render_template('contact.html', success=True)

    return render_template('contact.html')


# ================= DELETE =================
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enquiries WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')


# ================= ADMIN =================
@app.route('/admin')
def admin():
    search = request.args.get('search')

    conn = get_db_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute("SELECT * FROM enquiries WHERE name ILIKE %s", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM enquiries ORDER BY id DESC")

    data = cursor.fetchall()
    conn.close()

    return render_template('admin.html', data=data)


# ================= MAIN =================
if __name__ == '__main__':
    app.run(debug=False)