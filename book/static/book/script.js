
document.addEventListener('DOMContentLoaded', () => {
    toggle_model();
    let index = 0;
    if (window.location.pathname.endsWith("/")) {
        const nav1 = document.querySelector('#nav-first');
        const nav2 = document.querySelector('#nav-sec');
        nav1.style.display = 'block';
        nav2.style.display = 'none';
    }
    else {
        const nav1 = document.querySelector('#nav-first');
        const nav2 = document.querySelector('#nav-sec');
        nav1.style.display = 'none';
        nav2.style.display = 'block';
    }
    document.addEventListener('click', e => {
        dropdown(e);
        search(e);
        payment(e);
        rating(e);
        selected_rooms(e);
        section_scroll(e);
        filter_target(e);
        displaySubmit(e);
        triger(e);


        let slide_index = document.querySelectorAll('.small-slide').length;
        slide_index = slide_index - 4;
        if (e.target.matches('.slide-nav-button')) {
            const right = document.querySelector('.right');
            const left = document.querySelector('.left');
            if (e.target.matches('.right')) {
                index++;
                nav_next(index);
                if (index == slide_index) {
                    right.style.display = 'none';
                }
            }
            else if (e.target.matches('.left')) {
                nav_prev(index);
                index--;
                if (index == 0) {
                    left.style.display = 'none';
                }
                if (index < slide_index) {
                    right.style.display = 'block';
                }

            }

        }

        return;
    })


})

function displaySubmit(e) {
    const hotelTriger = document.querySelector('.room-triger');
    const resTriger = document.querySelector('.table-triger');
    const submit = document.querySelector('#form-submit');
    if (e.target.matches('.table-triger')) {
        resTriger.style.display = "none";
        submit.style.display = "block";
    }
    else if (e.target.matches('.room-triger')) {
        hotelTriger.style.display = "none";
        submit.style.display = "block";
    }
}

function triger(e) {
    const hotel = document.querySelector('#hotel-click');
    const resturant = document.querySelector('#res-click');
    const category = document.querySelector('#category-advert')
    const div = document.querySelector('.selector');
    const hotelTriger = document.querySelector('.room-triger');
    const resTriger = document.querySelector('.table-triger');
    const submit = document.querySelector('#form-submit');
    const price = document.querySelector('#wholePrice');
    if (e.target.matches('#category-advert')) {
        category.addEventListener('change', () => {
            if (category.value == 'Hotel') {
                hotelTriger.style.display = "block";
                resTriger.style.display = "none";
                submit.style.display = "none";
                price.style.display = "none";
            }
            else if (category.value == 'Resturant') {
                hotelTriger.style.display = "none";
                resTriger.style.display = "block";
                submit.style.display = "none";
                price.style.display = "none";
            }
            else {
                hotelTriger.style.display = "none";
                resTriger.style.display = "none";
                submit.style.display = "block";
                price.style.display = "block";
            }

        })


    }
    return;
}

function filter_target(e) {
    const hotelCheck = document.querySelector('#check1');
    const apartmentCheck = document.querySelector('#check2');
    const resortCheck = document.querySelector('#check3');
    const resturantCheck = document.querySelector('#check4');
    const checked = document.querySelector('.checked');
    let first_time = 0;
    if (checked == null)
        first_time = 1;
    if (e.target.matches('#check1')) {
        if (!hotelCheck.classList.contains('checked')) {
            hotelCheck.classList.add('checked');
            filter_by_category('Hotel', first_time);
        }
        else
            hotelCheck.classList.remove('checked');
    }
    else if (e.target.matches('#check2')) {
        if (!apartmentCheck.classList.contains('checked')) {
            apartmentCheck.classList.add('checked');
            filter_by_category('Apartment', first_time);
        }

        else
            apartmentCheck.classList.remove('checked');
    }
    else if (e.target.matches('#check3')) {
        if (!resortCheck.classList.contains('checked')) {
            resortCheck.classList.add('checked');
            filter_by_category('Resort', first_time);
        }
        else
            resortCheck.classList.remove('checked');
    }
    else if (e.target.matches('#check4')) {
        if (!resturantCheck.classList.contains('checked')) {
            resturantCheck.classList.add('checked');
            filter_by_category('Resturant', first_time);
        }
        else
            resturantCheck.classList.remove('checked');
    }
    return;
}
function filter_by_category(category, first_time) {
    const selectedCards = document.querySelectorAll(`.${category}`);
    const allCards = document.querySelectorAll('.card');
    if (first_time == 1) {
        for (let i = 0; i < allCards.length; i++) {
            allCards[i].style.display = 'none';
        }
    }
    for (let i = 0; i < selectedCards.length; i++) {
        selectedCards[i].style.display = 'block';
    }
    return;
}

function section_scroll(e) {
    if (e.target.matches('#section-block-1')) {

        section = document.querySelector('.section-2');
        if (section.classList.contains('hidden-section')) {
            section.classList.remove('hidden-section');
            section.classList.add('show-section');
        }
        else {
            section.classList.remove('show-section');
            section.classList.add('hidden-section');
            return;
        }
        length = document.querySelector('.section-1').offsetHeight;
        navlenght = document.querySelector('.navbar').offsetHeight;
        window.scrollBy(0, length + navlenght);
    }
    else if (e.target.matches('#section-block-2')) {

        section = document.querySelector('.section-3');
        if (section.classList.contains('hidden-section')) {
            section.classList.remove('hidden-section');
            section.classList.add('show-section');
        }
        else {
            section.classList.remove('show-section');
            section.classList.add('hidden-section');
            return;
        }
        length = document.querySelector('.section-1').offsetHeight;
        navlenght = document.querySelector('.navbar').offsetHeight;
        window.scrollBy(0, length + navlenght);
    }
    else if (e.target.matches('#section-block-3')) {

        section = document.querySelector('.section-4');
        if (section.classList.contains('hidden-section')) {
            section.classList.remove('hidden-section');
            section.classList.add('show-section');
        }
        else {
            section.classList.remove('show-section');
            section.classList.add('hidden-section');
            return;
        }
        length = document.querySelector('.section-1').offsetHeight;
        navlenght = document.querySelector('.navbar').offsetHeight;
        window.scrollBy(0, length + navlenght);
    }
    else if (e.target.matches('#section-block-4')) {

        section = document.querySelector('.section-5');
        if (section.classList.contains('hidden-section')) {
            section.classList.remove('hidden-section');
            section.classList.add('show-section');
        }
        else {
            section.classList.remove('show-section');
            section.classList.add('hidden-section');
            return;
        }
        length = document.querySelector('.section-1').offsetHeight;
        navlenght = document.querySelector('.navbar').offsetHeight;
        window.scrollBy(0, length + navlenght);
    }
    return;
}
function nav_next(index) {
    const width = document.querySelector('.small-slide').offsetWidth;
    const left = document.querySelector('.left');
    const track = document.querySelector('.slide-container');
    track.style.transform = `translateX(-${index * width}px)`;
    left.style.display = 'block';
    return;
}

function nav_prev(index) {
    const width = document.querySelector('.small-slide').offsetWidth;
    const track = document.querySelector('.slide-container');
    track.style.transform = `translateX(-${(index - 1) * width}px)`;
    return;
}
function payment(e) {
    if (e.target.matches('.final-payment-btn')) {
        const price_per_night = document.querySelector('.price-per-night');
        const nights = document.querySelector('.stay-days');
        const total_payment = document.querySelector('.total-payment');
        const start_date_input = document.querySelector('.start-date');
        const end_date_input = document.querySelector('.end-date');
        const input_total = document.querySelector('.input-total');
        const start_date = new Date(start_date_input.value);
        const end_date = new Date(end_date_input.value);
        let timeDifference = end_date.getTime() - start_date.getTime();
        let no_of_nights = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
        let total = 0;
        total = no_of_nights * parseFloat(price_per_night.innerHTML);
        console.log(total);
        nights.innerHTML = `${no_of_nights}`;
        total_payment.innerHTML = `${total}`;
        input_total.value = total;

    }
    else {
        return;
    }
}
function selected_rooms(e) {
    if (e.target.matches('#room_selected_button')) {
        const garde = document.querySelectorAll('.room-selector');
        const Array = document.querySelectorAll('.payment-modal-selected-rooms');
        const secondArray = document.querySelectorAll('.price-table-indiv-price');
        const roomTotal = document.querySelectorAll('.room-total-price');
        const priceArray = document.querySelectorAll('.room-price');
        const total_price = document.querySelector('.total');
        const input_total = document.querySelector('.input-total');
        let total = 0;
        let num = 0;
        for (let i = 0; i < Array.length; i++) {
            Array[i].value = garde[i].value;
            secondArray[i].innerHTML = `${garde[i].value}`;
            if (priceArray.length > 0) {
                num = parseInt(priceArray[i].innerHTML) * parseInt(secondArray[i].innerHTML);
                roomTotal[i].innerHTML = `${num}`
                total += parseInt(roomTotal[i].innerHTML);
            }

        }
        if (total_price != null)
            total_price.innerHTML = total;
        if (input_total != null)
            input_total.value = total;
    }
    else {
        return;
    }

}

function rating(e) {
    const star_input = document.querySelectorAll('.star-input');
    const rating = document.querySelector('.customer-rating');
    const rating_label = document.querySelector('.rate-label');
    for (let i = 0; i < star_input.length; i++) {
        if (e.target === star_input[i]) {
            rating_label.innerHTML = star_input.length - i;
            rating.value = rating_label.innerHTML;
            rating_label.innerHTML += '.0';
            return;
        }
    }
    return;
}

function toggle_model() {
    const button = document.querySelector("#review-buttton");

    if (button !== null) {
        button.click();
    }
    return
}
function search(e) {
    if (e.target.matches('#done-selection')) {
        const field = document.querySelector('#field');
        const adults = document.querySelector('#adults-no');
        const childs = document.querySelector('#children-no');
        const rooms = document.querySelector('#rooms-no');
        field.value = `${adults.value} Adults ,${childs.value} Children ,${rooms.value} rooms`
    }
    else if (e.target.matches('#done-selection-1')) {
        const field = document.querySelector('#field-1');
        const adults = document.querySelector('#adults-no-1');
        const childs = document.querySelector('#children-no-1');
        const rooms = document.querySelector('#rooms-no-1');
        field.value = `${adults.value} Adults ,${childs.value} Children ,${rooms.value} rooms`
    }
    return;

}
function dropdown(e) {
    if (e.target.matches('#section-dropdown')) {
        CurrentDropdown = e.target.closest('[data-dropdown]');
        CurrentDropdown.classList.toggle('active');
    }
    document.querySelectorAll('[data-dropdown].active').forEach(dropdown => {
        if (dropdown === CurrentDropdown)
            return;
        dropdown.classList.remove('active');
    })

}