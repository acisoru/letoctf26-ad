const url = document.location.toString().split('/').slice(0, 3).join('/');
const backend = new BackendAPI(url);

const username = document.getElementById('username');

backend.user().then((data) => {
    username.textContent = data.username
}).catch((error) => {console.log(error)});

const info = document.getElementById('infoBlock');

backend.info().then((data) => {
    console.log(data)
    if (data) {
        data = data[0];
    }
    if (!data.fio || !data.passport) {
        info.textContent = 'Your information is empty.';
    } else {
        info.innerHTML = `Full name: <b>${data.fio}</b> <br><br> Passport: <b>${data.passport}</b> <br><br> Approved: <b>${data.approved}</b>`;
    }
})

const codeField = document.getElementById("codeField");

backend.recoveryCode().then((data) => {
    var code = data.code;
    codeField.textContent = code;
})

const requestButton = document.getElementById('requestButton');
const popupBackground = document.getElementById('popupBackground');
const closePopupButton = document.getElementById('closePopupButton');

requestButton.addEventListener('click', () => {
    popupBackground.style.display = 'block';
});

closePopupButton.addEventListener('click', () => {
    popupBackground.style.display = 'none';
});

const codeButton = document.getElementById('codeButton');
const popupBackgroundCode = document.getElementById('popupBackgroundCode');
const closePopupButtonCode = document.getElementById('closePopupButtonCode');

codeButton.addEventListener('click', () => {
    popupBackgroundCode.style.display = 'block';
});

closePopupButtonCode.addEventListener('click', () => {
    popupBackgroundCode.style.display = 'none';
});

const submitRequest = document.getElementById('submitRequest');

submitRequest.addEventListener('click', () => {
  let fio = document.getElementById('fio').value;
  let passport = document.getElementById('passport').value;
  backend.sendRequest(fio, passport)
    .then(() => {
      alert("Request sent");
      document.location = "/home";
    })
    .catch((error) => {
      alert(error);
    });
});