// Detect system color scheme
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    // Load general_dark.css
    document.getElementById("theme").setAttribute("href", "general_dark.css");
  } else {
    // Load general_light.css
    document.getElementById("theme").setAttribute("href", "general_light.css");
  }
  
  // Listen for changes in system setting
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (e.matches) {
      // Switch to general_dark.css
      document.getElementById("theme").setAttribute("href", "general_dark.css");
    } else {
      // Switch to general_light.css
      document.getElementById("theme").setAttribute("href", "general_light.css");
    }
  });


document.addEventListener("DOMContentLoaded", function () {
    // Placeholder for login status, replace with actual login check
    const userLoggedIn = false; 
    const userMenu = document.getElementById('userMenu');
    if (userLoggedIn) {
        userMenu.innerHTML = `
            <a class="dropdown-item" href="#profile">Profile</a>
            <a class="dropdown-item" href="#logout">Logout</a>
        `;
    } else {
        userMenu.innerHTML = `
            <a class="dropdown-item" href="#signup">Sign Up</a>
        `;
    }
    document.getElementById("adjust_rate").addEventListener("click", function () {
        const new_rate = document.getElementById("refresh_rate").value;
        fetch("/adjust_refresh_rate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ new_rate }),
        })
        .then((response) => response.json())
        .then((data) => {
            alert("Refresh rate adjusted!");
        });
    });

    document.getElementById("update_software").addEventListener("click", function () {
        fetch("/update_software", {
            method: "POST",
        })
        .then((response) => response.json())
        .then((data) => {
            alert("Software updated!");
        });
    });
});

function sendMessage() {
    var message = document.querySelector('.chat-content textarea').value;
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'message=' + encodeURIComponent(message)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the server's response, e.g., display it in the chat box
        alert(data.response);
    });
}

function getAnswer() {
    let question = document.getElementById("question").value;
    let loading = document.getElementById("loading");
    let answer = document.getElementById("answer");
    loading.style.display = "block";
    answer.textContent = "";
    
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: question
        })
    })
    .then(response => {
        loading.style.display = "none";
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        answer.textContent = data.answer;
    })
    .catch(error => {
        answer.textContent = "Error: " + error;
    });
}


// Attach the sendMessage function to the "Send" button
document.querySelector('.chat-content button').addEventListener('click', sendMessage);
  