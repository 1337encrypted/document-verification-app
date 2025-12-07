import hashlib
import json
import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ledger_file = "ledger.json"

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            return hashlib.sha256(data).hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def add_certificate(filepath, name, issuer):
    try:
        cert_hash = get_hash(filepath)
        new_cert = {
            "hash": cert_hash,
            "name": name,
            "issuer": issuer,
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        }

        if os.path.exists(ledger_file):
            with open(ledger_file, "r") as f:
                ledger = json.load(f)
        else:
            ledger = []

        ledger.append(new_cert)

        with open(ledger_file, "w") as f:
            json.dump(ledger, f, indent=4)

        return True
    except json.JSONDecodeError:
        raise Exception("Ledger file is corrupted. Please check ledger.json")
    except Exception as e:
        raise Exception(f"Error adding certificate: {str(e)}")

def verify_certificate(filepath):
    try:
        cert_hash = get_hash(filepath)

        if os.path.exists(ledger_file):
            with open(ledger_file, "r") as f:
                ledger = json.load(f)
        else:
            return {"success": False, "message": "Ledger not found."}

        for cert in ledger:
            if cert["hash"] == cert_hash:
                return {
                    "success": True,
                    "message": f"✅ VERIFIED: Issued to {cert['name']} by {cert['issuer']} on {cert['date']}"
                }
        return {"success": False, "message": "❌ Certificate NOT FOUND — likely fake or unregistered."}
    except json.JSONDecodeError:
        return {"success": False, "message": "Error: Ledger file is corrupted."}
    except Exception as e:
        return {"success": False, "message": f"Error verifying certificate: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ledger')
def view_ledger():
    if os.path.exists(ledger_file):
        with open(ledger_file, "r") as f:
            try:
                ledger = json.load(f)
                return render_template('ledger.html', ledger=ledger)
            except json.JSONDecodeError:
                flash('Error reading ledger file', 'error')
                return redirect(url_for('index'))
    else:
        flash('No ledger found. Add certificates first.', 'error')
        return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    name = request.form.get('name', '').strip()
    issuer = request.form.get('issuer', '').strip()

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    if not name or not issuer:
        flash('Please fill in Name and Issuer fields', 'error')
        return redirect(url_for('index'))

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        add_certificate(filepath, name, issuer)
        flash('✅ Certificate added to blockchain successfully!', 'success')

        # Clean up uploaded file
        os.remove(filepath)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/verify', methods=['POST'])
def verify():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        result = verify_certificate(filepath)
        flash(result['message'], 'success' if result['success'] else 'error')

        # Clean up uploaded file
        os.remove(filepath)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('index'))

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    print("\n" + "="*50)
    print("Certificate Verification System Starting...")
    print("Opening browser at http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    app.run(debug=False, port=5000)
