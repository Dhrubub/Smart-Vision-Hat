from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/api/upload', methods=['POST'])
def upload():
    try:
        # Get data from the request JSON
        data = request.json

        # Extract device_id, image data, and items list from the JSON
        device_id = data.get('device_id')
        image_data = data.get('image')
        labels = data.get('labels')

        # Check if the user has set keep data to private

        # Search for all users attached to this device id
        # Add the data to those users




        # Check if device_id is provided
        if device_id is None:
            return jsonify({'message': 'Device ID is required'}), 400

        # Store the data in the database (for demonstration purposes, you would use a real database)
        # database[device_id] = {'image': image_data, 'items': items}

        # Return a success message
        return jsonify({'message': 'Data uploaded successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500