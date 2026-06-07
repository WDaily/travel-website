<script lang="js">
    let { form } = $props();
	
	let latitude;
	let longitude;
	let errorMessage = $state("");

	let responseText = $state("");
	let radius = $state("");
	let spot = $state("");
	let locationInput = $state("");
	let chooseOption = $state(false);
	let isLoading = $state(false);
	let requested = $state(false);

	function optionPicked(){
		chooseOption = !chooseOption;
	}
	
	function closeMessage(){
		errorMessage = "";
	}
	
	function location(){
		if(navigator.geolocation){
			navigator.geolocation.getCurrentPosition(successFunction, errorFunction);
		}else{
			errorMessage = "Geolocation not supported by your browser. Type your location instead";
		}
	}

	const successFunction = (positon) =>{

		latitude = position.coords.latitude;
		longitude = position.coords.longitude;
	};

	const errorFunction = (error) => {
		errorMessage = "Location error. Please Try Again In A few Minutes";
	}

	function retry(){
		requested = !requested;
	}
	async function recommend(e){
        e.preventDefault();

        isLoading = true;
        responseText = "";
        requested = true;

        if(!latitude && !longitude && !location){
        	errorMessage = "Please provide the location";
        	isLoading = false;
        	requested = false;
        	return
        }

        let userLocation;
        if(locationInput){
        	userLocation = locationInput;
        }else{
        	userLocation = "latitude: " + latitude + "longitude: " + longitide;
        }

        const locationData = {location: userLocation, area: radius, activity: spot};

        try {
             const response = await fetch("http://localhost:8080/recommend" , {
                method: "POST",
                headers:{"Content-Type" : "application/json"},
                body: JSON.stringify(locationData),
                credentials:"include"
            });

            const data = await response.json();

            if (!response.ok) {
                 throw new Error(`Server error: ${data.message}`);
             }

            responseText = data.text;

        } catch (error) {
            errorMessage += "Error: " + error.message;
        	requested = false;

        } finally {
            isLoading = false;
        }
    }

</script>

<div class="recommend-section">
	<div class="hero-header">
		<h1>Discover Your Next Adventure</h1>
		<p>Find the perfect travel recommendations tailored to your interests</p>
	</div>

	<div class="recommend-block">
		{#if responseText || isLoading}
			<div class="recommendations response-text">
				<div class="response-header">
					<h2>Your Personalized Recommendations</h2>
				</div>
				{#if isLoading}
					<div class="spinner"><span class="sr-only">Loading...</span></div>
					<p class="loading-text">Planning your journey...</p>
				{:else}
					<div class="recommendation-content">
						<p class="response-message">{responseText}</p>
						<div class="retry-section"><button onclick={retry} class="retry-button" type="button">Search Again</button></div>
					</div>
				{/if}
			</div>
		{/if}

		{#if errorMessage}
			<div class = "message-section" role="dialog" aria-modal="true">
				<div class = "message-block">
					<div class="error-header">Oops!</div>
					<p>{errorMessage}</p>
					<button class="close-button" onclick={closeMessage} aria-label="Close">Got it</button>
				</div>
			</div>
		{/if}

		{#if !requested}
		<form onsubmit={recommend} class="travel-form">
			<div class="form-section">
				<label for="options-block" class="section-label">Location</label>

				{#if !chooseOption}
					<div class="options-block">
						<button onclick={location} class="location-button" type="button">
							Use My Current Location
						</button>
						<button class="options-button" onclick={optionPicked} type="button">
							Type Location Instead
						</button>
					</div>

				{:else}
					<div class="options-block input-mode">
						<input 
							name="locationInput" 
							type="text" 
							id="locationInput" 
							bind:value={locationInput} 
							placeholder="e.g., city, country" 
							required
							class="form-input"
						/>
						<button class="options-button secondary" onclick={optionPicked} type="button">
							Use GPS Instead
						</button>
					</div>
				{/if}
			</div>

			<div class="form-section">
				<label for="spotValue" class="section-label">Distance</label>
				<div class="input-group">
					<input 
						name="radius" 
						type="number" 
						id="spotValue" 
						bind:value={radius} 
						placeholder="50" 
						required
						class="form-input"
						min="1"
					/>
					<span class="unit">km</span>
				</div>
			</div>

			<div class="form-section">
				<label for="spotText" class="section-label">Interest</label>
				<input 
					name="spot" 
					type="text" 
					id="spotText" 
					bind:value={spot} 
					placeholder="e.g., hotels, museums, game parks" 
					required
					class="form-input"
				/>
			</div>

			<button type="submit" class="submit-button">
				Get Recommendations
			</button>
		</form>
		{/if}
	</div>
</div>



<style>
:root {
	--primary-color: #2c7a7b;
	--primary-light: #4a9fa8;
	--accent-color: #0ab720;
	--error-color: maroon;
	--light-bg: #f0fdf4;
	--text-dark: #1f2937;
	--border-color: #e5e7eb;
	--shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.response-message{
	white-space:pre-line;
}
.recommend-section {
	display: grid;
	place-items: center;
	padding: 2rem 1rem;
	min-height: 100vh;
}

.hero-header {
	text-align: center;
	margin-bottom: 3rem;
	animation: slideDown 0.6s ease-out;
}

.hero-header h1 {
	font-size: 2.5rem;
	color: var(--primary-color);
	margin: 0 0 0.5rem 0;
	font-weight: 700;
	letter-spacing: -0.02em;
}

.hero-header p {
	font-size: 1.125rem;
	color: #6b7280;
	margin: 0;
}

.recommend-block {
	width: 100%;
	max-width: 600px;
}

.travel-form {
	background: white;
	border-radius: 16px;
	padding: 2rem;
	box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
	animation: slideUp 0.6s ease-out;
}

.form-section {
	margin-bottom: 2rem;
}

.form-section:last-of-type {
	margin-bottom: 2.5rem;
}

.section-label {
	display: block;
	font-size: 0.95rem;
	font-weight: 700;
	color: var(--text-dark);
	margin-bottom: 0.75rem;
	text-transform: capitalize;
}

.form-input {
	width: 100%;
	padding: 0.875rem 1rem;
	border: 2px solid var(--border-color);
	border-radius: 10px;
	font-size: 1rem;
	transition: all 0.3s ease;
	font-family: inherit;
}

.form-input:focus {
	outline: none;
	border-color: var(--primary-color);
	box-shadow: 0 0 0 3px rgba(44, 122, 123, 0.1);
}

.form-input::placeholder {
	color: #9ca3af;
}

.input-group {
	position: relative;
	display: flex;
	align-items: center;
}

.input-group .form-input {
	padding-right: 3.5rem;
}

.unit {
	position: absolute;
	right: 1rem;
	color: #6b7280;
	font-weight: 500;
	pointer-events: none;
}

.options-block {
	display: flex;
	gap: 0.75rem;
	flex-wrap: wrap;
}

.options-block.input-mode {
	flex-direction: column;
	gap: 0.5rem;
}

.location-button,
.options-button {
	flex: 1;
	min-width: 150px;
	padding: 0.875rem 1.25rem;
	border: 2px solid var(--primary-color);
	border-radius: 10px;
	background: white;
	color: var(--primary-color);
	font-size: 0.95rem;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.3s ease;
	font-family: inherit;
}

.location-button:hover,
.options-button:hover {
	background: var(--primary-color);
	color: white;
	transform: translateY(-2px);
	box-shadow: 0 4px 12px rgba(44, 122, 123, 0.25);
}

.options-button.secondary {
	border-color: var(--accent-color);
	color: var(--accent-color);
	flex: none;
	width: 100%;
}

.options-button.secondary:hover {
	background: var(--accent-color);
	color: white;
}

.submit-button {
	width: 100%;
	padding: 1rem 1.5rem;
	background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
	color: white;
	border: none;
	border-radius: 10px;
	font-size: 1.05rem;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.3s ease;
	font-family: inherit;
	text-transform: capitalize;
	letter-spacing: 0.5px;
	box-shadow: 0 4px 12px rgba(44, 122, 123, 0.2);
}

.submit-button:hover {
	transform: translateY(-2px);
	box-shadow: 0 6px 20px rgba(44, 122, 123, 0.3);
}

.submit-button:active {
	transform: translateY(0);
}

.response-text {
	background: white;
	border-radius: 16px;
	padding: 2rem;
	box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
	animation: slideUp 0.6s ease-out;
}

.response-header {
	border-bottom: 3px solid var(--primary-color);
	padding-bottom: 1rem;
	margin-bottom: 1.5rem;
}

.response-header h2 {
	font-size: 1.5rem;
	color: var(--primary-color);
	margin: 0;
}

.recommendation-content p {
	font-size: 1rem;
	line-height: 1.6;
	color: var(--text-dark);
	margin: 0 0 1.5rem 0;
}

.loading-text {
	text-align: center;
	color: #6b7280;
	margin-top: 1rem;
	font-weight: 500;
}

.retry-section {
	display: flex;
	justify-content: center;
	margin-top: 2rem;
}

.retry-button {
	padding: 0.875rem 1.75rem;
	background: var(--primary-color);
	color: white;
	border: none;
	border-radius: 10px;
	font-size: 0.95rem;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.3s ease;
	font-family: inherit;
}

.retry-button:hover {
	background: var(--primary-light);
	transform: translateY(-2px);
	box-shadow: 0 4px 12px rgba(44, 122, 123, 0.25);
}

.message-section {
	position: fixed;
	inset: 0;
	display: flex;
	justify-content: center;
	align-items: center;
	background: rgba(0, 0, 0, 0.4);
	z-index: 1000;
	animation: fadeIn 0.3s ease-out;
}

.message-block {
	background: white;
	color: var(--text-dark);
	padding: 1.5rem;
	border-radius: 12px;
	box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
	max-width: 90%;
	width: 420px;
	position: relative;
	animation: popIn 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.error-header {
	font-size: 1.25rem;
	font-weight: 700;
	color: var(--error-color);
	margin-bottom: 0.5rem;
}

.message-block p {
	margin: 0.75rem 0 1.5rem 0;
	font-size: 1rem;
	line-height: 1.5;
}

.close-button {
	width: 100%;
	padding: 0.75rem 1rem;
	border: none;
	background: var(--primary-color);
	color: white;
	border-radius: 8px;
	font-size: 0.95rem;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.3s ease;
	font-family: inherit;
}

.close-button:hover {
	background: var(--primary-light);
	transform: translateY(-1px);
}

.spinner {
	width: 40px;
	height: 40px;
	border: 4px solid var(--border-color);
	border-top-color: var(--primary-color);
	border-radius: 50%;
	animation: spin 1s linear infinite;
	margin: 1rem auto;
}

.sr-only {
	position: absolute;
	width: 1px;
	height: 1px;
	padding: 0;
	margin: -1px;
	overflow: hidden;
	clip: rect(0, 0, 0, 0);
	white-space: nowrap;
	border: 0;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

@keyframes slideDown {
	from {
		transform: translateY(-20px);
		opacity: 0;
	}
	to {
		transform: translateY(0);
		opacity: 1;
	}
}

@keyframes slideUp {
	from {
		transform: translateY(20px);
		opacity: 0;
	}
	to {
		transform: translateY(0);
		opacity: 1;
	}
}

@keyframes fadeIn {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}

@keyframes popIn {
	from {
		transform: scale(0.9);
		opacity: 0;
	}
	to {
		transform: scale(1);
		opacity: 1;
	}
}

@media (max-width: 640px) {
	.recommend-section {
		padding: 1rem;
	}

	.hero-header h1 {
		font-size: 2rem;
	}

	.hero-header p {
		font-size: 1rem;
	}

	.travel-form,
	.response-text {
		padding: 1.5rem;
	}

	.options-block {
		flex-direction: column;
	}

	.location-button,
	.options-button {
		min-width: unset;
	}

	.message-block {
		width: calc(100% - 2rem);
	}
}
</style>