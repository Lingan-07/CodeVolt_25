document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent form from submitting normally
  
    // Get input features
    const featuresInput = document.getElementById('features').value;
    const features = featuresInput.split(',').map(item => parseFloat(item.trim()));
  
    if (features.some(isNaN)) {
      alert("Please enter valid numerical values for all features.");
      return;
    }
  
    // Prepare data to send to FastAPI
    const requestData = {
      features: features
    };
  
    try {
      // Make POST request to the FastAPI backend
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });
  
      // Handle response
      if (!response.ok) {
        throw new Error('Prediction request failed');
      }
  
      const data = await response.json();
      document.getElementById('prediction-value').textContent = data.prediction;
    } catch (error) {
      alert('Error: ' + error.message);
    }
  });
  