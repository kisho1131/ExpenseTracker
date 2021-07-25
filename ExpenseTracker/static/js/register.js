const usernameField = document.querySelector('#username')
const feedBackArea = document.querySelector('.invalid_feedback')
const emailFeedBackArea = document.querySelector('.invalid_emailFeedBack')
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput")
const emailField = document.querySelector('#email')
const emailSuccessOutput = document.querySelector('.emailSuccessOutput')
const passwordField = document.querySelector("#password")
const showPasswordToggle = document.querySelector(".showPasswordToggle")
const submitBtn = document.querySelector(".submit-btn")


const handleToggleInput = (e)=>{
    if(showPasswordToggle.textContent === "SHOW PASSWORD"){
        passwordField.setAttribute("type", "text")
        showPasswordToggle.textContent = "HIDE PASSWORD"
    }else{
        showPasswordToggle.textContent = "SHOW PASSWORD"
        passwordField.setAttribute("type", "password")
    }
}
showPasswordToggle.addEventListener('click', handleToggleInput)



// Event Listner for Validating the Email ID 
emailField.addEventListener("keyup", (e) =>{
    const emailVal = e.target.value
    emailSuccessOutput.style.display = "block"
    emailSuccessOutput.textContent = `Checking ${emailVal}`

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";
    if(emailVal.length > 0){
        fetch("/authentication/validate-email", {
            // convert the javascript object into the json object
            body:JSON.stringify({email : emailVal}),
                method : "POST",
        }).then(res => res.json()).then((data)=>{
            console.log('data', data)
            emailSuccessOutput.style.display = "none"
            if(data.email_error){
                // submitBtn.setAttribute('disabled', "disabled")
                submitBtn.disabled = true
                emailField.classList.add("is-invalid")
                emailFeedBackArea.style.display = "block"
                emailFeedBackArea.innerHTML = `<p> ${data.email_error}</p>`
            }else{
                submitBtn.removeAttribute("disabled")
            }
        });
    }
})


// Event Listener for Validiting the User name 
usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value
    usernameSuccessOutput.style.display = "block"
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";
    if(usernameVal.length > 0){
        fetch("/authentication/validate-username", {
            // convert the javascript object into the json object
            body:JSON.stringify({username : usernameVal}),
                method : "POST",
        }).then(res => res.json()).then((data)=>{
            console.log('data', data)
            usernameSuccessOutput.style.display = "none"
            if(data.username_error){
                submitBtn.disabled = true
                usernameField.classList.add("is-invalid")
                feedBackArea.style.display = "block"
                feedBackArea.innerHTML = `<p> ${data.username_error}</p>`
            }else{
                submitBtn.removeAttribute("disabled")
            }
        });
    }
})
