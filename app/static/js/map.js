// script.js
API_KEY = '6f17bce624f94d769b279d0b8f61bc39';
let ports = ['Geraldton', 'BCJ4', 'BCJ3', 'Bunbury', 'Albany', 'Esperance'];
let jsonData;

// Example function to process the JSON data
function processData(data) {
    // Do something with the JSON data
    // For example, you can access specific properties or iterate through arrays
    for (let i = 0; i < ports.length; i++) {
      data[ports[i]] = JSON.parse(data[ports[i]]);
    }
    console.log('Processing data:', data);
    return data;
  }

async function fetch_table() {
    // Make an HTTP GET request to the Python server
    await fetch('/get_object')
        .then(response => response.json())
        .then(data => {
            // Assign the JSON data to the variable
            jsonData = data;
            // You can update your webpage or perform actions with the data
            // For example, you can call a function to process the data
            jsonData = processData(jsonData);
            let port = prompt("Please enter the desire port(either Geraldton, BCJ4, BCJ3, Bunbury, Albany, Esperance");
            destinations(jsonData,port.toLowerCase());
            console.log(jsonData);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function destinations(jsonData, destination) {
    // Assuming jsonData is an object with keys representing place names
    let markers = [];
    for (const place in jsonData) {
        // console.log(place);
        if(place.toLowerCase() == destination.toLowerCase()){
        if (jsonData.hasOwnProperty(place)) {
            const placeData = [jsonData[place]];
            // console.log(placeData);
            if (Array.isArray(placeData)) {
                for (const rows of placeData) {
                    console.log(rows);
                    for(const row in rows){
                        const productName = rows[row]['product'];
                        const country = productToCountry[productName.toUpperCase()];
                        console.log(productName);
                        console.log(country);
                        if (country) {
                            markers.push(country);
                        } else {
                            console.warn(`Country not found for product: ${productName}`);
                        }
                }
                }
            } else {
                console.warn(`placeData is not an array for place: ${place}`);
            }
        }
    }
    }
    // Move the console.log statement outside the loop
    // console.log(markers);
    addMarkersForPlaces(markers);
}


  
fetch_table();
    // Example usage:



function markers(jsonData){
    // Assuming jsonData is an object with keys representing place names
    let markers = [];
    for (const placeName in jsonData) {
    if (jsonData.hasOwnProperty(placeName)) {
      for (const row in jsonData[placeName]){
      let place = jsonData[placeName][row]['port'];
      // Now you can access placeName (the place name) and placeData (the data associated with it)
      console.log(`Place Name: ${placeName}`);
      console.log(`Place Data: `, place);
      markers.push(place);
    }
      
    }
  }
  addMarkersForPlaces(markers);
  console.log(markers)
}







var map = L.map('map-container').setView([0, 0], 2); // Set the initial view with a global scope

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
}).addTo(map);

function fetchCoordinatesForPlace(placeName) {
    // Replace 'YOUR_API_KEY' with your actual API key for the chosen geocoding service
    var geocodingServiceURL = `https://api.opencagedata.com/geocode/v1/json?q=${encodeURIComponent(
      placeName
    )}&key=${API_KEY}`;
  
    return fetch(geocodingServiceURL)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        if (data.results.length > 0) {
          var coordinates = data.results[0].geometry;
          return { lat: coordinates.lat, lng: coordinates.lng };
        } else {
          throw new Error('Place not found. Please enter a valid place name.');
        }
      });
  }

  function addMarkersForPlaces(placeNames) {
    // Iterate through the array of place names
    placeNames.forEach((placeName) => {
      // Use the fetchCoordinatesForPlace function to fetch coordinates for each place name
      fetchCoordinatesForPlace(placeName)
        .then((coordinates) => {
          // Create a marker for the place and add it to the map
          var marker = L.marker([coordinates.lat, coordinates.lng]).addTo(map);
          marker.bindPopup(placeName);
        })
        .catch((error) => {
          console.error(`Error for place ${placeName}:`, error.message);
        });
    });
  }


// Example usage: Add a marker for a place based on its name
// var placeNameInput = prompt("Enter the name of a place:");
var placeNameInput = ['Fremantle'];
if (placeNameInput) {
	addMarkersForPlaces(placeNameInput);
}

const productToCountry = {
    'UREA': 'QATAR',
    'UAN': 'USA',
    'MOP': 'EGYPT',
    'MAP': 'RSA',
};

  



 

  

  