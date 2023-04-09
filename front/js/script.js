const api = {
    base: "http://127.0.0.1:8000/api/sharer/v1"
}

const spinner = document.querySelector('.spinner-border');
const alert_message = document.querySelector('.alert-message');

function CreateAlert(message) {
    alert_message.parentElement.classList.remove('alert-success')
    alert_message.parentElement.classList.add('active', 'alert-danger')
    alert_message.innerHTML = `${message}`
    window.setTimeout(function () {
        if (alert_message.parentElement.classList.contains('alert-danger'))
            alert_message.parentElement.classList.remove('active', 'alert-danger')
    }, 6000);
}

function CreateAdvice(message) {
    alert_message.parentElement.classList.remove('alert-danger')
    alert_message.parentElement.classList.add('active', 'alert-success')
    alert_message.innerHTML = `<i class="fas fa-copy"></i> ${message}`
    window.setTimeout(function () {
        if (alert_message.parentElement.classList.contains('alert-success'))
            alert_message.parentElement.classList.remove('active', 'alert-success')
    }, 10000);
}

async function sendTextToApi(text_content) {
    spinner.classList.add('active')
    try {
        fetch(`${api.base}/upload/text`, {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "text": text_content
            })
        })
            .then(response => {
                return response.json();
            })
            .then(response => {
                spinner.classList.remove('active')
                if (response.temporary_url) {
                    CreateAdvice(`<b>Sucesso! </b> ${response.message}`)
                    CreateAdvice(response.temporary_url)
                }
                else {
                    CreateAlert(`<b>Erro! </b> ${response.message}`)
                    console.log(e)
                }
            });
    }
    catch (e) {
        CreateAlert(`<b>Erro! </b> ${e}`)
        console.log(e)
    }
}

async function sendFileToApiPost(file, url, fields) {
    // implement
    spinner.classList.remove('active')
}

async function sendFileToApiGet(file) {
    spinner.classList.add('active')

    try {
        fetch(`${api.base}/upload/file`, {
            method: "get",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                return response.json();
            })
            .then(response => {
                console.log(response)
                if (response.url) {
                    sendFileToApiPost(file, response.url, response.fields)
                }
                else {
                    CreateAlert(`<b>Erro! </b> ${response.message}`)
                    console.log(e)
                }
            });
    }
    catch (e) {
        CreateAlert(`<b>Erro! </b> ${e}`)
        console.log(e)
    }
}

async function GetInfo(text_content, uploaded_file) {
    if (!(text_content || uploaded_file)) {
        CreateAlert(`<b>Error!</b> Enter a text content or upload some file at least`)
        return
    }
    if (text_content) {
        sendTextToApi(text_content)
    }
    else {
        console.log(uploaded_file)
        sendFileToApiGet(uploaded_file)
    }
    return
}