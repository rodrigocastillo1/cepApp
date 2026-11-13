# cepApp

**Circular Economy Passport Application is the capstone project for the Compact Programming Course in Python at
the University of Applied Sciences and Arts Dortmund (Fachhochschule
Dortmund).**

cepApp is an AI-powered product-passport web application for exploring
electronics, assessing circularity, and understanding sustainability through
product data, analytics, and AI.

For more information about the project, please visit the demonstration video: [
Digital Product Passport Application - Group 11 CPC FH Dortmund](https://www.youtube.com/watch?v=ORGj7_iKnrg)


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
- Install Git, then clone the repository and open a terminal in the project folder. Use PowerShell on Windows or a terminal on macOS/Linux:

  ```text
  git clone https://github.com/rodrigocastillo1/cepApp.git
  cd cepApp
  ```

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
2. Open `.env` in a text editor and set `AI_PROVIDER` to `openai` or `gemini` (Use Gemini for quicker responses).
3. Add the selected provider's API key to `OPENAI_API_KEY` or `GEMINI_API_KEY`.
4. Optionally replace the `SECRET_KEY` placeholder with a random value. You can generate
   one with Python:

   ```text
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. The application image is public, so no GitHub login is needed. From the
   project folder, run:

   ```text
   docker compose pull
   docker compose up -d
   ```

6. Open [http://localhost:5000](http://localhost:5000) in your browser.

#### View service output

The `-d` option runs Compose in the background, so the startup command returns
without streaming service output. To follow logs from all services:

```text
docker compose logs --follow
```

Press **Ctrl+C** to stop following the logs; the services continue running.
To view only one service, append its name, for example:
`docker compose logs --follow web`.

---

## (If needed) Build and run the application image locally

For local builds run the following (Windows, macOS and Linux terminal):

```text
docker compose pull redpanda
docker build --tag ghcr.io/rodrigocastillo1/cepapp:latest .
docker compose up -d --pull never
```

This pulls Redpanda, builds the three application services from the local
source, and starts them without pulling their GHCR image.

### Stop the application

To stop the services, including when they were started in detached mode, run
this from the project folder on Windows, macOS, or Linux:

```text
docker compose down
```

## Run the tests

Run these commands from the project folder in a Python environment with the
project dependencies installed (including `pytest`). To run all tests in
`tests/test_subsystem_units.py` with verbose test names:

```text
python -m pytest -v tests/test_subsystem_units.py
```

To run one test, replace `test_function_name` with the test function's name:

```text
python -m pytest -v tests/test_subsystem_units.py::test_function_name
```

To list the test names in that file without running them:

```text
python -m pytest --collect-only -q tests/test_subsystem_units.py
```
