from flask import Flask, request
import smtplib, os
from email.message import EmailMessage

app = Flask(__name__)

# معلومات المنتجات المخزنة
PRODUCTS = {
    "op": {"name": "tawakal", "price": "1.00", "file": "products/hhhhhh.pdf"},
    "PROD002": {"name": "Product 2", "price": "10.00", "file": "products/product2.zip"},
}

# بريدك Gmail (يجب تفعيل كلمة مرور التطبيقات)
EMAIL_ADDRESS = "farik7sa7402@gmail.com"
EMAIL_PASSWORD = "ebyt bmjh qdcn sduy"

@app.route('/', methods=['GET'])
def home():
    return "IPN Listener يعمل إن شاء الله تعالى"

@app.route('/ipn', methods=['POST'])
def ipn():
    # استلام بيانات IPN
    data = request.form
    payer_email = data.get("payer_email")
    item_number = data.get("item_number")
    payment_status = data.get("payment_status")
    mc_gross = data.get("mc_gross")

    if payment_status != "Completed":
        return "الدفع لم يكتمل", 400

    product = PRODUCTS.get(item_number)

    if not product or product["price"] != mc_gross:
        return "بيانات المنتج غير متطابقة", 400

    # تجهيز الرسالة
    msg = EmailMessage()
    msg["Subject"] = "شكرا على الشراء"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = payer_email
    msg.set_content(f"شكرا على شراء {product['name']}. تجد المنتج مرفقاً في هذه الرسالة إن شاء الله تعالى.")

    # إرفاق المنتج
    filepath = product["file"]
    with open(filepath, "rb") as f:
        file_data = f.read()
        filename = os.path.basename(filepath)
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=filename)

    # إرسال البريد
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    return "تم التوصيل", 200
