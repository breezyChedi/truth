document.addEventListener('DOMContentLoaded', function() {
    function initializeAccordions(container) {
        const accordionWords = container.querySelectorAll('.accordion-word');

        accordionWords.forEach((word) => {
            // Avoid processing the same accordion twice
            if (word.nextElementSibling && word.nextElementSibling.classList.contains('accordion-content')) {
                return;
            }

            const contentText = word.getAttribute('data-content');
            const content = document.createElement('div');
            content.classList.add('accordion-content');
            content.innerHTML = contentText; // Use innerHTML to support nested HTML

            word.insertAdjacentElement('afterend', content);

            word.addEventListener('click', () => {
                const isVisible = content.style.display === 'block';

                // Close all other open accordions
                closeAllAccordions(container, content);

                // Toggle the clicked accordion
                content.style.display = isVisible ? 'none' : 'block';

                // Initialize nested accordions if they exist and are being displayed
                if (!isVisible) {
                    initializeAccordions(content);
                }
            });
        });
    }

    function closeAllAccordions(container, exceptElement) {
        const openAccordions = container.querySelectorAll('.accordion-content');

        openAccordions.forEach((accordion) => {
            if (accordion !== exceptElement && accordion.style.display === 'block') {
                accordion.style.display = 'none';
            }
        });
    }

    initializeAccordions(document.body);
});



function loadNavbar() {
    const hostname = window.location.hostname;
    let baseUrl;

    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        baseUrl = 'http://localhost:8000';
    } else {
        baseUrl = 'http://192.168.3.34:8000';
    }

    fetch(`${baseUrl}/navbar.html`).then(response => {
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
