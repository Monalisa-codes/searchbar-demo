// search.js
const userInput = document.getElementById('user-input');
const searchButton = document.getElementById('search-button');
const resultsContainer = document.getElementById('results-container');

searchButton.addEventListener('click', () => {
    const userMessage = userInput.value;
    searchProducts(userMessage);
});

function searchProducts(message) {
    fetch('/?message=' + message, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        const response = data.response;
        const imagePaths = data.image_paths;
        resultsContainer.innerHTML = `<p>${response}</p>`;

        if (imagePaths && imagePaths.length > 0) {
            imagePaths.forEach(imagePath => {
                const image = document.createElement('img');
                image.src = imagePath;
                resultsContainer.appendChild(image);
            });
        }
    });
}
