const form = document.getElementById("userForm")

form.addEventListener("submit", async(e)=>{
    e.preventDefault()
    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    let id = document.getElementById("userId").value
    
    if (id) {
        fetch("/user/update?id="+id, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data =>{
            if (data.status == "success") {
                alert(data.message)
                
                location.reload()
            }
            else{
                throw data.message
            }
        })
        .catch(err =>{
            alert(err)
        })
    }else{
        fetch("/user/new", {
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
                form.reset()
            }
            else{
                throw data.message
            }
        })
        .catch(err =>{
            alert(err)
        })
    }
})


function loadUser() {
    fetch('/user/getAllNames')
        .then(res => res.json())
        .then(response => {

            if (response.status == "success") {

                const data = response.data

                $('.userSelect').select2({
                    dropdownParent: $('#addTagModal'),
                    data: data
                });

            }
            else {
                throw err
            }
        })
        .catch(err => {
            alert(err)
        })
}




$(document).ready(function() {

    loadUser()

    $('#username').select2({
        tags: true,
        dropdownParent: $('#addTagModal')
    })

    $('#userTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/user/getAll",
            "type": "GET",
            "dataSrc": 'data'
        },
        "columns": [
            {"data": "name", "defaultContent": "N/A"},
            {"data": "email", "defaultContent": "N/A"},
            {"data": "password", "defaultContent": "N/A"},
            {"data": "mobileNumber", "defaultContent": "N/A"},
            {"data": "addedTime", "defaultContent": "N/A"},
            {"data": "updatedTime", "defaultContent": "N/A"},
            {
                "data": "id",
                "render": function(data, type, row) {
                    return `
                        <div class="dropdown">
                            <button type="button" class="btn p-0 dropdown hide-arrow" data-bs-toggle="dropdown">
                              <i class="bi bi-three-dots-vertical"></i>
                            </button>
                            <div class="dropdown-menu">
                              <a class="dropdown-item edit-btn" href="javascript:void(0);" data-id="${data}"  data-bs-toggle="modal" data-bs-target="#addTagModal"><i class="bi bi-pencil me-1"></i>Edit</a>
                              <a class="dropdown-item delete-btn" href="javascript:void(0);" data-id="${data}"><i class="bi bi-trash3-fill me-1"></i>Delete</a>
                            </div>
                        </div>
                    `;
                },
                "orderable": false
            }
        ],
        "order": true,
        "searching": true,
        "autoWidth": false,
        "paging": true
    })
});


document.querySelector("#userTable tbody").addEventListener('click', (event)=>{
    if (event.target.classList.contains('edit-btn')) {
        let id = event.target.getAttribute('data-id')

        fetch('/user/get?id='+id)
        .then(res => res.json())
        .then(response =>{
            const data = response.data
            if (response.status == "success"){
                
                document.getElementById("name").value = data.name
                document.getElementById("email").value = data.email
                document.getElementById("password").value = data.password
                document.getElementById("mobileNumber").value = data.mobileNumber
                
                document.getElementById("userId").value = data.id
            }
            else{
                throw data.message
            }
        })
        .catch(err =>{
            alert(err)
        })
    }
})


document.querySelector("#userTable tbody").addEventListener('click', (event)=>{
    if (event.target.classList.contains('delete-btn')) {
        let id = event.target.getAttribute('data-id')

        fetch('/user/delete?id='+id, {
            method: "DELETE"
        })
        .then(res => res.json())
        .then(response =>{
            if (response.status == "success"){
                
                alert(response.message)

                location.reload()
            }
            else{
                throw data.message
            }
        })
        .catch(err =>{
            alert(err)
        })
    }
})