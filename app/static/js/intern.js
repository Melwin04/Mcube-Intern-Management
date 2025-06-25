const form = document.getElementById("internForm")

form.addEventListener("submit", async (e) => {
    e.preventDefault()


    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    fetch("/intern/new", {
        method:"POST",
        headers: {
             "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data =>{
        if (data.status == "success") {
            alert(data.message)
            form.reset()
        }
        else{
            throw data.message
        }
    })
    .catch(err =>{
        alert(err)
    })
})
