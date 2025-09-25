# qr-code-authentication-system
 QR Code-based authentication system for customer &amp; vehicle management developed during my internship at Abdul Latif Jameel (Connected Car Department).
[README.md](https://github.com/user-attachments/files/22532984/README.md)

# 🚗 QR Code Authentication System for Customer & Vehicle Management

> A Python-based web and WhatsApp-enabled system to authenticate customers and vehicles using QR codes, developed as an internship project for Abdul Latif Jameel Motors, Connected Car Department.

---

## 📋 Project Overview

This system validates QR codes against a customer & vehicle database and displays detailed information about the customer and their vehicles.  
It features:
- A **web interface** for uploading QR code images or PDFs.
- A **WhatsApp interface** for sending QR codes via WhatsApp Business.
- Automatic validation of QR code: valid / expired / invalid.
- Displays customer details, membership status, and vehicle data.

---

## 🎯 Features

✅ Generate realistic customer & vehicle database (with QR codes).  
✅ Validate uploaded or sent QR code against the database.  
✅ Web interface with light/dark mode and responsive design.  
✅ WhatsApp Business API integration for QR validation on mobile.  
✅ Handles complex 1-to-many customer-to-vehicle relationships.  
✅ Displays maintenance and predictive alert information.

---

## 📂 Project Structure

```
.
├── create_database.py        # Script to generate database & QR codes
├── customers_with_vehicles.xlsx  # Generated database (sample data)
├── QRCodeReader.py           # Reads & decodes QR codes from files
├── Validator.py              # Validates decoded QR against database
├── WebApp.py                 # Flask app with web & WhatsApp interfaces
├── templates/
│   └── index.html            # Web UI template
├── QRcodes/                  # Folder with generated QR code images
├── temp_uploaded_file/       # Temporary upload folder (runtime)
└── README.md                 # (you’re reading this)
```

---

## 🧪 Technologies Used

| Category            | Tools & Libraries                |
|---------------------|----------------------------------|
| Language            | Python 3.x                       |
| Backend Framework   | Flask                            |
| QR Code             | OpenCV, qrcode                   |
| Database            | Excel (via pandas & openpyxl)   |
| Frontend            | HTML, CSS, Jinja2               |
| WhatsApp API        | Meta WhatsApp Business API, ngrok |
| PDF Handling        | pdf2image                        |

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip
- WhatsApp Business API credentials
- `ngrok` account (for public webhook)

### Install dependencies
```bash
pip install -r requirements.txt
```

Sample `requirements.txt`:
```
flask
opencv-python
qrcode
pandas
openpyxl
pdf2image
requests
```

---

## 🔨 Usage

### 1️⃣ Generate Database
Run the following to generate 500 customer records, an Excel file, and QR code images:
```bash
python create_database.py
```

Output:
- `customers_with_vehicles.xlsx`
- `QRcodes/` folder with `.png` QR codes.

---

### 2️⃣ Run the Web App
Start the Flask app:
```bash
python WebApp.py
```
- Visit [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser.
- Upload a QR code image or PDF to validate.

---

### 3️⃣ WhatsApp Integration (optional)
- Configure your webhook URL with `ngrok`:
  ```bash
  ngrok http 8080
  ```
- Set the `ngrok` URL in WhatsApp Business dashboard as webhook.
- Send a QR code image to your WhatsApp Business number.
- The system replies with validation result & customer details.

---

## 🖥️ Interfaces

### 🌐 Web Interface
- File upload for `.png`, `.jpg`, `.jpeg`, `.pdf`.
- Displays:
  - Valid / Expired / Invalid status.
  - Customer name, ID, membership expiry.
  - Vehicle list & maintenance details.
- Light/Dark mode toggle.
- Mobile-friendly.

### 💬 WhatsApp Interface
- Sends reply directly to sender with validation result.
- Supports customers on the go.

---

## 📄 Sample Results

| Status   | Example |
|----------|---------|
| ✅ Valid | Shows customer & vehicle info |
| ⚠️ Expired | Membership expired |
| ❌ Invalid | Customer not found |

---

## 👨‍💻 Code Highlights

- `QRCodeReader.py` — Decodes QR from images or PDFs using OpenCV.
- `Validator.py` — Looks up customer in database & validates membership.
- `WebApp.py` — Connects everything: web upload + WhatsApp webhook.
- `index.html` — Responsive UI with Jinja2 templating.

---

## 📜 Acknowledgments

This project was developed as part of the internship at:
> Abdul Latif Jameel Motors — Connected Car Department  
> Mentor: Ahmed Trabelsi

---

## 📧 Contact

For questions or contributions:
- Mentor: Ahmed Trabelsi [trabelsia@alj.com](mailto:trabelsia@alj.com)
- Intern: Zeyad Alghamdi [ziadmsfer1424@gmail.com](ziadmsfer1424@gmail.com)
