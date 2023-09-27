/* 
  source: https://www.codesdope.com/blog/article/12-creative-css-and-javascript-text-typing-animati/
  modified by: Dhruv Jobanputra
*/
function setupTypewriter(t) {
	let HTML = t.innerHTML;

	t.innerHTML = '';

	let cursorPosition = 0,
		tag = '',
		writingTag = false,
		tagOpen = false,
		typeSpeed = 100,
		tempTypeSpeed = 0;

	let type = function () {
		if (writingTag === true) {
			tag += HTML[cursorPosition];
		}

		if (HTML[cursorPosition] === '<') {
			tempTypeSpeed = 0;
			if (tagOpen) {
				tagOpen = false;
				writingTag = true;
			} else {
				tag = '';
				tagOpen = true;
				writingTag = true;
				tag += HTML[cursorPosition];
			}
		}
		if (!writingTag && tagOpen) {
			tag.innerHTML += HTML[cursorPosition];
		}
		if (!writingTag && !tagOpen) {
			if (HTML[cursorPosition] === ' ') {
				tempTypeSpeed = 0;
			} else {
				tempTypeSpeed = Math.random() * typeSpeed + 1000 / HTML.length;
			}
			t.innerHTML += HTML[cursorPosition];
		}
		if (writingTag === true && HTML[cursorPosition] === '>') {
			tempTypeSpeed = Math.random() * typeSpeed + 1000 / HTML.length;
			writingTag = false;
			if (tagOpen) {
				let newSpan = document.createElement('span');
				t.appendChild(newSpan);
				newSpan.innerHTML = tag;
				tag = newSpan.firstChild;
			}
		}

		cursorPosition += 1;
		if (cursorPosition < HTML.length) {
			setTimeout(type, tempTypeSpeed);
		}
	};

	return {
		type: type,
	};
}

let typer = document.getElementsByClassName('typewriter');

for (let i = 0; i < typer.length; i++) {
	let typewriter = setupTypewriter(typer[i]);

	typewriter.type();
}
