<script>

	import { onMount } from "svelte";

	let items = $state([]);
	let responseText = $state("");
	let sending = $state(false);
	let images = $state([]);
	let amount = $state([]);

	const results = $derived.by(() => {
		let displayAreas = [];
		let itemIndex = 0;

		for (var i = 0; i < amount.length; i++) {
			let displayArea = {
				image_data: images[i]["image_data"],
				chats: []
			};

			for (var r = 0; r < amount[i]; r++) {
				displayArea.chats.push(items[itemIndex + r]);
			}

			itemIndex += amount[i];
			displayAreas.push(displayArea);
		}

		return displayAreas;
	});

	onMount(async () => {

		sending = true;
		try{
			const response = await fetch("http://127.0.0.1:8080/chats",{
				credentials:"include"
			});
		
			const data = await response.json();

			if (!response.ok) {
				throw new Error(`Error:${data.message}`);
			}

			items = data.chat;
			images = data.images;
			amount = data.amount;
		
		} catch(error){
			responseText="Previous chats unavailable or an error occurred.";
		}finally{
			sending = false;
		}
	});
	
</script>

<div class="page-header">
				<h1>Previous Chats</h1>
				<p class="tagline">Your previous chat history.</p>
			</div>
{#if !responseText}

		<div class="chats-section">


			{#if sending}
				<div class="loader-container">
					<div class="loader"></div>
				</div>
			{/if}

			{#each results as displayArea}
			<div class = "display-area">

				{#if displayArea.image_data}
					<div class = "image-area"> 
						<img src={displayArea.image_data} alt="travel destination image, travel planning inspiration, vacation location preview" class="image-preview" />
					</div>
				{/if}

				<div class = "chats-area">
					<span class="chat-section-label">Travel Planning Discussion</span>
					{#each displayArea.chats as chat}
						{#if chat["model"]}
							<div class = "chats model">
								<span class="chat-role">Response</span>
								{chat["model"]}
								<span class ="type"></span>
								<p class = "chat-text"></p>
							</div>
						{/if}

						{#if chat["user"]}
							<div class = "chats user">
								<span class="chat-role">Your Query</span>
								{chat["user"]}
								<span class ="type"></span>
								<p class = "chat-text"></p>
							</div>
						{/if}
					{/each}
				</div>
			</div>
			{/each}
		</div>
	
{:else}
	<div class = "chats-section">
	 	<div class = "display-area">
			<div class="response-text"><p>{responseText}</p></div>
		</div>
	</div>
{/if}