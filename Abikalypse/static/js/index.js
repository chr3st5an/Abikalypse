window.onload = () => {
    document.querySelectorAll('#home-img img').forEach(img => {
        img.setAttribute('width', window.innerWidth);
    });
}

window.onresize = () => {
    document.querySelectorAll('#home-img img').forEach(img => {
        img.setAttribute('width', window.innerWidth);
    });
}
