document.getElementById("order-form").addEventListener("submit", function(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append("name", document.getElementById("name").value);
    formData.append("company", document.getElementById("company").value);
    formData.append("address", document.getElementById("address").value);
    formData.append("quantity", document.getElementById("quantity").value);
    formData.append("material", document.getElementById("material").value);
    
    let fileInput = document.getElementById("file-upload");
    if (fileInput.files.length === 0) {
        document.getElementById("order-status").innerText = "❌ Please select a file!";
        return;
    }
    formData.append("file", fileInput.files[0]);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);
        if (data.order_id) {
            document.getElementById("order-status").innerHTML = `✅ Order submitted successfully! Order ID: <strong>${data.order_id}</strong>`;
        } else if (data.error) {
            document.getElementById("order-status").innerHTML = `❌ Error: <strong>${data.error}</strong>`;
        } else {
            document.getElementById("order-status").innerText = "❌ Unexpected server response!";
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        document.getElementById("order-status").innerText = "❌ Order submission failed!";
    });
});