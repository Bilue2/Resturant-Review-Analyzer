# Installation

This page explains how to install the project on your computer.

## Step 1: Install Python

Install Python 3.10 or newer.

To check whether Python is already installed, open a terminal and run:

```bash
python3 --version
```

If that does not work, try:

```bash
python --version
```

## Step 2: Open the project folder

Use a terminal to move into the repository folder:

```bash
cd /path/to/Resturant-Review-Analyzer
```

## Step 3: Create a virtual environment

A virtual environment keeps this project separate from other Python work on your computer.

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

You should see the name of the environment appear in your terminal prompt, such as (venv).

## Step 4: Install the dependencies

This downloads the libraries the project needs.

```bash
pip install -r requirements.txt
```

## Step 5: Confirm installation

You can check that the main app script exists by listing the repository files:

```bash
ls
```

You should see files such as streamlit_app.py and the scripts folder.

## Notes

The project uses Python modules from the app/ folder. For this reason, commands should be run from the project root.
