import {fetchApiGet, fetchApiPost} from "./data_manager.js";
import {clearValue, setDisplay, clearTextContent} from "./utils.js";

// REGISTER

const regModal = document.getElementById("regModal")
const regMenuBtn = document.getElementById("bt_register")
const closeModalBtn = document.getElementById("closeRegModal")
const regUsernameInput = document.querySelector("#regUsername")
const regUsernameInputErrors = document.querySelector("#regUsernameErrors")
const regPasswordInput = document.querySelector("#regPassword")
const regPasswordInputErrors = document.querySelector("#regPasswordErrors")
const regButton = document.querySelector("#regButton")

if (regMenuBtn){
    regMenuBtn.addEventListener('click', () => regModal.style.display = "block")
    closeModalBtn.addEventListener('click', () => regModal.style.display = "none")
    regButton.addEventListener('click', () => {
        let cond1 = regUsernameInputErrors.textContent.length === 0 && regUsernameInput.value.length > 0
        let cond2 = regPasswordInputErrors.textContent.length === 0 && regPasswordInput.value.length > 0
        if (cond1 && cond2) {
            fetchApiPost("/register", clearInputsAfterRegister, {
                    username: regUsernameInput.value,
                    password: regPasswordInput.value
            })
        } else {
            alert("Invalid data provided!")
        }
    })

    regUsernameInput.addEventListener('input', e => {
        checkLength(e.target, 5, regUsernameInputErrors)
        findUser(e.target, regUsernameInputErrors, `${e.target.value} already exists`, "")
    })

    regPasswordInput.addEventListener('input', e => checkLength(e.target, 8, regPasswordInputErrors))
}

const clearInputsAfterRegister = () => {
    let userName = regUsernameInput.value
    clearValue(regUsernameInput, regPasswordInput)
    setDisplay("none", regModal)
    alert(`Registration successful! You can now log in ${userName}!`)
}

// LOGIN / LOGOUT

const loginMenuBtn = document.querySelector("#bt_login")
const loginModal = document.querySelector("#loginModal")
const closeLoginModalBtn = document.querySelector("#closeLoginModal")
const loginUsernameInput = document.querySelector("#logUsername")
const loginUsernameError = document.querySelector("#logUsernameErrors")
const loginPasswordInput = document.querySelector("#logPassword")
const loginPasswordError = document.querySelector("#logPasswordErrors")
const loginButton = document.querySelector("#logButton")
const logoutButton = document.querySelector("#bt_logout")

if (loginMenuBtn){
    loginMenuBtn.addEventListener("click", () => loginModal.style.display = "block")
    closeLoginModalBtn.addEventListener("click", () => loginModal.style.display = "none")

    loginButton.addEventListener("click", () => {
        let cond1 = loginUsernameInput.value.length > 0 && loginUsernameError.textContent.length === 0
        let cond2 = loginPasswordInput.value.length > 0 && loginPasswordError.textContent.length === 0

        if (cond1 && cond2) {
            fetchApiPost("/login", checkIfSuccessfullyLoggedIn, {
                    username: loginUsernameInput.value,
                    password: loginPasswordInput.value
                })
        }
    })

    loginUsernameInput.addEventListener("input", e => {
        checkLength(e.target, 5, loginUsernameError)
        findUser(e.target, loginUsernameError, "", `Username "${e.target.value}" not found`)
    })

    loginPasswordInput.addEventListener("input", e => checkLength(e.target, 8, loginPasswordError))
}
else {
    logoutButton.addEventListener("click", () => {
        fetchApiPost("/logout", checkIfSuccessfullyLoggedOut)
    })
}

// HELPER FUNCTIONS

const checkLength = (field, length, errorsContainer) => {
    if (field.value.length < length && field.value.length !== 0) {
        errorsContainer.textContent = `This field needs to be at least ${length} characters long`
    } else {
        clearTextContent(errorsContainer)
    }
}

const findUser = (inputContainer, errorContainer, messageFound, messageNotFound) => {
    const _findUserCallback = data => {
        if (data && data[0].username){
            errorContainer.textContent = messageFound
        } else {
            errorContainer.textContent = messageNotFound
        }
    }
    if (errorContainer.textContent.length === 0 && inputContainer.value.length > 0) {
        fetchApiGet(`/user/${inputContainer.value}`, _findUserCallback)
    }

}

const checkIfSuccessfullyLoggedIn = data => {
    if (data.logged){
        alert("Successfully logged in!")
        window.location.reload()
    } else {
        loginPasswordError.textContent = "Wrong password"
    }
}

const checkIfSuccessfullyLoggedOut = data => {
    if (data.loggedOut){
        alert("Logged out!")
        window.location.reload()
    } else {
        alert("Something went wrong, you may not be logged in")
    }
}