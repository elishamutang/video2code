# Video2Code

![vide2code-demo](demo.gif)

## What is it?

A bare-bones prototype to _detect_ code, _extract_ it from a specific frame, and display it to the user in the appropriate format.

Built using Svelte and Django REST Framework.

![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)

## Live Preview

Visit [video2code.xyz](https://video2code.xyz)

## Install locally

## Pre-requisites

1. [Groq AI API key](https://groq.com/)
2. [Tesseract OCR Installer](#2-download-tesseract-ocr) (WINDOWS ONLY)

## Using Docker

I have created a docker compose file that you can run the application locally which will get the application running in no time! Simply do the following:

```
docker compose -f docker-compose-local.yml up
```

## 1. Clone Repo

## 2. Download Tesseract OCR

**(WINDOWS ONLY) PLEASE TAKE NOTE OF WHERE YOU INSTALL TESSERACT.EXE AS YOU WILL NEED TO SET THE PATH IN THE DJANGO APPLICATION.**

If you are on Windows, download the installer for Windows for Tesseract from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).

If you are on Linux, you can install Tesseract through the terminal using `apt-get install tesseract-ocr`.

For other operating systems, please follow the instructions from Tesseract's documentation [here](https://tesseract-ocr.github.io/tessdoc/Installation.html).

## 3. Server

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
TESSERACT_PATH=YOUR_PATH (WINDOWS ONLY, IF YOU ARE ON LINUX TESSERACT OCR IS ALREADY ADDED TO YOUR PATH)
```

5. Start project

```
cd adv_ui_ocrroo_project
python manage.py runserver
```

## 4. Client

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

## 5. Have fun!
