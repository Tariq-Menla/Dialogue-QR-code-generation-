import sqlite3 # Database
from flask import Flask, render_template, request
import qrcode
import uuid # Needed to generate tokens
import io # handle image data

app = Flask(__name__)
connection = sqlite3.connect('./instance/qr.db')
cursor = connection.cursor()


# This code forms the 100 qr_codes with links that "work"
# db_connection = sqlite3.connect('./instance/qr.db')
    
# cursor.execute("SELECT qr_code FROM qr_codes WHERE is_used = 0")
def create_url_pngs():
    tokens = cursor.fetchall()
    for row in tokens:
        token = row[0]
        url = f'http://127.0.0.1:5000/form/{token}'
        #c reate url img
        img = qrcode.make(url)
        img.save(f"qr_{token}.png")
    connection.close()


def create_url_png():
    token = cursor.fetchone()
    qr_token = token[0]
    url = f'http://127.0.0.1:5000/form/{qr_token}'
    #create url img
    img = qrcode.make(url)
    img.save(f"qr_{token}.png")
    connection.close()

# THE FUNCTION GENERATE LINKS IN ORDER TO USE FOR 
def generate_link():
    host_ip = "192.168.2.27"
    for i in range(100):
        token = str(uuid.uuid4())
        basic_url = f"http://{host_ip}:5000/onboard/{token}"
        cursor.execute("INSERT INTO qr_codes(qr_code, is_used) VALUES (?, ?)", (token, False))



# cursor.execute("CREATE TABLE qr_codes ( qr_code TEXT, is_used BOOL)")
# generate_link()
# connection.commit()


# host_ip = "192.168.2.27"
# base_url = f"http://{host_ip}:5000/onboard/{token}"
# img = qrcode.make(base_url)
# type(img)  # qrcode.image.pil.PilImage
# img.save("invite_qr.png")

@app.route('/form/<token>', methods=['GET', 'POST'])
def Home(token):
    # 1. Connect to the DB
    conn = sqlite3.connect('hackathon.db')
    cursor = conn.cursor()

    # 2. Get the data (using your current logic of fetching any unused code)
    cursor.execute("SELECT qr_code FROM qr_codes WHERE is_used = 0 LIMIT 1")
    row = cursor.fetchone()
    
    # Close connection immediately to avoid "Database is locked" errors
    conn.close()

    # 3. Handle the case where no codes are left
    qr_data = row[0] if row else "No codes available"
    url = f'http://127.0.0.1:5000/form/{qr_data}'
    #c reate url img
    img = qrcode.make(url)
    img.save(f"qr_{token}.png")
    # 4. Pass 'qr_data' to your HTML
    return render_template("index.html", qr_code=qr_data, token=token)



    
    # if result is None:
    #     # Scenario A: The token doesn't exist at all
    #     return "<h1>Invalid Code</h1>" 
    
    # elif result[0]: 
    #     # Scenario B: The token exists, but is_used is True (1)
    #     # (result[0] accesses the first column, which is 'is_used')
    #     return render_template("invalid.html")
        
    # else:
    #     # Scenario C: Token exists and is_used is False (0)
    #     return render_template("index.html")
    
# base_url= http://192.168.2.27:5000/form
