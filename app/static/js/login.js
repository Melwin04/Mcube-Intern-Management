const form = document.getElementById("loginForm")

form.addEventListener("submit", async (e) => {
    e.preventDefault()

    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data =>{
        if (data.status == "success") {
            alert(data.message)
            
            window.location.href = "/dashboard"
        }
        else{
            throw data.message
        }
    })
    .catch(err =>{
        alert(err)
    })
})