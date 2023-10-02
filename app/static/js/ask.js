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
