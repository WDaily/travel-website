<script>

	import { onMount } from "svelte";

	let items = $state("");

	let responseText = $state("");
	let sending = $state(false);

	let images = $state("");
	let amount = $state("");

	const results = $derived.by(() => {
		let chunks = [];
		let itemIndex =0;
		let i = 0;

		for(let count of amount){
			let chunk = types.slice(itemIndex, itemIndex + count);

			chunks.push(images[i],chunk);

			itemIndex += count;

			i += 1;
		}

		return chunks;
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

			items = data.chats;
		
		} catch(error){
			responseText="Previous chats unavailable or an error occurred.";
		} finally{
			sending = false;
		}
	});
</script>


{#if !responseText}
	{#each results as result}

		<div class="chats-section">
			<div class = "display-area">

				{#if sending}
					<div class="loader-container">
						<div class="loader"></div>
					</div>
				{:else}
					<div></div>
				{/if}



				{#if result["image_data"]}
					<div class = "image-area"> 
						<img src={result["image_data"]} alt="upload preview" class="image-preview" />
					</div>
				{/if}

				<div class = "chats-area">
				
					{#if result["model"]}
						<div class = "chats {"model"}">
							{result["model"]}
							<span class ="type"></span>
							<p class = "chat-text"></p>
						</div>
					{/if}

					{#if result["user"]}
						<div class = "chats {"user"}">
							{text["user"]}
							<span class ="type"></span>
							<p class = "chat-text"></p>
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/each}
{:else}
	<div class = "chats-section">
	 	<div class = "desplay-area">
			<div class="response-text"><p>{responseText}</p></div>
		</div>
	</div>
{/if}

<style>
	:root{
		--cart-bg:ivory;
		--text-main: #1f2937;
  		--bot-bubble: #f3f4f5;
  		--user-bubble: #5375f1;
  		--user-text: ivory;
	}

	.display-area {
 		width: 100%;
  		max-width: 450px;
  		height: 90vh;
  		background: var(--card-bg);
  		border-radius: 24px;
  		box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  		display: flex;
  		flex-direction: column;
  		overflow: hidden;
	}
	* {
  		box-sizing: border-box;
 		margin: 0;
  		padding: 0;
	}

	.image-preview {
  		width: 100%;
  		height: auto;
  		position: relative;
	}
	* {
  		box-sizing: border-box;
  		margin: 0;
  		padding: 0;
	}

	.chats-area {
  		flex: 1;
  		overflow-y: scroll;
  		padding: 20px;
  		display: flex;
  		flex-direction: column;
  		gap: 15px;
  		background-color: ivory;
	}
	* {
  		box-sizing: border-box;
  		margin: 0;
	}

	.image-area{
		display:grid;
		place-content:center;
	}
/*
	.image-area{
        position: relative;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }*/

    .image-preview{
        width: auto;
        height: auto;
        max-height: 350px;
        object-fit: contain;
        display: block;
        background: #001;
    }

	.chats {
  		max-width: 80%;
  		padding: 12px 16px;
  		border-radius: 18px;
    	border-bottom-left-radius: 18px;
  		font-size: 0.95rem;
 		line-height: 1.4;
	}
	* {
  		box-sizing: border-box;
  		margin: 0;
  		padding: 0;
	}

	.model {
  		align-self: flex-start;
  		background-color: var(--bot-bubble);
  		color: var(--text-main);
  		border-bottom-left-radius: 4px;
	}

	.user {
  		align-self: flex-end;
  		background-color: var(--user-bubble);
  		color: var(--user-text);
  		border-bottom-right-radius: 4px;
	}

	.chats-section{
		display: grid;
		place-content: center;
	}

	.response-text{
		display: grid;
		place-content: center;
		height:500px;
	}

	@media (max-width: 480px) {
  		.display-area {
    		height: 100vh;
    		border-radius: 0;
  		}
  	}
</style>