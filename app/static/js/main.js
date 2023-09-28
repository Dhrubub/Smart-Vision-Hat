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

// Attach the sendMessage function to the "Send" button
document.querySelector('.chat-content button').addEventListener('click', sendMessage);

