import os
import requests
from flask import Flask, request, render_template
from QRCodeReader import QRCodeReader
from Validator import Validator

app = Flask(__name__)

# Your WhatsApp config
VERIFY_TOKEN = "my_verify_token"
ACCESS_TOKEN = "EAAR9abQEip0BPO622DbDDHlJOEGxpVzZCdg7reHWHB9qwTaialtZAQHjxYLDoeDdLMnoZAnVLjPhs9vzEdwbdjsJrh1T4bRB2ZCVZCZBgd2l3hfYxSpRD3kFPfQHIt10ZC9yQq4TECUdcXk3e1aJQgz9H1jCGYbXu6glhAgi1iuZBV8oCeV3ebTH3vw1tKiRkQkWPL5dPG80ret55JmIT4mporvn08egWJccB4VtZBmsDFxMZD"
PHONE_NUMBER_ID = "699992206533063"

reader = QRCodeReader()
validator = Validator()

UPLOAD_FOLDER = "temp_uploaded_file"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        result = None
        file = request.files['file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Decode QR
            qr_data = reader.smart_decode(filepath)
            if qr_data:
                result = validator.validate(qr_data)
            else:
                result = "Invalid or unreadable QR code"

            os.remove(filepath)
        return render_template('index.html', result=result)
    
    # For GET requests, don't pass any result
    return render_template('index.html')


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified!")
            return challenge, 200
        else:
            return "❌ Verification failed", 403

    if request.method == "POST":
        data = request.get_json()
        print("📩 Incoming webhook:", data)

        try:
            entry = data.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])

            if not messages:
                return "OK", 200

            message = messages[0]
            from_number = message["from"]
            msg_type = message["type"]

            if msg_type == "image":
                media_id = message["image"]["id"]
                print(f"📷 Image media_id: {media_id}")

                # Step 1: Get media URL
                media_url = get_media_url(media_id)
                if not media_url:
                    send_whatsapp_message(from_number, "❌ Failed to get image URL.")
                    return "OK", 200

                # Step 2: Download the image
                image_path = os.path.join(UPLOAD_FOLDER, f"{media_id}.jpg")
                download_image(media_url, image_path)

                # Step 3: Decode & Validate
                qr_data = reader.smart_decode(image_path)
                os.remove(image_path)

                if not qr_data:
                    send_whatsapp_message(from_number, "❌ Invalid or unreadable QR code.")
                    return "OK", 200

                result = validator.validate(qr_data)

                # Step 4: Format result
                if "error" in result:
                    reply = f"⚠️ {result['error']}"
                else:
                    customer = result["data"][0]  # first record contains customer info
                    reply = "✅ QR Code is valid!\n\n"
                    reply += f"👤 Customer: {customer.get('first_name', '')} {customer.get('last_name', '')}\n"
                    reply += f"🆔 ID: {customer.get('customer_id', '')}\n"
                    reply += f"📅 Membership Expiration: {customer.get('expiration_date', '')}\n"
                    reply += f"🚗 Total Vehicles: {customer.get('number of cars', len(result['data']))}\n\n"

                    # Now list vehicles
                    for idx, car in enumerate(result["data"], 1):
                        reply += f"🚙 Vehicle #{idx}\n"
                        reply += f"   Make & Model: {car.get('car_make', '')} {car.get('car_model', '')}\n"
                        reply += f"   VIN: {car.get('car_vin', '')}\n"
                        reply += f"   Status: {car.get('status', '')}\n"
                        reply += f"   Last Service: {car.get('last_maintenance_date', '')}\n"
                        reply += f"   Next Due: {car.get('next_maintenance_due', '')}\n"

                        if car.get('predictive_maintenance_alert') == 'True':
                            reply += f"   🚨 Predictive Alert: Remaining Life: {car.get('remaining_useful_life', '')}\n"

                        reply += "\n"

                send_whatsapp_message(from_number, reply)

            else:
                print(f"📄 Received message type: {msg_type}")
                send_whatsapp_message(from_number, "📷 Please send a QR code image.")

        except Exception as e:
            print("❌ Error:", e)

        return "OK", 200


def get_media_url(media_id):
    url = f"https://graph.facebook.com/v18.0/{media_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"fields": "url"}

    r = requests.get(url, headers=headers, params=params)
    if r.ok:
        return r.json().get("url")
    print("❌ Failed to get media URL:", r.text)
    return None


def download_image(url, filepath):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    r = requests.get(url, headers=headers)
    with open(filepath, "wb") as f:
        f.write(r.content)
    print(f"✅ Image downloaded: {filepath}")


def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    r = requests.post(url, headers=headers, json=data)
    if r.ok:
        print("✅ Reply sent!")
    else:
        print("❌ Failed to send message:", r.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
