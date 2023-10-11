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
- Root
  |--- devices
  |    |--- Device ID 1
  |    |    |--- privacy: true
  |    |    |--- refresh_rate: 15
  |    |--- Device ID 2
  |    |    |--- privacy: false
  |    |    |--- refresh_rate: 20
  |
  |--- users
       |--- User ID 1
            |--- images
                 |--- -Image ID 1
                 |    |--- device_id: "Device ID 1"
                 |    |--- imageURL: "https://..."
                 |    |--- label: ["2 persons"]
                 |--- -Image ID 2
                 |    |--- device_id: "Device ID 1"
                 |    |--- imageURL: "https://..."
                 |    |--- label: ["2 persons"]
                 |
                 . . . (and so on for each image object)
```

Sample data:

```json
{
  "devices": {
    "a8:27:eb:a8:66:d2": {
      "privacy": true,
      "refresh_rate": 15
    },
    "b8:27:eb:a8:66:d1": {
      "privacy": false,
      "refresh_rate": 20
    }
  },
  "users": {
    "bbHF9TatSDP5djYNVZU7jMABAeH3": {
      "images": {
        "-NgJRZGOBoVdHPUOTqbu": {
          "device_id": "b8:27:eb:a8:66:d1",
          "imageURL": "https://firebasestorage.googleapis.com/v0/b/smart-vision-hat.appspot.com/o/Public%2Fab50053a-8486-46d6-b8a7-6fdf6ccadcaf?alt=media",
          "label": [
            "2 persons"
          ]
        },
      }
    }
  }
}      
```
