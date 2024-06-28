const slider = document.getElementById('n_cards_slider');
const displayer = document.getElementById('n_cards')
displayer.innerHTML = slider.value;

slider.oninput = function() {
    displayer.innerHTML = slider.value;
}