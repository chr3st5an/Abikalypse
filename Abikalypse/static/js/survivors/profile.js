window.onload = () => {
    preventRightClickOnImages();

    /* Verify user input */
    {
        let form = document.getElementsByTagName("form")[0];

        form.onsubmit = e => {
            let input = document.getElementsByTagName("input");

            let author  = input[0].value;
            let content = input[1].value;

            e.preventDefault();

            if (!(1 < author.length && author.length < 17) || !(3 < content.length && content.length < 129)) {
                if (!(3 < author.length && author.length < 16)) {
                    input[0].focus();
                } else {
                    input[1].focus();
                }

                return false;
            }

            input[0].value = input[1].value = '';

            return postData(author, content);
        }
    }
}

const postData = (...args) => {
    let request = new XMLHttpRequest();

    request.open('POST', location.href, true);
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    request.onreadystatechange = () => {
        if (request.readyState == 4) {
            switch (request.status) {
                case 201:
                    createResource(request.responseText);
                    break;
                case 400:
                    showErrToast('Die übertragenen Daten sind falsch!');
                    break;
                default:
                    showErrToast('Da stimmt etwas nicht!');
            }
        }
    }

    request.send(`username=${args[0]}&content=${args[1]}`);
};

const createResource = response => {
    let guestBook  = document.querySelector('#guest-book section div');
    let noComments = document.getElementById('no-comments-yet');

    if (noComments) noComments.remove();

    guestBook.innerHTML += response;
}

const showErrToast = (message, hideAfterMS = 3000) => {
    let toast = document.getElementsByClassName("toast")[0];
    let text  = document.createTextNode(message);

    toast.appendChild(text);
    toast.setAttribute('visibility', 'visible');

    setTimeout(() => {
        toast.setAttribute('visibility', 'hidden');
        text.remove();
    }, hideAfterMS);
}
