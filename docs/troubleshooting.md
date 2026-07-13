# Troubleshooting

## Problem: the app does not start

### Symptoms

The terminal shows an error when you run the Streamlit app.

### Cause

The required Python packages may not be installed yet.

### Fix

Run:

```bash
pip install -r requirements.txt
```

## Problem: a missing key error appears

### Symptoms

The app reports that an API key is missing.

### Cause

The .env file is missing or incomplete.

### Fix

Add the required values to your .env file.

## Problem: import errors appear

### Symptoms

Messages mention ModuleNotFoundError or similar.

### Cause

The script may have been run in the wrong way.

### Fix

Run commands from the project root and use the module form when possible.

## Problem: no results appear

### Symptoms

The app runs but returns empty or weak answers.

### Cause

There may be no indexed review data or the data may not have been prepared correctly.

### Fix

Run the cleaning, chunking, and indexing steps again.
