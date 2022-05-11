window.onload = () => {
    /* Load group photos */
    {
        for (let photo of document.querySelectorAll('.group-photos img')) {
            photo.setAttribute('width', String(window.innerWidth / 1.2));
            photo.setAttribute('height', 'auto');
        }
    }
}

window.onresize = () => {
    /* Resize group photos */
    {
        const groupPhotos = document.querySelectorAll('.group-photos img');

        groupPhotos.forEach(img => {
            img.setAttribute('width', String(window.innerWidth / 1.2));
        })
    }
}
