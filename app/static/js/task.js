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

            form.reset()
            $('.projectSelect').val(null).trigger('change');
            
        }
        else{
            throw data.message
        }
    })
    .catch(err =>{
        alert(err)
    })
})


function loadProject() {
    fetch('/project/getAllNames')
        .then(res => res.json())
        .then(response => {

            if (response.status == "success") {

                const data = response.data

                $('.projectSelect').select2({
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
    loadProject()

    $('#taskTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/task/getAll",
            "type": "GET",
            "dataSrc": 'data'
        },
        "columns": [
            {"data": "name", "defaultContent": "N/A"},
            {"data": "description", "defaultContent": "N/A"},
            {"data": "user", "defaultContent": "N/A"},
            {"data": "project", "defaultContent": "N/A"},
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
                              <a class="dropdown-item edit-btn" href="javascript:void(0);" data-id="${data}"><i class="bi bi-pencil me-1"></i>Edit</a>
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


