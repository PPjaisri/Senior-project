document.addEventListener('DOMContentLoaded', passData, false)

function fetchdata(input) {
    alert("Url is : " + input.value)
}

function passData() {
    document.getElementById('submit').addEventListener('click', function () {
        const url = document.getElementById('content')
        fetchdata(url)
    })
}