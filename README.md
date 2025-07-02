# Video 2 Code

## Installation

## Pre-requisites

1. [Groq AI API key](https://groq.com/)
2. [Tesseract OCR Installer](#2-download-tesseract-ocr)

## 1. Clone Repo

## 2. Download Tesseract OCR

**PLEASE TAKE NOTE OF WHERE YOU INSTALL TESSERACT.EXE AS YOU WILL NEED TO SET THE PATH IN THE DJANGO APPLICATION.**

If you are on Windows, download the installer for Windows for Tesseract from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).

For other operating systems, please follow the instructions from Tesseract's documentation [here](https://tesseract-ocr.github.io/tessdoc/Installation.html).

## 3. Client

The repository holds both the client (frontend) and server (backend) for the project. The client was built using Svelte. To setup the client, run the following:

1. Install project dependencies

```
npm install
```

2. Start client development server:

```
npm run dev
```

> If you are using VS Code, for better developer experience, please feel free to install the Svelte language support extension.

## 4. Server

The server was built using Django REST Framework. It currently stores the video that will be served to the frontend via the REST API. The extraction of a specific video frame and resulting code is done here. To setup the server, run the following:

1. Setup a virtual environment within the server folder (place it on the same level as project folder, .gitignore, and requirements.txt)

```
python -m venv .venv
```

2. Activate virtual environment

```
source .venv/Scripts/activate
```

3. Install project dependencies (make sure you are in the server directory)

```
pip install -r requirements.txt
```

4. Set up environment variables

```
GROQ_KEY=YOUR_KEY
TESSERACT_PATH=YOUR_PATH
```

5. Start project

```
cd adv_ui_ocrroo_project
python manage.py runserver
```

## 5. Have fun!
