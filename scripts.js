document.addEventListener('DOMContentLoaded', () => {
    const rectangleContent = document.getElementById('rectangleContent');
    //id="target-section"
    const rectangleTexts = ['A group of boers known as Jerusalemgangers believed they could trek to Jerusalem from Gauteng', 'Moses went South', 'Christianity is based on Ancient Egyptian beliefs', 'The Jews in Israel have no connection to the land of palestine or the Hebrews who followed Moses', 'The banks cause inflation because its profitable for them', "Israel's economy is dependenent on the exploitation of Africa", 'israel is a fake country', 'they were initially going to create israel in Uganda', 'his-story is whitewashed','The trans-atlantic slave trade began when the black jews of Spain and Portugal were persecuted','The Jewish identity has been whitewashed', "Africa has always been influencing the world", "Theres is no such thing as a red sea"]; // Corrected list of texts
    let currentIndex = 0;

    if (rectangleContent) { // Only run the code if rectangleContent exists
        function slideRectangle() {
            rand=getRandomInt(0,rectangleTexts.length-1)
            if (currentIndex >= rectangleTexts.length) {
                currentIndex = 0; // Reset index if it exceeds text array length
            }
            rectangleContent.innerText = rectangleTexts[rand];
            currentIndex++;
        }

        setInterval(slideRectangle, 10000); // Change text every 10 seconds (adjust as needed)
        slideRectangle(); // Initial text display
    }

    // Other code that you want to run regardless of rectangleContent's existence
    console.log("Rest of the code is executing.");
});

function getRandomInt(min, max) {
    console.log('rand')
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


//http://localhost:8000/navbar.html
// Navbar loading function
function loadNavbar() {
    const hostname = window.location.hostname;
    let baseUrl;

    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        baseUrl = 'http://localhost:8000';
    } else {
        baseUrl = 'http://192.168.3.34:8000';
    }

    fetch(`${baseUrl}/navbar.html`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('navbar').innerHTML = data;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            document.getElementById('navbar').innerHTML = '<p>Error loading navbar</p>';
        });
}


window.onload = loadNavbar;
