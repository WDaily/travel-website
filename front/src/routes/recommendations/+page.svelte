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

	function optionPicked(){
		chooseOption = !chooseOption;
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

	async function recommend(e){
        e.preventDefault();

        //location();

        if(!latitude && !longitude && !location){
        	errorMessage = "Please provide the location";
        	return
        }

        let userLocation;
        if(locationInput){
        	userLocation = locationInput;
        	console.log("location input");
        }else{
        	userLocation = "latitude: " + latitude + "longitude: " + longitide;
        }

        console.log(userLocation);

        const locationData = {location: userLocation, area: radius, activity: spot};

        try {
             const response = await fetch("http://127.0.0.1:8080/recommend" , {
                method: "POST",
                headers:{ "Content-Type" : "application/json"},
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
        } 
    }	

</script>

<div class="recommend-section">
	{#if responseText}
		<div class="reccommendations">
			<h1>Recommendations</h1>
			<p>{responseText}</p>
		</div>
	{/if}

	{#if errorMessage}
		<div class = "message-section">
			<div class = "message-block">
				<p>{errorMessage}</p>
			</div>
		</div>
	{/if}

	<form onsubmit={recommend}>
		<label for="options-block">Your location</label>

		{#if !chooseOption}
			<div class="options-block">
				<button onclick={location}>location</button>
				<button class="options-button" onclick={optionPicked}>Type instead</button>
			</div>

		{:else}
			<div class="options-block">
				<input name="locationInput" type="text" id="locationInput" bind:value={locationInput} placeholder="Type Your location here" required/>
				<button class="options-button" onclick={optionPicked}>locate instead</button>
			</div>
		{/if}

		<label for="spotValue">Around how many KM</label>
		<input name="radius" type="text" id="spotValue" bind:value={radius} placeholder="Around how many km" required/>

		<label for="spotText" >What is your area of interest</label>
		<input name="spot" type="text" id="spotText" bind:value={spot} placeholder="what are your areas of intrests" required/>

		<button type="submit">Recommendations</button>
	</form>
</div>



<style>
	.options-block{
		display:flex;

	}

	.options-button{
		width:fit-content;
	}

</style>