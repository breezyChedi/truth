document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed'); // Debugging info

    let currentSlideIndex = 0;

    // Make sure markers are detected
    const markers = document.querySelectorAll('.marker');
    console.log('Total markers detected:', markers.length); // Debugging info

    // Attach click event listeners to markers
    markers.forEach(marker => {
        console.log('Adding click event to marker:', marker);  // Debugging info
        marker.addEventListener('click', event => {
            event.preventDefault();
            console.log('Marker clicked:', marker);  // Debugging info
            const slideIndex = parseInt(marker.getAttribute('data-slide-index'));
            showSlide(slideIndex);
        });
    });

    // Function to show the specified slide and highlight the corresponding marker
    function showSlide(index) {
        const slides = document.querySelectorAll('.slide');
        slides.forEach((slide, idx) => {
            slide.style.display = (idx === index) ? 'block' : 'none';
        });

        markers.forEach(marker => {
            marker.classList.remove('selected');
        });

        markers[index].classList.add('selected');

        currentSlideIndex = index;
    }

    // Function to navigate through slides
    window.changeSlide = function(direction) {
        const slides = document.querySelectorAll('.slide');
        currentSlideIndex += direction;

        if (currentSlideIndex >= slides.length) {
            currentSlideIndex = 0;
        } else if (currentSlideIndex < 0) {
            currentSlideIndex = slides.length - 1;
        }

        showSlide(currentSlideIndex);
    };

    // Initially display the first slide and highlight the first marker
    showSlide(currentSlideIndex);
});