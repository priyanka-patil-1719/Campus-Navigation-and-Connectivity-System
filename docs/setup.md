# Setup and deployment

## Local setup

Use Python 3.10 or newer. From the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5000>. To use an already configured Python environment, install the requirements and run `python app.py`. On macOS/Linux, use `.venv/bin/python` instead of the Windows interpreter path. No assets need downloading at runtime, and no environment variables are required.

If port 5000 is occupied, select a different port in PowerShell:

```powershell
$env:PORT = '5001'
python app.py
```

Use <http://127.0.0.1:5001> in that case. Stop the server with Ctrl+C.

## Verification

```powershell
python -m unittest discover -s tests -v
```

No test package is required. The suite uses Python `unittest` and Flask's test client. Browser checks should include mobile navigation, scrolling the map/table, the full add/connect flow, directed arrows and weight labels, traversal playback, and empty-state recovery.

## Render

Publish this project to a Git repository and create a Render Python **Web Service**. If this project is a repository subdirectory, set its root directory accordingly.

| Setting | Value |
| --- | --- |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app` |
| Instance | Free, where available |

Gunicorn automatically reads `gunicorn.conf.py`. It binds to `0.0.0.0` and Render's `PORT`, uses one worker and four threads, and logs requests to standard output. No secret or database provisioning is needed. Gunicorn's requirement is platform-marked so Windows users can install the same requirements file; the Linux host installs Gunicorn.

Keep one worker and one instance. Every visitor shares the same in-memory graph. A process restart or free-service recycle restores the sample and loses edits. This is intentional for the classroom demonstration. The local Flask development server is for local use; use Gunicorn on the Linux host.

Reference: [Render Flask deployment](https://render.com/docs/deploy-flask), [Render free-service limitations](https://render.com/docs/free), [Flask Gunicorn documentation](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/).
