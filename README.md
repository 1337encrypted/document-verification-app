# Certificate Verification System

A blockchain-based document authentication system using SHA-256 hashing.

## Requirements

- Python 3.9 or higher
- Flask (web framework)

## Installation

1. **Clone or download this project**

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # macOS/Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python3 app.py
```

The application will:
- Start a local web server
- Automatically open your browser to `http://127.0.0.1:5000`

**To stop the server:** Press `Ctrl+C` in the terminal

## How to Use

### Add a Certificate
1. Click "Choose File" in the **Add Certificate** section
2. Select any document (PDF, image, etc.)
3. Enter the certificate holder's **Name**
4. Enter the **Issuer** (who issued the certificate)
5. Click **Add Certificate**

The file's hash will be stored in the blockchain ledger.

### Verify a Certificate
1. Click "Choose File" in the **Verify Certificate** section
2. Select a document
3. Click **Verify Certificate**

If the document exists in the ledger, you'll see who it was issued to and when.

### Testing Tampering Detection
1. Add a certificate for any file
2. Open the file and make a small change
3. Save it and try to verify again
4. The verification will fail because the hash changed

## How It Works

- Each file is hashed using SHA-256
- The hash, along with certificate metadata, is stored in `ledger.json`
- Verification checks if a file's hash exists in the ledger
- Any modification to the file changes its hash, making tampering detectable

## Files

- `app.py` - Flask web application
- `templates/index.html` - Web interface
- `ledger.json` - Certificate storage (created automatically)
- `requirements.txt` - Python dependencies
