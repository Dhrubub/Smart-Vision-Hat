let jsonData;
let id;
document.addEventListener('DOMContentLoaded', function () {
    // Get the data-id attribute from the body element
    const section = document.querySelector('section[data-id]');
id = section.getAttribute('data-id');

    // Make an AJAX request to fetch the data from the API using the retrieved id
    fetch(`/api/data/${id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            jsonData = data;
            // Here, you can process the fetched data as needed, such as populating the table

            // Example: Populate a table with the fetched data
            const tableBody = document.getElementById("table");
      
            jsonData.forEach(item => {
                const row = document.createElement('tr');
                
                for (const key in item) {
                    if (item.hasOwnProperty(key)) {
                        const cell = document.createElement('td');
                        cell.textContent = item[key];
                        row.appendChild(cell);
                    }
                }
      
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
