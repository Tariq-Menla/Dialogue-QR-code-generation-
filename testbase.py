import sqlite3 # Database
# from flask import Flask, render_template, request
# import qrcode
import uuid # Needed to generate tokens





host_ip = "ipv4"
base_url = f"http://{host_ip}:5000/onboard/{token}"
img = qrcode.make(base_url)
# type(img)  # qrcode.image.pil.PilImage
# img.save("invite_qr.png")


# USE THIS TO GET TOKENS FROM DB
# cursor.execute("SELECT qr_code FROM qr_codes")

# rows = cursor.fetchall()
# for row in rows:
#     print(row[0])
    
# connection.close()
