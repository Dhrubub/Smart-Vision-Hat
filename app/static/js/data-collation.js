let jsonData;
const loader = document.getElementsByClassName('loader')[0];
async function fetchDataAndPopulateTable() {
	await fetch('get_dash_data')
		.then((response) => response.json())
		.then((data) => {
			// Get the tbody element by ID
			const tbody = document.getElementById('collated-data');
			// data = JSON.parse(data);
			console.log(data);
			jsonData = data;
			// Loop through the data and create table rows
			jsonData.forEach((item) => {
				const row = document.createElement('tr');
				// Loop through the keys (headings) in each item
				for (const key in item) {
					if (item.hasOwnProperty(key)) {
						const cell = document.createElement('td');
						cell.textContent = item[key];
						row.appendChild(cell);
					}
				}
				let id = item['ID'];
				// Add a data-href attribute to specify the target page URL
				// row.setAttribute('data-href', '/analyse/lookup.html'); // Replace 'page2.html' with the actual URL
				row.setAttribute('data-href', `/analyse/lookup/${id}`); // Replace 'page2.html' with the actual URL
				// Add a click event listener to redirect when a row is clicked
				row.addEventListener('click', () => {
					const targetUrl = row.getAttribute('data-href');
					// console.log('Target URL:', targetUrl);
					if (targetUrl) {
						window.location.href = targetUrl;
					}
				});
				// Append the row to the tbody
				tbody.appendChild(row);
			});
			company_filter();
		})
		.catch((error) => {
			console.error('Error:', error);
		});
}

// Call the function to fetch data and populate the table
fetchDataAndPopulateTable();

function company_filter() {
	// Get the HTML elements
	const companyFilter = document.getElementById('company-filter');
	const tbody = document.getElementById('collated-data');

	// Define a function to create a dropdown option
	function createOption(value, text) {
		const option = document.createElement('option');
		option.value = value;
		option.textContent = text;
		return option;
	}

	// Function to populate the company name dropdown
	function populateCompanyDropdown() {
		// Get unique company names from the data
		const uniqueCompanyNames = [
			...new Set(jsonData.map((item) => item['COMPANY NAME'])),
		];

		// Clear existing options and add a "Reset" option
		companyFilter.innerHTML = '';
		companyFilter.appendChild(createOption('All', 'All'));

		// Add unique company names to the dropdown
		uniqueCompanyNames.forEach((companyName) => {
			companyFilter.appendChild(createOption(companyName, companyName));
		});
	}

	// Function to filter and populate the table
	function filterTable() {
		const selectedCompany = companyFilter.value;

		// Get all rows in the table
		const rows = tbody.querySelectorAll('tr');

		// Hide all rows initially
		rows.forEach((row) => {
			row.style.display = 'none';
		});

		// Show rows that match the selected company or show all rows if 'All' is selected
		rows.forEach((row) => {
			const companyName =
				row.querySelector('td:nth-child(2)').textContent; // Assuming the second column contains the company name
			if (selectedCompany === 'All' || companyName === selectedCompany) {
				row.style.display = 'table-row';
			}
		});
	}

	// Add event listeners
	companyFilter.addEventListener('change', filterTable);

	// Initial setup
	populateCompanyDropdown(); // Call this function to populate the dropdown initially
	filterTable();
}

// Call the company_filter function when the page loads
document.addEventListener('DOMContentLoaded', company_filter);

// Function to send a message to the chatbot
function sendMessageToChatbot() {
	// Get references to the input field and send button by their IDs
	const messageInput = document.getElementById('inputTextarea');
	const sendMessageButton = document.getElementById('sendButton');

	// Define the URL of your Flask server's /chatbot route
	const url = '/chatbot';

	// Add an event listener to the send button
	sendMessageButton.addEventListener('click', () => {
		loader.style.display = 'inline';

		// Get the message from the input field
		const message =
			messageInput.value +
			"(return a full JSON only don't return any text): " +
			JSON.stringify(jsonData);

		// Create a data object with the message

		const data = { message };
		console.log(data);

		// Configure the fetch request
		fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		})
			.then((response) => response.json())
			.then((responseJson) => {
				// Handle the chatbot's response here (responseJson)
				console.log(responseJson);
				let messageContent =
					responseJson['answer']['choices'][0]['message']['content'];
				let respond = messageContent;
				//   console.log(respond);
				// You can perform additional actions here with the chatbot's response
				filterTableWithJsonData(JSON.parse(respond));
				// Example: Send the answer to the server
				// sendAnswerToServer(messageContent);

				// Example: Fetch and populate table data
				// fetchDataAndPopulateTable();
				loader.style.display = 'none';
			})
			.catch((error) => {
				console.error('Error:', error);
			});
	});
}

// Call the function to set up the event listener
sendMessageToChatbot();

function filterTableWithJsonData(data) {
	// Get the tbody element by ID
	const tbody = document.getElementById('collated-data');

	// Clear the table before populating it with filtered data
	tbody.innerHTML = ''; // This line clears the existing table content.
	console.log(data);
	// Loop through the data and create table rows
	data.forEach((item) => {
		const row = document.createElement('tr');
		// Loop through the keys (headings) in each item
		for (const key in item) {
			if (item.hasOwnProperty(key)) {
				const cell = document.createElement('td');
				cell.textContent = item[key];
				row.appendChild(cell);
			}
		}
		let id = item['ID'];
		// Add a data-href attribute to specify the target page URL
		// row.setAttribute('data-href', '/analyse/lookup.html'); // Replace 'page2.html' with the actual URL
		row.setAttribute('data-href', `/analyse/lookup/${id}`); // Replace 'page2.html' with the actual URL
		// Add a click event listener to redirect when a row is clicked
		row.addEventListener('click', () => {
			const targetUrl = row.getAttribute('data-href');
			// console.log('Target URL:', targetUrl);
			if (targetUrl) {
				window.location.href = targetUrl;
			}
		});
		// Append the row to the tbody
		tbody.appendChild(row);
	});

	// Additional actions or filters can be applied as needed

	company_filter();
}

// Example usage:
// Pass your JSON data to the function to filter the table
// filterTableWithJsonData(filteredData);

const textarea = document.getElementById('inputTextarea');

// Function to check if there is text in the textarea and change the button color
function checkTextareaContent() {
	sendButton = document.getElementById('sendButton');

	if (textarea.value.trim() !== '') {
		sendButton.classList.add('send-btn-allowed'); // Add the blue-button class
	} else {
		sendButton.classList.remove('send-btn-allowed'); // Remove the blue-button class
	}
}

// Attach an event listener for input in the textarea
textarea.addEventListener('input', checkTextareaContent);

// Initially check textarea content on page load
checkTextareaContent();
