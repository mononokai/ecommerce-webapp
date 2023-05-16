"use strict";
const discountSelector = document.querySelector('#discount');
const discountFields = document.querySelector('#discount-fields');
discountSelector.addEventListener('change', () => {
    if (discountSelector.value == 'yes') {
        discountFields.removeAttribute('hidden');
    }
    else {
        discountFields.setAttribute('hidden', '');
    }
});
//# sourceMappingURL=app.js.map