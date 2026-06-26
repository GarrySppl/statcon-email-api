@app.route("/send-enquiry", methods=["POST"])
def send_enquiry():
    data = request.json or {}
    print("REQUEST DATA:", data)

    sender_email = os.environ.get("SMTP_EMAIL")
    sender_password = os.environ.get("SMTP_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")

    print("SMTP_EMAIL:", sender_email)
    print("SMTP_PASSWORD exists:", bool(sender_password))
    print("RECEIVER_EMAIL:", receiver_email)

    if not sender_email or not sender_password or not receiver_email:
        return jsonify({
            "success": False,
            "error": "Missing environment variables. Check SMTP_EMAIL, SMTP_PASSWORD, RECEIVER_EMAIL"
        }), 500

    customer_name = data.get("customer_name", "Not provided")
    phone_number = data.get("phone_number", "Not provided")
    email = data.get("email", "Not provided")
    city = data.get("city", "Not provided")
    enquiry_type = data.get("enquiry_type", "General")
    product = data.get("product", "Not provided")
    requirement = data.get("requirement", "Not provided")
    issue = data.get("issue", "Not provided")

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
        print("Connecting to Office365 SMTP...")

        with smtplib.SMTP("smtp.office365.com", 587, timeout=20) as server:
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()

            print("Logging in...")
            server.login(sender_email, sender_password)

            print("Sending email...")
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Email sent successfully")

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
    
