function truncateText(element, maxLength) {
    // var element = document.querySelector(selector),
    var truncated = element.innerText;

    if (truncated.length > maxLength) {
        truncated = truncated.substr(0,maxLength) + '...';
    }
    return truncated;
}

// document.querySelector('.service .iconbox-service .contents p').innerText = truncateText('.service .iconbox-service .contents p', 150);

var forCutting = document.querySelectorAll('.service .iconbox-service .contents p');

for (i = 0; i < forCutting.length; i++) {
	forCutting[i].innerText = truncateText(forCutting[i], 150);
}