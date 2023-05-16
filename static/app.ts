const discountSelector= document.querySelector('#discount') as HTMLSelectElement;
const discountFields = document.querySelector('#discount-fields') as HTMLDivElement;

discountSelector.addEventListener('change', () => {
    if (discountSelector.value == 'yes') {
        discountFields.removeAttribute('hidden');
    }
    else {
        discountFields.setAttribute('hidden', '');
    }
});