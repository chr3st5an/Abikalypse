const aspectRatio = 0.5369;
const imgElement  = document.createElement('img');


window.onload = () => {
    /* Add homepage group image */
    {
        let imgContainer = document.getElementById('home-img');

        imgElement.setAttribute('src', '/img/group_photos/gruppenfoto-letzter_tag.png');
        imgElement.setAttribute('width', String(window.innerWidth));
        imgElement.setAttribute('height', String(window.innerWidth * aspectRatio));
        imgElement.setAttribute('draggable', 'false');
        imgElement.setAttribute('alt', 'Cooles Gruppenfoto');

        imgContainer.appendChild(imgElement);
    }

    removeScriptTags();
}

window.onresize = () => {
    imgElement.setAttribute('width', window.innerWidth);
    imgElement.setAttribute('height', window.innerWidth * aspectRatio);
}
