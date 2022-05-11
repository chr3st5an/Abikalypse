window.onload = () => { preventRightClickOnImages(); removeScriptTags() };

window.onresize = () => {
    let size = document.getElementsByClassName('survivor-card')[0].offsetWidth - 40;

    for (let imgElement of document.querySelectorAll('.wrapper img')) {
        imgElement.setAttribute('width', String(size));
        imgElement.setAttribute('height', String(size));
    }
}