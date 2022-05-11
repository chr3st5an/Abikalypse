window.onload = () => {
    preventRightClickOnImages();
    removeScriptTags();

    /* Verify user input */
    {
        let form = document.getElementsByTagName("form")[0];

        form.onsubmit = e => {
            let input = document.getElementsByTagName("input");

            let author  = input[0].value;
            let content = input[1].value;

            if (!(1 < author.length && author.length < 17) || !(3 < content.length && content.length < 129)) {
                e.preventDefault();

                if (!(3 < author.length && author.length < 16)) {
                    input[0].focus();
                } else {
                    input[1].focus();
                }

                try {
                    let toast = document.getElementsByClassName("toast")[0];

                    toast.style = 'visibility:visible';

                    setTimeout(() => toast.style = "", 3000);
                } catch (err) {}

                return false;
            }

            return true;
        }
    }
}

window.onresize = () => {
    let profileImg = document.querySelector('.card img');

    if (!profileImg) return null;

    let size = document.getElementsByClassName('card')[0].offsetWidth - 44;

    profileImg.setAttribute('width', String(size));
    profileImg.setAttribute('height', String(size));
}
