const form = document.getElementById("taskForm")

form.addEventListener("submit", async (e) => {
    e.preventDefault()
    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    fetch("/task/new" , {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data =>{
        if (data.status == "success"){
            alert(data.message)
        }
        else{
            throw data.message
        }
    })
    .catch(err =>{
        alert(err)
    })
})