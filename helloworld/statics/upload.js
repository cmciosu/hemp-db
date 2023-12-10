function uploadExcel() {
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);

    // Backend endpoint to handle file uploads
    const endpoint = '/api/upload-excel/';

    fetch(endpoint, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Upload successful:', data);
        // Can add further actions here, like updating the UI or displaying a success message
    })
    .catch(error => {
        console.error('Error uploading file:', error);
        // Handle errors, display an error message, etc.
    });
}
