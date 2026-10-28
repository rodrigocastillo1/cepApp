# cepApp
An AI-powered web app for exploring electronics product passports, evaluating circularity, and understanding sustainability through data, analytics, and AI.

## How to run the app locally

1. Open a terminal in the project folder.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root and set a secret key:
   ```text
   SECRET_KEY=your-generated-secret-key
   ```
   Keep this file local; it is ignored by Git. You can generate a key running the following command:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
5. Start the Flask app:
   ```bash
   python -m app.app
   ```
5. Open the app in your browser:
   ```text
   http://127.0.0.1:5000
   ```

