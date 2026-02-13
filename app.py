import sqlite3 # Database
from flask import Flask, render_template, request, redirect
import qrcode
import uuid # Needed to generate tokens
import io # handle image data

app = Flask(__name__)
# connection = sqlite3.connect('./instance/qr.db')
# cursor = connection.cursor()


# This code forms the 100 qr_codes with links that "work"
# db_connection = sqlite3.connect('./instance/qr.db')
    
# cursor.execute("SELECT qr_code FROM qr_codes WHERE is_used = 0")

print("All tokens reset to fresh. Try scanning now!")
def create_url_pngs():
    connection = sqlite3.connect('./instance/qr.db')
    cursor = connection.cursor()
    cursor.execute("SELECT qr_code FROM qr_codes")
    tokens = cursor.fetchall()
    for row in tokens:
        token = row[0]
        url = f'http://192.168.2.25:5000/form/{token}'
        #c reate url img
        img = qrcode.make(url)
        img.save(f"qr_{token}.png")
    connection.close()


def create_url_png():
    connection = sqlite3.connect('./instance/qr.db')
    cursor = connection.cursor()
    cursor.execute("SELECT qr_code FROM qr_codes LIMIT 1")
    token = cursor.fetchone()[0]
    url = f'http://192.168.2.25:5000/form/{token}'
    #create url img
    img = qrcode.make(url)
    img.save(f"qr_{token}.png")
    connection.close()

# create_url_pngs()

# THE FUNCTION GENERATE LINKS IN ORDER TO USE FOR 
def generate_link():
    connection = sqlite3.connect('./instance/qr.db')
    cursor = connection.cursor()
    host_ip = "192.168.2.25"
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
    connection = sqlite3.connect('./instance/qr.db')
    cursor = connection.cursor()
    
    # check if the token exists and check its status
    cursor.execute("SELECT is_used FROM qr_codes WHERE qr_code = ?", (token,))
    row = cursor.fetchone()
    if row is None or row[0] == 1:
        connection.close()
        return render_template("failure.html")
    if row[0] == 0:
        connection.close()
        return render_template("index.html", token=token)
    if request.method == 'POST':
        # ONLY burn the token now that they've finished
        return redirect('/submission')
    connection.close()
    return render_template("failure.html")
@app.route('/submission', methods=['POST'])
def submission():
#     cursor.execute("UPDATE qr_codes SET is_used = 1 WHERE qr_code = ?", (token,))
#     connection.commit()
    token = request.form.get('token') # Get the token from the hidden field
    
    connection = sqlite3.connect('./instance/qr.db')
    cursor = connection.cursor()
    
    if token:
        cursor.execute("UPDATE qr_codes SET is_used = 1 WHERE qr_code = ?", (token,))
        connection.commit()
    return render_template('success.html')

     
# base_url= http://192.168.2.27:5000/form

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)