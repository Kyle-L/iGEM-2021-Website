1. Clone the repository.
```
$ git clone git@github.com:Kyle-L/iGEM-2021-Website.git
```

2. Check into the cloned repository.
```
cd iGEM-2021-Website/
```

3. Install Pipenv using pip, install pip if you haven't already.
```
pip install pipenv
```

4. Setup a virtual environment with Pipenv.
```
$ python -m venv env
```

5. Start the virtual environment
```
$ source env/bin/activate
```

6. Install the requirements
```
$ pip install -r requirements.txt
```

7. Create the file `.env` at the root of `/iGEM-2021-Website` with following information. Replace `Your_username` and `Your_password` with your iGEM info.
```
IGEM_USERNAME=Your_username
IGEM_PASSWORD=Your_password
```

8. Run `python wikisync.py`