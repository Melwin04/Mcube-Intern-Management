/* ================ Add Intern ================ */

const form = document.getElementById("internForm")

form.addEventListener("submit", async (e) => {
    e.preventDefault()


    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    const selectedSkills = $('#skills').select2('data');

    let skillList = []
    selectedSkills.forEach(skill => {
        skillList.push(skill.text)
    });

    data['skills'] = skillList

    let id = document.getElementById("internId").value
    
    if (id) {
        fetch("/intern/update?id="+id, {
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
        fetch("/intern/new", {
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

    
/* ================ Load User & Initialize Select 2 ================ */


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

/* ================ Get All Values ================ */

$(document).ready(function () {

    loadUser()

    $('#skills').select2({
        tags: true,
        dropdownParent: $('#addTagModal')
    })

    $('#internTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/intern/getAll",
            "type": "GET",
            "dataSrc": 'data'
        },
        "columns": [
            {"data": "user", "defaultContent": "N/A"},
            {"data": "skills", "defaultContent": "N/A"},
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
                              <a class="dropdown-item edit-btn" href="javascript:void(0);" data-id="${data}" data-bs-toggle="modal" data-bs-target="#addTagModal"><i class="bi bi-pencil me-1"></i>Edit</a>
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
    
    document.querySelector("#internTable tbody").addEventListener('click', (event)=>{
    if (event.target.classList.contains('edit-btn')) {
        let id = event.target.getAttribute('data-id')

        fetch('/intern/get?id='+id)
        .then(res => res.json())
        .then(response =>{
            const data = response.data
            if (response.status == "success"){
                
                // document.getElementById("user").value = data.name
                // document.getElementById("skills").value = data.email
                
                document.getElementById("internId").value = data.id
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
});


document.querySelector("#internTable tbody").addEventListener('click', (event)=>{
    if (event.target.classList.contains('delete-btn')) {
        let id = event.target.getAttribute('data-id')
~
        fetch('/intern/delete?id='+id, {
            method: "DELETE"
        })
        .then(res => res.json())
        .then(response =>{
            if (response.status == "success"){
                
                alert(response.message)

                location.reload()
            }
            else{
                throw response.message
            }
        })
        .catch(err =>{
            alert(err)
        })
    }
})

