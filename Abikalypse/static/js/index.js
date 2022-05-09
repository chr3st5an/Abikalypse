window.onload = () => {
    {
        const photoFormat = 0.5369;

        let imgContainer = document.getElementById('home-img');
        let width        = window.innerWidth;
        let height       = width * photoFormat;

        imgContainer.innerHTML = `
            <img src="/img/group_photos/gruppenfoto-letzter_tag.png" width='${width}' height='${height}'/>
        `;
    }

    removeScriptTags();
}