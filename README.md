# cepApp
Capstone Project for the Compact Programming Course in Python. This is an AI-powered web app for exploring electronics product passports, evaluating circularity, and understanding sustainability through data, analytics, and AI.

Prof. Dr. Galyna Tabunshchyk

Group 11.
Topic: AI-Powered Circular Economy Product Passport

| Student                    | Matriculation number | Subsystem                                                        |
| -------------------------- | -------------------- | ---------------------------------------------------------------- |
| Rodrigo Castillo Alcantara | ESE - 7226791        | - Analytics Subsystem<br>- AI provider Subsystem               |
| Elnur Allazov              | ESE - 7226316        | - Product Data Subsystem<br>- Circularity Assessment Subsystem |

# [Homeworkassignment004] Exception Handling and Unit tests

For more information watch the presentation video: [HomeAssignment4-CPC(GROUP 11)](https://youtu.be/cI1xLXaSG6g?si=xnD2oO0cj91rpWuY)

Coverage results below were obtained by running:

```bash
python -m pytest tests --cov=modules --cov-report=term-missing
```

All subsystems included in this coverage report are located in the `modules/` folder.

| Module | Statements | Miss | Coverage |
| --- | ---: | ---: | ---: |
| `ai/gemini_provider.py` | 31 | 10 | 68% |
| `ai/openai_provider.py` | 31 | 10 | 68% |
| `ai/provider.py` | 8 | 0 | 100% |
| `analytics/errors.py` | 2 | 0 | 100% |
| `analytics/service.py` | 61 | 6 | 90% |
| `circularity/errors.py` | 3 | 0 | 100% |
| `circularity/methodology.py` | 26 | 2 | 92% |
| `circularity/scoring.py` | 65 | 1 | 98% |
| `product_data/database.py` | 51 | 16 | 69% |
| `product_data/errors.py` | 3 | 0 | 100% |
| `product_data/models.py` | 33 | 0 | 100% |
| `product_data/product_repository.py` | 53 | 4 | 92% |
| `product_data/seed.py` | 14 | 1 | 93% |
| **TOTAL** | **381** | **50** | **87%** |

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
   AI_PROVIDER=openai
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_MODEL=gpt-4o-mini
   GEMINI_API_KEY=your-gemini-api-key
   GEMINI_MODEL=gemini-flash-latest
   ```
   Choose `AI_PROVIDER=openai` or `AI_PROVIDER=gemini`; only the selected
   provider's API key is needed. The model settings are optional and default to
   `gpt-4o-mini` and `gemini-3.5-flash-lite`, respectively. Keep `.env` local; it
   is ignored by Git. You can generate a Flask secret key running the following command:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Without the selected provider's API key, the coach shows a configuration
   error instead of returning a mock answer.
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
