window.onload = () => {
    for (let container of document.querySelectorAll('.img-container')) {
        let photo = container.getElementsByTagName('img')[0];

        photo.setAttribute('width', String(window.innerWidth / 1.2));
        photo.setAttribute('height', 'auto');

        container.addEventListener('mousedown', e => e.preventDefault() || false);
    }
}

window.onresize = () => {
    /* Resize photos */
    for (let photo of document.getElementsByTagName('img')) {
        photo.setAttribute('width', String(window.innerWidth / 1.2));
    }
}

window.onscroll = () => {
    if (window.innerWidth > 700) {
        for (let container of document.querySelectorAll('.img-container')) {
            let rect = container.getBoundingClientRect();

            if (rect.top / window.innerHeight < 0.15 && rect.bottom / window.innerHeight > 0.15) {
                container.focus({'preventScroll': true});
            } else {
                container.blur();
            }
        }
    }
}
