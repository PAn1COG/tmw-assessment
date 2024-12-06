document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        // formData object
        const formData = new FormData(form);
        // upload
        fetch('http://127.0.0.1:8000/upload/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.task_id) {
                alert(`This is your task ID: ${data.task_id}, Async execution has started. You can copy and paste this to check the status.`);
            } else {
                alert('Failed to upload file. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            alert('An error occurred while uploading the file. Please try again.');
        });
    });
});
