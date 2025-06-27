const assignForm = document.getElementById("assignForm");

assignForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(assignForm);
    const data = Object.fromEntries(formData);

    fetch("/assignProject/new", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert(data.message);
                assignForm.reset();

                $('.taskSelect').val(null).trigger('change');
                $('.userSelect').val(null).trigger('change');
                $('#assignTable').DataTable().ajax.reload();
            } else {
                throw data.message;
            }
        })
        .catch(err => {
            alert(err);
        });
});


function loadUsers() {
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

function loadTasks() {
    fetch('/task/getAllNames')
        .then(res => res.json())
        .then(response => {
            if (response.status === "success") {
                $('.taskSelect').select2({
                    dropdownParent: $('#addTagModal'),
                    data: response.data
                });
            }
        })
        .catch(err => alert(err));
}

$(document).ready(function () {
    loadUsers();
    loadTasks();

    $('#assignTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/assignProject/getAll",
            "type": "GET",
            "dataSrc": 'data'
        },
        "columns": [
            { "data": "user", "defaultContent": "N/A" },
            { "data": "project", "defaultContent": "N/A" },
            { "data": "task", "defaultContent": "N/A" },
            { "data": "status", "defaultContent": "N/A" },
            { "data": "deadline", "defaultContent": "N/A" },
            { "data": "addedTime", "defaultContent": "N/A" },
            { "data": "updatedTime", "defaultContent": "N/A" },
            {
                "data": "id",
                "render": function (data, type, row) {
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
    });
});
