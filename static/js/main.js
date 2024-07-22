window.onload = function () {
    const clickableDiv = document.getElementsByClassName('div-1')[0];
    const targetDiv = document.getElementsByClassName('target-1')[0];
    if (clickableDiv) {
        clickableDiv.addEventListener('click', function () {
            targetDiv.scrollIntoView({ behavior: 'smooth' });
        });
    }

    const clickableDiv2 = document.getElementsByClassName('div-2')[0];
    const targetDiv2 = document.getElementsByClassName('target-2')[0];
    if (clickableDiv2) {
        clickableDiv2.addEventListener('click', function () {
            targetDiv2.scrollIntoView({ behavior: 'smooth' });
        });
    }
}

