const data = {
	dates: "According to the Fremantle Ports website, the Sydney Express ship is not scheduled to arrive at the Fremantle port in the next month (September 2023). The ship's last arrival at the port was on September 7, 2023, and its next arrival is not scheduled until October 20, 2023.\nHere are the arrival and departure dates of the Sydney Express ship at the Fremantle port in the next 3 months:\nSeptember: Not scheduled\nOctober:\nArrival: October 20, 2023\nDeparture: October 21, 2023\nNovember:\nArrival: November 17, 2023\nDeparture: November 18, 2023\nDecember:\nArrival: December 15, 2023\nDeparture: December 16, 2023\nI hope this helps!",
	ports: "The Sydney Express is a container ship operated by Hapag-Lloyd. It has visited several ports in Australia this year, including:\nPort Botany, New South Wales\nPort of Melbourne, Victoria\nPort of Brisbane, Queensland\nPort of Fremantle, Western Australia\nPort of Adelaide, South Australia\nPort of Darwin, Northern Territory\nThe Sydney Express is a large container ship, with a capacity of 18,000 TEU. It typically makes one or two voyages to Australia each month, carrying a variety of cargo, including containers, cars, and machinery.\nHere are the specific dates when the Sydney Express visited each port in Australia this year:\nPort Botany: January 15, February 12, March 11, April 9, May 8, June 6, July 5, August 3, September 7, October 20, November 17, December 15\nPort of Melbourne: January 22, February 20, March 19, April 17, May 16, June 14, July 13, August 11, September 10, October 23, November 19, December 17\nPort of Brisbane: January 29, February 27, March 26, April 24, May 23, June 21, July 20, August 18, September 17, October 28, November 24, December 22\nPort of Fremantle: February 5, March 4, April 2, May 1, June 6, July 5, August 3, September 7, October 20, November 17, December 15\nPort of Adelaide: February 12, March 11, April 9, May 8, June 6, July 5, August 3, September 7, October 20, November 17, December 15\nPort of Darwin: March 4, April 2, May 1, June 6, July 5, August 3, September 7, October 20, November 17, December 15\nPlease note that these are just the dates that the Sydney Express has visited these ports so far this year. The ship's schedule may change in the future.",
	default: "I'm sorry I don't have that information.",
};

// Get the textarea element
const textarea = document.getElementById('inputTextarea');
const sendButton = document.getElementById('sendButton');
const answerTextarea = document.getElementById('answerTextarea');
const loader = document.getElementsByClassName('loader')[0];
answerTextarea.style.display = 'none';
// Function to adjust the number of rows based on content
function adjustTextareaRows() {
	const minimumRows = 3; // Set a minimum of 3 rows
	const lineHeight = parseInt(getComputedStyle(textarea).lineHeight);

	const previousRows = textarea.rows;
	textarea.rows = minimumRows; // Reset rows to the minimum

	const currentRows = Math.min(
		Math.floor(textarea.scrollHeight / lineHeight),
		10
	);
	textarea.rows = Math.max(currentRows, minimumRows); // Set rows to the maximum of currentRows and minimumRows

	// If rows have changed, you can perform any necessary actions here
	if (textarea.rows !== previousRows) {
		// Rows have changed, you can perform actions here
	}
}

// Attach an event listener for input
textarea.addEventListener('input', adjustTextareaRows);

// Initially adjust rows based on placeholder text
adjustTextareaRows();

async function sendData() {
	const value = textarea.value;
	const response = await fetch('/search_chat', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ value: value }),
	});
	const data = await response.json();
	const out = data.result;
	return out;
}

// Function to check if there is text in the textarea and change the button color
function checkTextareaContent() {
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

async function senddata() {
	if (textarea.value.trim() !== '') {
		answerTextarea.style.display = 'none';

		loader.style.display = 'inline';

		const result = await sendData();
		console.log(result);
		answerTextarea.innerText = result;

		answerTextarea.style.display = 'block';
		loader.style.display = 'none';
		answerTextarea.innerHTML = result;
	}
}
