function uploadImage() {
    const fileInput = document.getElementById("imageUpload");
    if (fileInput.files.length === 0) {
        alert("Please select an image.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    // Preview the image
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById("preview").src = e.target.result;
        document.getElementById("preview").style.display = "block";
    };
    reader.readAsDataURL(file);

    // Send image to FastAPI server
    fetch("http://127.0.0.1:8000/predict/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.predicted_label) {
            document.getElementById("result").innerText = "Predicted Sign: " + data.predicted_label;
        } else {
            document.getElementById("result").innerText = "Error: " + (data.error || "Could not predict.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error in prediction!";
    });
}
