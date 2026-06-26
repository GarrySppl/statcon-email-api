from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return "Statcon Email API is running."


@app.route("/send-enquiry", methods=["POST"])
def send_enquiry():
    data = request.get_json(silent=True) or {}

    customer_name = data.get("customer_name", "Not provided")
    phone_number = data.get("phone_number", "Not provided")
    email = data.get("email", "Not provided")
    city = data.get("city", "Not provided")
    enquiry_type = data.get("enquiry_type", "General")
    product = data.get("product", "Not provided")
    requirement = data.get("requirement", "Not provided")
    issue = data.get("issue", "Not provided")

    sender_email = os.environ.get("SMTP_EMAIL")
    sender_password = os.environ.get("SMTP_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")

    print("SMTP_EMAIL:", sender_email)
    print("SMTP_PASSWORD exists:", bool(sender_password))
    print("RECEIVER_EMAIL:", receiver_email)

    if not sender_email or not sender_password or not receiver_email:
        return jsonify({
            "success": False,
            "error": "Missing environment variables. Please set SMTP_EMAIL, SMTP_PASSWORD, and RECEIVER_EMAIL in Render."
        }), 500

    subject = f"New {enquiry_type} Enquiry from ElevenLabs AI"

    body = f"""
New enquiry received from ElevenLabs AI Agent.

Customer Name: {customer_name}
Phone Number: {phone_number}
Customer Email: {email}
City: {city}

Enquiry Type: {enquiry_type}
Product: {product}
Requirement: {requirement}
Issue: {issue}

Please follow up with the customer.
"""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        print("Connecting to Microsoft SMTP...")

        with smtplib.SMTP("smtp.office365.com", 587, timeout=100) as server:
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()

            print("Logging in...")
            server.login(sender_email, sender_password)

            print("Sending email...")
            server.sendmail(sender_email, receiver_email, message.as_string())

        return jsonify({
            "success": True,
            "message": "Email sent successfully"
        }), 200

    except Exception as e:
        print("SMTP ERROR:", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
