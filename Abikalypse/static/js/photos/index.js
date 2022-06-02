window.addEventListener('load', () => {
    for (let container of document.querySelectorAll('.img-container')) {
        container.addEventListener('mousedown', e => e.preventDefault() || false);
    }
})

window.addEventListener('scroll', () => {
    if (window.innerWidth > 1000) {
        for (let container of document.querySelectorAll('.img-container')) {
            let rect = container.getBoundingClientRect();

            if (rect.top / window.innerHeight < 0.2 && rect.bottom / window.innerHeight > 0.15) {
                container.focus({'preventScroll': true});
            } else {
                container.blur();
            }
        }
    }
})
