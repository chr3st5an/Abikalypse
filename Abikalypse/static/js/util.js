console.log("%cAbikalypse", "color:red; font-size:4.5em;");
console.log("Warum lieben Frauen objektorientierte Männer?");
console.log("- Weil sie Klasse haben");


/**
 * Prevents the context menu when an image is selected
 */
const preventRightClickOnImages = () => {
    for (let element of document.getElementsByTagName('img')) {
        element.addEventListener('contextmenu', e => {
            e.preventDefault();
        }, false);

        element.addEventListener('dragstart', e => {
            e.preventDefault();
        }, false);
    }
}
