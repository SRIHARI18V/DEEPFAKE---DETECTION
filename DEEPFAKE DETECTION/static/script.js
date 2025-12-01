async function uploadImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    if (!file) {
      alert('Please upload an image.');
      return;
    }
  
    const formData = new FormData();
    formData.append('image', file);
  
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData,
    });
  
    if (response.ok) {
      const result = await response.json();
      document.getElementById('result').innerText = `Prediction: ${result.label}`;
    } else {
      const error = await response.json();
      document.getElementById('result').innerText = `Error: ${error.error}`;
    }
  }
  