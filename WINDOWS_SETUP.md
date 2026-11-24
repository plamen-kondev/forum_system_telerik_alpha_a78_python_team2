## Run locally (Windows PowerShell)

### Prerequisites

- Python installed and added to PATH
- Git installed
- MariaDB installed and running
- MariaDB added to PATH

### 1. Clone the repository

```powershell
git clone <repo-url>
cd <repo-folder>
```

Skip this step if you have already cloned the repository.

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell prevents you from activating the virtual
environment, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Once activated, your terminal should display `(venv)`.

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

Note: `uvloop` is not supported on Windows.
Make sure the following dependency in `requirements.txt`
contains the platform-specific environment marker:

```text
uvloop==0.23.0; sys_platform != "win32"
```

This allows Linux/macOS users to install uvloop while
Windows users use Python's built-in asyncio event loop.

### 4. Create the environment configuration file

```powershell
Copy-Item .env.example .env
```

Make sure the database credentials in `.env` match
your local database configuration.

### 5. Verify MariaDB installation

```powershell
mariadb --version
```

If MariaDB is not recognized:

1. Locate your MariaDB installation directory.
   For example: `C:\Program Files\MariaDB 13.0\bin`
2. Search for "Edit the system environment variables"
   in the Windows Start menu.
3. Click "Environment Variables".
4. Under "User variables", select `Path` and click "Edit".
5. Click "New" and add the MariaDB bin directory.
6. Save the changes.
7. Completely restart VS Code.

Use your actual MariaDB installation directory.

After restarting VS Code, reactivate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

There is no need to reinstall dependencies.

### 6. Create the database and database users

```powershell
mariadb -u root -p -e "SOURCE db/setup_user.sql"
```

When prompted, enter your MariaDB root password
(the password you configured when installing MariaDB).

This script creates the `hot_takes` database and
the `forum_user` database accounts with the
required permissions.

### 7. Initialize the database schema

```powershell
mariadb -h 127.0.0.1 -u forum_user -p -e "SOURCE db/schema.sql"
```

When prompted, enter:

```text
forum_pass
```

Do not enter your root password for this step.

### 8. Verify the database setup

```powershell
mariadb -h 127.0.0.1 -u forum_user -p -e "USE hot_takes; SHOW TABLES;"
```

Enter `forum_pass` when prompted.

Expected output:

```text
+---------------------+
| Tables_in_hot_takes |
+---------------------+
| categories          |
| replies             |
| reply_votes         |
| topic_members       |
| topics              |
| users               |
+---------------------+
```

### 9. Start the application

```powershell
uvicorn app.main:app --reload
```

Open the Swagger UI in your browser:

http://127.0.0.1:8000/docs

### 10. Stop the application

Press `Ctrl + C` to stop the Uvicorn server.

To deactivate the virtual environment:

```powershell
deactivate
```

### Running the application again

Once the initial setup is complete, you only need
to execute the following commands from the project directory:

```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

There is no need to recreate the database, virtual
environment, or reinstall dependencies every time
you start the application.