// Intern Count
fetch("/dashboard/intern/count")
    .then(res => res.json())
    .then(data => {
        document.getElementById("internCount").innerText = data.count;
    })
    .catch(err => {
        document.getElementById("internCount").innerText = "Error";
    });

// Project Count
fetch("/dashboard/project/count")
    .then(res => res.json())
    .then(data => {
        document.getElementById("projectCount").innerText = data.count;
    })
    .catch(err => {
        document.getElementById("projectCount").innerText = "Error";
    });

// Task Count
fetch("/dashboard/task/count")
    .then(res => res.json())
    .then(data => {
        document.getElementById("taskCount").innerText = data.count;
    })
    .catch(err => {
        document.getElementById("taskCount").innerText = "Error";
    });
