document.addEventListener('DOMContentLoaded', passData, false)

function getdata(input) {
    alert("Url is : " + input.value);
}

async function sendData(url) {
    sessionStorage.setItem('fetch_url', url.value)
    chrome
}

function passData() {
    document.getElementById('submit').addEventListener('click', function () {
        const url = document.getElementById('url')
        getdata(url)
        sendData(url)
    })
}