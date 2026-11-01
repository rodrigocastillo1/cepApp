# cepApp
An AI-powered web app for exploring electronics product passports, evaluating circularity, and understanding sustainability through data, analytics, and AI.

## How to run the app locally

For an explanation of the current indicator normalization rules, score
calculation, and coverage, see
[Circularity Score Calculation](./CIRCULARITY_METHODOLOGY.md).

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
6. Open the app in your browser:
   ```text
   http://127.0.0.1:5000
   ```

### Generate demo QR codes

From the project root, run:
```bash
python -m tools.generate_demo_qr_codes
```

The utility saves one SVG per demo product to `data/demo_qr_codes/`. Choose a
different output directory with:
```bash
python -m tools.generate_demo_qr_codes --output-dir path\to\qr-codes
```
