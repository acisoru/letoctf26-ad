const url = document.location.toString().split('/').slice(0, 3).join('/');
const backend = new BackendAPI(url);

const signUpButton = document.getElementById('signUpButton');
const popupBackgroundSignup = document.getElementById('popupBackgroundSignup');
const closePopupButtonSignup = document.getElementById('closePopupButtonSignup');

signUpButton.addEventListener('click', () => {
  popupBackgroundSignup.style.display = 'block';
});

closePopupButtonSignup.addEventListener('click', () => {
  popupBackgroundSignup.style.display = 'none';
});

const logInButton = document.getElementById('logInButton');
const popupBackgroundLogin = document.getElementById('popupBackgroundLogin');
const closePopupButtonLogin = document.getElementById('closePopupButtonLogin');

logInButton.addEventListener('click', () => {
  popupBackgroundLogin.style.display = 'block';
});

closePopupButtonLogin.addEventListener('click', () => {
  popupBackgroundLogin.style.display = 'none';
});

const resetButton = document.getElementById('resetButton');
const popupBackgroundReset = document.getElementById('popupBackgroundReset');
const closePopupButtonReset = document.getElementById('closePopupButtonReset');

resetButton.addEventListener('click', () => {
  popupBackgroundReset.style.display = 'block';
});

closePopupButtonReset.addEventListener('click', () => {
  popupBackgroundReset.style.display = 'none';
});


const submitSignup = document.getElementById('submitSignup');

submitSignup.addEventListener('click', () => {
  let username = document.getElementById('usernameSignup').value;
  let email = document.getElementById('emailSignup').value;
  let password1 = document.getElementById('password1Signup').value;
  let password2 = document.getElementById('password2Signup').value;
  if (password1 !== password2) {
    alert('Passwords do not match');
    return;
  }
  backend.register(username, email, password1)
    .then(() => {
      alert("Success");
    })
    .catch((error) => {
      alert("User exists");
    });
});

const submitLogin = document.getElementById('submitLogin');

submitLogin.addEventListener('click', () => {
  let username = document.getElementById('usernameLogin').value;
  let password = document.getElementById('passwordLogin').value;
  backend.login(username, password)
    .then(() => {
      document.location = "/home";
    })
    .catch((error) => {
      alert("Wrong credentials");
    });
});

const submitReset = document.getElementById('submitReset');

submitReset.addEventListener('click', () => {
  let code = document.getElementById('codeReset').value;
  let password = document.getElementById('passwordReset').value;
  backend.resetPassword(code, password)
    .then(() => {
      alert('Success');
      document.location = "/home";
    })
    .catch((error) => {
      alert("Wrong data");
    });
});