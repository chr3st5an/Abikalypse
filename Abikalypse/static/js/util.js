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

/**
 * Removes every script tag within the body tag
 */
const removeScriptTags = () => {
    for (let scriptTag of document.querySelectorAll('body script')) {
        scriptTag.remove();
    }
}

let navbarExpanded = false;

/**
 * Expand / collapse the navbar
 */
const navbarExpand = () => {
    const navbar = document.getElementsByClassName('hamburger')[0];
    let items    = Array.from(navbar.getElementsByTagName('li'));

    items.slice(1).forEach(i => {
        i.style = 'display:' + (navbarExpanded ? 'none' : 'block');
    });

    navbarExpanded = !navbarExpanded;
}
