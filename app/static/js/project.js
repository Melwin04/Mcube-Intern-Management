const form = document.getElementById("projectForm")

form.addEventListener("submit", async (e) => {
    e.preventDefault()
    const formData = new FormData(form)
    const data = Object.fromEntries(formData)

    fetch("/project/new" , {
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

            form.reset ()
        }
        else{
            throw data.message
        }
    })
    .catch(err =>{
        alert(err)
    })
})


$('#projectTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/project/getAll",
            "type": "GET",
            "dataSrc": 'data'
        },
        "columns": [
            {"data": "name", "defaultContent": "N/A"},
            {"data": "description", "defaultContent": "N/A"},
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