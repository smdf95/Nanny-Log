document.addEventListener('DOMContentLoaded', () => {

    // Function for opening and closing the menu on tablets and phones

    const mainMenu = document.querySelector('.links');
    const openMenu = document.querySelector('.openMenu');
    const closeMenu = document.querySelector('.closeMenu');


    openMenu.addEventListener('click', show);
    closeMenu.addEventListener('click', close);


    function show() {
        mainMenu.style.left = "0";
        mainMenu.style.boxShadow = "0 0 200px 100px #000000";
    }

    function close() {
        mainMenu.style.left = "-70%";
        mainMenu.style.boxShadow = "none";

    }
});


document.addEventListener('DOMContentLoaded', () => {

    // Function for opening and closing the add event tab

    const events = document.querySelector('.events');
    const addEvent = document.querySelector('.add_event');
    const closeTab = document.querySelector('.close_tab');


    addEvent.addEventListener('click', show);
    closeTab.addEventListener('click', close);


    function show() {
        events.style.bottom = "20px";
        events.style.boxShadow = "0 0 25px #000000";
        addEvent.style.bottom = "-100px";
    }

    function close() {
        events.style.bottom = "-450px";
        events.style.boxShadow = "none";

        setTimeout(function () {
            addEvent.style.bottom = "20px";
        }, 900);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            // Toggle the class on the next sibling (which is the image) of the checkbox's parent (the label)
            var image = checkbox.closest('label').querySelector('img');
            if (checkbox.checked) {
                image.classList.add('selected-image');
            } else {
                image.classList.remove('selected-image');
            }
        });
    });
});

function redirectToUrl(element) {
    var url = element.dataset.url;
    window.location.href = url;
}
