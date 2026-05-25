<script lang="js">
    let { form } = $props();

    let textInput = $state("");
    let imageInput = $state(null);
    let responseText = $state("Waiting for data input.....");
    let submitBtn = $state(false);
    let sending = $state(false);


    function fileChange(event){
        const targetImage = event.target.files[0];

        processImage(targetImage);
    }

        let isDragOver = $state(false);
        let previewImage = $state("");
        let fileInput = $state(null);

    function triggerFileInput(){
        if (fileInput) fileInput.click();
    }

    function dragEnter(e){
        e.preventDefault();

        isDragOver = true;
    }

    function dragOver(e){
        e.preventDefault();

        isDragOver = true;
    }

    function dragLeave(){

        isDragOver = false;
    }
    function handleDrop(e){
        e.preventDefault();

        isDragOver = false;

        const file = event.dataTransfer?.files?.[0];

        processImage(file);
    }

    function processImage(imageFile){
        if(!imageFile) return;

        imageInput = imageFile;

        const reader = new FileReader();
        reader.readAsDataURL(imageInput);
        reader.onloadend = () =>{
            previewImage = reader.result;
        };
    }

    function removeImage(e){
        e.stopPropagation();

        previewImage = "";

        if(fileInput) fileInput.value = "";
    }

    async function imageHandle(e){
        e.preventDefault();

        if (!textInput && !imageInput) {
            responseText = "Please provide some text or an image.";
            return;
        }

         const formData = new FormData();
        formData.append('type', textInput);
        if (imageInput) {
            formData.append('image', imageInput);
        }

        responseText = "Processing your request...";
        submitBtn = true;

        sending = true;

        try {
            const response = await fetch("http://127.0.0.1:8080/translate" , {
                method: "POST",
                body: formData,
                credentials: "include"
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(`Error:${data.message}`);
            }

            responseText = data.response;

            textInput = "";

            previewImage = "";

            if(fileInput) fileInput.value = "";

            imageInput = null;
        } catch (error) {
            responseText = "Error: " + error.message + "\n(Note: This is expected if no real API endpoint is configured)";
        } finally {
            submitBtn = false;

            sending = true;
        }
    }

    let chatQuestion = $state("");
    let chatText = $state("");
    let clicked = $state(false);

    function buttonClick() {
        clicked = true;
    }

    async function question(e){
        e.preventDefault();

        const questionData = {question:chatQuestion};


        try {
             const response = await fetch("http://127.0.0.1:8080/question" , {
                method: "POST",
                headers:{ "Content-Type" : "application/json"},
                body: JSON.stringify(questionData),
                credentials:"include"
            });


            const data = await response.json();

            if (!response.ok) {
                 throw new Error(`Server error: ${data.message}`);
             }

            chatText += data.response;

        } catch (error) {

            chatText += "Error: " + error.message;

         } 
    }
</script>

<section class="hero">
    <h1>Make Your Adventure Memorable</h1>
    <p>Upload your pictures to get a language translation or identify a building, munument or any other landmark.</p>
</section>

<div class="main-container">
    <h2 class="section-title">Translator or Identifier</h2>

    <form onsubmit={imageHandle}>

        {#if !previewImage}
            <button
                class="form-group drop-zone"

                class:drag-over={isDragOver}
                onclick={triggerFileInput}
                ondragenter={dragEnter}
                ondragover={dragOver}
                ondragleave={dragLeave}
                ondrop={handleDrop}
                type="button"
            >
                <!--<label for="destinationImage">Upload a reference image</label>-->
                <p class="text"><strong>Drag and Drop your image</strong> here, or click to pick</p>
                <input name="image" type="file" id="destinationImage" class="file-input" onchange={fileChange} accept="image/*" bind:this={fileInput} required>
            </button>
        {:else}
            <div class="preview-container">
                <button class="remove-btn" onclick={removeImage} type="button">Remove</button>
                <img src={previewImage} alt="uploaded file" class="preview-image">
            </div>
        {/if}


        <div class="form-group">
            <label for="destinationText">Type</label>
            <input name="type" type="text" id="destinationText" bind:value={textInput} placeholder="translate" required/>
        </div>


        <button type="submit" id="submitBtn" disabled={submitBtn} >{submitBtn ? "Sending....." : "Analysis"} </button>
    </form>

    <div class="response-container">
        <h3>API Response</h3>

        {#if sending}
            <div class="loader-container">
                <div class="loader"></div>
            </div>
        {:else}
        <div></div>
        {/if}

        {#if responseText}
        <div id="apiResponse">{responseText}</div>
        {/if}

        <div class="chats">

            <div class="answer-section">
             <button class="start-chat" onclick={buttonClick}>chat</button>
            </div>

            {#if chatText}
                <div class="chat-Display"><p>{chatText}</p></div>
            {/if}

             {#if clicked}
            <div class="chat-form">
                <form class="chat-form" onsubmit={question}>
                    <label for="questionInput">Ask a question</label>
                    <input type="text" name="chat" bind:value={chatQuestion} class="question-input" required/>
                    <button type="submit" class="answer-button">Answer</button>
                </form>
            </div>
            {/if}

            {#if chatText}
            <div class="save-container">
                <button class="save">Open Chats</button>
            </div>
            {/if}
        </div> 
    </div>
</div>

<style>
    .drop-zone{
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        background: #f8fafc;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 250px;
        width: 100%;
        font-size: 1rem;
    }

    .drop-zone:hover, .drop-zone.drag-over{
        border-color: #4f46e5;
        background-color: #f0fdff4;
    }

    .drop-zone:hover{
        transform: translateY(-2px);
    }

    .file-input{
        display: none;
    }

    .preview-container{
        position: relative;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    .preview-image{
        width: 100%;
        height: auto;
        max-height: 350px;
        object-fit: contain;
        display: block;
        background: #001;
    }

    .remove-btn{
        width: fit-content;
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(15, 23, 41, 0.75);
        color: ivory;
        border: none;
        padding: 0.5rem 0.8rem;
        border-radius: 20px;
        cursor: pointer;
        font-size: 0.8rem;
        backdrop-filter: blur(4px);
        transition: all 0.3s ease;
        z-index: 10;
    }

    .remove-btn:hover{
        background: rgba(239, 68, 68, 0.9);
    }

    .answer-section{
        width:100%;
        display:grid;
        place-content:end;
    }
    .start-chat{
        width:fit-content;
        transition: transform 0.1s, opacity 0.2s;
        padding:10px;
        margin:20px 0px;
        border-radius:10px;
    }

    .start-chat:hover {
        opacity: 0.9;
    }

    .start-chat:active {
        transform: scale(0.95);
    }

    .answer-button{
        margin: 10px 0px;
        transition: transform 0.1s;
    }

    .answer-button:active{
        transform:scale(0.95);
    }

    .text{
        color:grey;
        font-size:0.95rem;
        font-weight:normal;
    }
</style>