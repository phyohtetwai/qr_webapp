# 📄 QR PDF Generator Web App

A simple and elegant **Flask-based web application** that allows users to upload a `.txt` or `.csv` file and automatically generate a **PDF file containing QR codes** for each entry.

---

## 🚀 Features

- 🖱️ Upload `.txt` or `.csv` files easily  
- 🔲 Automatically generate QR codes for each line or entry  
- 📄 Download generated QR code PDF instantly  
- 💎 Beautiful and responsive web UI (built with Tailwind CSS)  
- ⚙️ Lightweight and easy to deploy on **AWS EC2**, **VPS**, or **local servers**

---

## 🧰 Tech Stack

| Component | Description |
|------------|--------------|
| **Frontend** | HTML5, Tailwind CSS |
| **Backend** | Python Flask |
| **QR Generation** | `qrcode` (Python library) |
| **PDF Creation** | `reportlab` (Python library) |

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/phyohtetwai/qr_webapp.git
cd qr_webapp
```

### 2️⃣ Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### ▶️ Run the Application
```bash
python app.py
```

By default, Flask runs on http://127.0.0.1:7777
