window.onload = () => {
    preventRightClickOnImages();

    let form = document.getElementsByTagName("form")[0];

    form.onsubmit = e => {
        let input = document.getElementsByTagName("input");

        let author  = input[0].value;
        let content = input[1].value;

        if (!(3 < author.length && author.length < 16) || !(4 < content.length && content.length < 128)) {
            e.preventDefault();

            if (!(3 < author.length && author.length < 16)) {
                input[0].focus();
            } else {
                input[1].focus();
            }

            return false;
        }

        return true;
    }
}