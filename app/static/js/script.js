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




function showDeleteModal(event_id) {
    var modal_container = document.querySelector('.modal_container.modal_container_' + event_id);
    var modal = document.getElementById('modal_' + event_id);
    modal_container.style.display = 'block';
    modal.style.display='block';
   
}

function cancel(event_id) {
    var modal_container = document.querySelector('.modal_container.modal_container_' + event_id);
    var modal = document.getElementById('modal_' + event_id);
    modal_container.style.display = 'none';
    modal.style.display='none';
   
}

function showDeleteCommentModal(comment_id) {
    var modal_container = document.querySelector('.comment_modal_container.comment_modal_container_' + comment_id);
    var modal = document.getElementById('comment_modal_' + comment_id);
    modal_container.style.display = 'block';
    modal.style.display='block';
}

function cancelCommentModal(comment_id) {
    var modal_container = document.querySelector('.comment_modal_container.comment_modal_container_' + comment_id);
    var modal = document.getElementById('comment_modal_' + comment_id);
    modal_container.style.display = 'none';
    modal.style.display='none';
}

function showRemoveParentModal(parent_id) {
    var modal_container = document.querySelector('.parent_modal_container_' + parent_id);
    var modal = document.getElementById('parent_modal_' + parent_id);
    modal_container.style.display = 'block';
    modal.style.display='block';
}

function cancelRemoveParent(parent_id) {
    var modal_container = document.querySelector('.parent_modal_container_' + parent_id);
    var modal = document.getElementById('parent_modal_' + parent_id);
    modal_container.style.display = 'none';
    modal.style.display='none';

}

function showRemoveNannyModal(nanny_id) {
    var modal_container = document.querySelector('.nanny_modal_container_' + nanny_id);
    var modal = document.getElementById('nanny_modal_' + nanny_id);
    modal_container.style.display = 'block';
    modal.style.display='block';
}

function cancelRemoveNanny(nanny_id) {
    var modal_container = document.querySelector('.nanny_modal_container_' + nanny_id);
    var modal = document.getElementById('nanny_modal_' + nanny_id);
    modal_container.style.display = 'none';
    modal.style.display='none';

}

function showRemoveProfileModal(id) {
    var modal_container = document.querySelector('.profile_modal_container_' + id);
    var modal = document.getElementById('profile_modal_' + id);
    modal_container.style.display = 'block';
    modal.style.display='block';
}

function cancelRemoveProfile(id) {
    var modal_container = document.querySelector('.profile_modal_container_' + id);
    var modal = document.getElementById('profile_modal_' + id);
    modal_container.style.display = 'none';
    modal.style.display='none';

}





