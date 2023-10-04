# Smart Vision Hat Dashboard

## Generates `requirements.txt`

```bash
pip freeze > requirements.txt
```

## Steps to run the dashboard

Simply run the `run.sh` script in the root directory of the project.

### Or you really want to do it manually

1. Create virtual environment called `venv` in the root directory of the project

    ```bash
    python3 -m venv venv
    ```

2. Activate the virtual environment

    ```bash
    source venv/bin/activate
    ```

3. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Run the dashboard

    ```bash
    flask run
    ```

5. Open the dashboard in the browser (Linux only)

    ```bash
    xdg-open http://127.0.0.1:5000
    ```


