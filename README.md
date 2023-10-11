# Smart Vision Hat Dashboard

## Dashboard
Visit [Smart Vision Hat](https://misoto22.pythonanywhere.com).


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

## Database Schema

``` bash
Database
│
└─── User UID (e.g., 4Lp1WS5JOQbpSN3DOhKIU6vDqiW2)
    │
    ├─── user_data
    │    ├─── privacy_preference: true/false
    │    ├─── device_ID: "sample_device_ID_123"
    │    └─── refresh_rate: 2
    │
    └─── images
         │
         ├─── image1_ID
         │    ├─── detected_results: "Example Detected Results 1"
         │    └─── imageURL: "https://link_to_image1.jpg"
         │
         ├─── image2_ID
         │    ├─── detected_results: "Example Detected Results 2"
         │    └─── imageURL: "https://link_to_image2.jpg"
         │
         └─── ...

```

```json
{
  "4Lp1WS5JOQbpSN3DOhKIU6vDqiW2": {
    "user_data": {
      "privacy_preference": true,
      "device_ID": "sample_device_ID_123",
      "refresh_rate": 60
    },
    "images": {
      "image1_ID": {
        "detected_results": "Example Detected Results 1",
        "imageURL": "https://link_to_image1.jpg"
      },
      "image2_ID": {
        "detected_results": "Example Detected Results 2",
        "imageURL": "https://link_to_image2.jpg"
      },
      ...
    }
  },
  ...
}
```
