// settings bs popover
var popover = new bootstrap.Popover(document.querySelector('.settings-popover'), {
    trigger: 'focus'
})

// adjust max_colors text value from slider
max_colors_value = document.getElementById('max_colors_value');
color_range = document.getElementById('colors');
setColorValue = () => {
    newValue = Number((color_range.value - color_range.min) * 100 / (color_range.max - color_range.min));
    max_colors_value.innerHTML = `<span>Max Colors: ${color_range.value}</span>`;
};
document.addEventListener("DOMContentLoaded", setColorValue);
color_range.addEventListener('input', setColorValue);

// adjust sensitivity text value from slider
sensitivity_value = document.getElementById('sensitivity_value');
sensitivity_range = document.getElementById('sensitivity');
setSensitivityValue = () => {
    newValue = Number((sensitivity_range.value - sensitivity_range.min) * 100 / (sensitivity_range.max - sensitivity_range.min));
    sensitivity_value.innerHTML = `<span>Sensitivity: ${sensitivity_range.value}</span>`;
};
document.addEventListener("DOMContentLoaded", setSensitivityValue);
sensitivity_range.addEventListener('input', setSensitivityValue);

// copy hex value to clipboard
function copy(btn) {
    // get the hex code from data-attr
    const hex = btn.getAttribute('data');
    // setup a temp textarea to store the hex for copying
    const body = document.querySelector('body');
    const area = document.createElement('textarea');
    area.setAttribute('readonly', '');
    area.style.position = 'absolute';
    area.style.left = '-9999px';
    // add the temp textarea to the body
    body.appendChild(area);
    // set the text area value to the hex code
    area.value = hex;
    area.select();
    // copy the selected text
    document.execCommand('copy');
    // remove the textarea
    body.removeChild(area);
}