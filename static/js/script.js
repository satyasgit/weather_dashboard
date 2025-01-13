document.getElementById('weatherForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const cityInput = document.getElementById('cityInput');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('errorMessage');
    const weatherResults = document.getElementById('weatherResults');
    const cityName = document.getElementById('cityName');
    const forecastContainer = document.getElementById('forecastContainer');
    
    // Form validation
    if (!cityInput.value.trim()) {
        errorMessage.textContent = 'Please enter a city name';
        errorMessage.classList.remove('d-none');
        return;
    }
    
    // Reset previous results
    errorMessage.classList.add('d-none');
    weatherResults.classList.add('d-none');
    loading.classList.remove('d-none');
    
    try {
        const formData = new FormData();
        formData.append('city', cityInput.value.trim());
        
        console.log('Fetching weather data for:', cityInput.value);
        
        const response = await fetch('/get_weather', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
            },
            body: formData
        });
        
        const data = await response.json();
        console.log('Weather data received:', data);
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch weather data');
        }
        
        // Display results with animation
        cityName.textContent = `${data.city}, ${data.country}`;
        forecastContainer.innerHTML = data.forecasts.map((forecast, index) => `
            <div class="col-md-6 col-lg-3 mb-4">
                <div class="weather-card p-3 text-center fade-in" style="animation-delay: ${index * 0.1}s">
                    <h5 class="mb-3">${forecast.date}</h5>
                    <img src="https://openweathermap.org/img/wn/${forecast.icon}@2x.png" 
                         alt="${forecast.description}" 
                         class="weather-icon mb-2">
                    <div class="temperature mb-2">${forecast.temp}°C</div>
                    <div class="feels-like mb-2">Feels like: ${forecast.feels_like}°C</div>
                    <div class="humidity mb-2">Humidity: ${forecast.humidity}%</div>
                    <div class="description">${forecast.description}</div>
                </div>
            </div>
        `).join('');
        
        weatherResults.classList.remove('d-none');
        cityInput.value = ''; // Clear input after successful search
        
    } catch (error) {
        console.error('Error:', error);
        errorMessage.textContent = error.message;
        errorMessage.classList.remove('d-none');
    } finally {
        loading.classList.add('d-none');
    }
});
