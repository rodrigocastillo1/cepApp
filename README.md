# cepApp

**Circular Economy Passport Application is the capstone project for the Compact Programming Course in Python at
the University of Applied Sciences and Arts Dortmund (Fachhochschule
Dortmund).**

cepApp is an AI-powered product-passport web application for exploring
electronics, assessing circularity, and understanding sustainability through
product data, analytics, and AI.

For more information about the project, please visit the demonstration video: ...

Prof. Dr. Galyna Tabunshchyk

Group 11.
Topic: AI-Powered Circular Economy Product Passport

| Student                    | Matriculation number | Subsystem                                                        |
| -------------------------- | -------------------- | ---------------------------------------------------------------- |
| Rodrigo Castillo Alcantara | ESE - 7226791        | - Analytics Subsystem<br>- AI provider Subsystem               |
| Elnur Allazov              | ESE - 7226316        | - Product Data Subsystem<br>- Circularity Assessment Subsystem |
---
## How to run the application with Docker Compose

### Prerequisites

- **Windows or macOS:** Install and start [Docker Desktop](https://docs.docker.com/get-docker/). It includes Docker Compose.
- **Linux:** Install [Docker Engine](https://docs.docker.com/engine/install/) and the [Docker Compose plugin](https://docs.docker.com/compose/install/linux/). Follow Docker's Linux post-install steps if you want to run Docker commands without `sudo`.

Verify Docker and Compose are available from a terminal:

```text
docker --version
docker compose version
```

### Configure and start

1. Make a private `.env` copy of the tracked template from the project folder.
   In PowerShell, use:
   ```powershell
   Copy-Item .env.template .env
   ```
   On macOS or Linux, use:
   ```sh
   cp .env.template .env
   ```
   If you already have a `.env` file, edit it instead of overwriting it.
2. Open `.env` in a text editor and set `AI_PROVIDER` to `openai` or `gemini`. Use gemini for a better performance.
3. Add the selected provider's API key to `OPENAI_API_KEY` or
   `GEMINI_API_KEY`.
4. Optionally select the model using `OPENAI_MODEL` or `GEMINI_MODEL`. The
   template provides default model names.
5. Optionally replace the `SECRET_KEY` placeholder with a random value. You can generate
   one with Python:

   ```text
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

6. In a terminal opened in the project folder, start the services. Compose
   automatically reads the `.env` file:

   ```text
   docker compose up --build
   ```

7. Open [http://localhost:5000](http://localhost:5000) in your browser.

### Stop the application

Press **Ctrl+C** in the terminal running Compose, then run:

```text
docker compose down
```
