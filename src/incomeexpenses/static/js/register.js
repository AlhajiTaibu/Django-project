const usernameField = document.querySelector('#usernameField');
const feedBackField = document.querySelector('.invalid-feedback');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const submitBtn = document.querySelector('#submit-btn')

usernameField.addEventListener('keyup', (e) => {
      const usernameVal = e.target.value;
      usernameSuccessOutput.textContent= 'Checking' + usernameVal;
      usernameSuccessOutput.style.display='block';
      usernameField.classList.remove('is-invalid');
      feedBackField.style.display='none';
      if(usernameVal.length>0){
        fetch('/authentication/validate-username',{
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
      }).then(res=>res.json()).then((data)=>{
        console.log('data', data);
        usernameSuccessOutput.style.display='none';
        if(data.username_error){
            submitBtn.disabled= true
            usernameField.classList.add('is-invalid');
            feedBackField.style.display='block';
            feedBackField.innerHTML= '<p>'+data.username_error+'</p>';
        }else{
            submitBtn.removeAttribute('disabled')
        }
      });
      }


})


const emailField = document.querySelector('#emailField');
const emailfeedBack = document.querySelector('.emailfeedBackArea');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');
emailField.addEventListener('keyup',(e)=>{
      const emailVal = e.target.value;
      emailField.classList.remove('is-invalid');
      emailSuccessOutput.textContent= 'Checking '+ emailVal;
      emailSuccessOutput.style.display = 'block'
      emailfeedBack.style.display='none';
      if(emailVal.length>0){
        fetch('/authentication/validate-email',{
            body: JSON.stringify({email: emailVal}),
            method: "POST",
      }).then(res=>res.json()).then((data)=>{
        console.log('data', data);
        emailSuccessOutput.style.display = 'none'
        if(data.email_error){
            submitBtn.disabled= true
            emailField.classList.add('is-invalid');
            emailfeedBack.style.display='block';
            emailfeedBack.innerHTML= '<p>'+data.email_error+'</p>';
        }else{
            submitBtn.removeAttribute('disabled')
        }
      });
      }



});


const showPasswordToggle = document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector('#passwordField');

const handleToggleInput = (e) => {
        if(showPasswordToggle.textContent==='SHOW'){
            showPasswordToggle.textContent='HIDE';
            passwordField.setAttribute("type", "text");

        }else{
             showPasswordToggle.textContent='SHOW';
             passwordField.setAttribute("type","password");
        }
};

    showPasswordToggle.addEventListener('click', handleToggleInput);