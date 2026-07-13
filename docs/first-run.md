# First run

Once the installation is complete, you can start the app.

## Start the Streamlit app

Run:

```bash
python3 -m streamlit run streamlit_app.py
```

This starts a local web app.

When it is ready, the terminal will show a local address such as:

```text
http://localhost:8501
```

Open that address in your browser.

## What you should see

You should see a simple web page with a chat-style interface and a sidebar for conversation history.

## If the app does not open

Check the terminal output for error messages. Common causes are:

- missing packages
- missing API keys
- a port already in use

If a port is already in use, try a different one:

```bash
python3 -m streamlit run streamlit_app.py --server.port 8502
```
