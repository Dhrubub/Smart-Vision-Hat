async function getAnswer() {
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: document.getElementById("question").value })
        });
        
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();
        document.getElementById("answer").textContent = data.answer;
    } catch (e) {
        console.log(`Error: ${e}`);
        document.getElementById("answer").textContent = "An error occurred.";
    }
}

// Speech recognition and synthesis
let recognition;

if ('webkitSpeechRecognition' in window) {
  recognition = new webkitSpeechRecognition();
  recognition.onresult = function(event) {
    const text = event.results[0][0].transcript;
    document.getElementById('question').value = text;
  };
}

function startListening() {
  if (recognition) {
    recognition.start();
  } else {
    alert("Your browser doesn't support speech recognition.");
  }
}

let synth = window.speechSynthesis;

function speakAnswer() {
  const answerText = document.getElementById("answer").textContent;
  const utterance = new SpeechSynthesisUtterance(answerText);
  synth.speak(utterance);
}

function stopSpeaking() {
  synth.cancel();
}

  
