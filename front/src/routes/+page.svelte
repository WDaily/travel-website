<script>
    import { PUBLIC_HTTPS } from "$env/static/public";
    import { onMount } from "svelte";
    let { form } = $props();

    let textInput = $state("");
    let imageInput = $state(null);
    let responseText = $state("Waiting for data input.....");
    let submitBtn = $state(false);
    let sending = $state(false);
    let sendingQuestion = $state(false);

    let mobile = $state(false);

    onMount(() =>{
        const isMobile = /Android|iPhone|webOS|iPad|Blackberry|IEMobile|Opera Mini/i.test(navigator.userAgent);

        if(isMobile){
                mobile = true;
        }
    });

    function fileChange(event){
        const targetImage = event.target.files[0];

        /* if it doesnt work create atemporary url for the image
        if(event.classList.contains("mobile-camera")){
            let Image = URL.createObjectURL(targetImage);
        }
        */

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
        chatText.length = 0;

        try {
            const response = await fetch(`${PUBLIC_HTTPS}/translate` , {
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
            responseText = "Error: " + error.message;
        } finally {
            submitBtn = false;

            sending = false;
        }
    }

    let chatQuestion = $state("");
    let chatText = $state([]);
    let errorText = $state("");
    let clicked = $state(false);
    let questions = [
        {"question": "How does the 'translate' and 'identify' feature work?", "answer":"Upload or take a photo (if on a mobile phone) then choose translate to translate non English text to English or identify to give the name and historical summary of a building, monument or any other landmark. "},
        {"question": "Is the app able to translate to other languages?", "answer":"The app currenlty only translates to English but can handle multiple popular languages that are to be translated"},
        {"question": "Can previous chats be viewed again?", "answer":"Yes. Through the chats page the previous chats can be viewed again."},
        {"question": "What does the app give recommendations on?", "answer":"It gives recommendations on the 'topic' given such as hotels, game parks within the given 'area' of the 'location' given."},
        {"question": "How many recommendations are given?", "answer":"Atleast one recommendation will be given based on input given. If there are non then nothing wil be shown."},
    ];

    let features = [
        {"title":"Language", "subtitle":"Translation & Language", "contents":"Instantly translate text from images into English and break down language barriers while traveling"},
        {"title":"Landmarks", "subtitle":"Landmark Identification", "contents":"Identify famous monuments, buildings, and historical sites around the world"},
        {"title":"Chat", "subtitle":"Travel Chat Support", "contents":"Ask our AI travel advisor anything about your destination and get expert guidance"},
        {"title":"Storage", "subtitle":"Previous Prompts Storage", "contents":"View your previous language translations and previously identifed landmarks"},
        {"title":"Recommendations", "subtitle":"Smart Recommendations", "contents":"Get personalized travel recommendations and local insights for your destinations"},
    ];

    function buttonClick() {
        clicked = !clicked;
    }

    async function question(e){
        e.preventDefault();

        const questionData = {question:chatQuestion};
        sendingQuestion = true;

        try {
             const response = await fetch("${PUBLIC_HTTPS}/question" , {
                method: "POST",
                headers:{ "Content-Type" : "application/json"},
                body: JSON.stringify(questionData),
                credentials:"include"
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(`Server error: ${data.message}`);
             }

             errorText = "";
            chatText.push(data.response);

        } catch (error) {
            errorText = "Error: " + error.message;
        } finally{
            sendingQuestion = false;
        } 
    }

</script>

<section class="hero">
    <h1>Travel Made Simple</h1>
    <p>Translate or identify a buildings, monuments or any other landmark by uploading pictures and also get recommendations on where to visit next around the area you are located.</p>
        <a href="#preview-section" class="cta-button">Start Exploring</a>
</section>

<section class="features-section">
    <h2>Why Choose Our Travel Platform?</h2>
    <div class="features-grid">
        {#each features as feature}
            <div class="feature-card">
                <div class="feature-icon">{feature["title"]}</div>
                <h3>{feature["subtitle"]}</h3>
                <p>{feature["contents"]}</p>
            </div>
        {/each}
    </div>
</section>

<div class="main-container">
    <h2 class="section-title">Translate or Identify</h2>

    <form onsubmit={imageHandle}>
<div id="preview-section" class="preview-section">
        {#if mobile}
            <button onclick={triggerFileInput} type="button" class="photo-button">
                <svg class="photo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span class="photo-text">Capture a Photo</span>
                <input id="mobile-camera" class="file-input" type="file" onchange={fileChange} accept="image/*" capture="environment" bind:this={fileInput}>
            </button>
        {/if}

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
</div>
<div class="value-input">

        <div class="form-group">
            <label for="destinationText">Type</label>
            <select name="type" id="destinationText" bind:value={textInput} required>
                <option value="translate">translate</option>
                <option value="identify">identify</option>
            </select>
        </div>


        <button type="submit" id="submitBtn" disabled={submitBtn} >{submitBtn ? "Sending....." : "Analysis"} </button>
        </div>
    </form>

    <div class="response-container">
        <h3>Response</h3>

        {#if sending}
            <div class="loader-container">
                <div class="loader spinner"></div>
            </div>
        {/if}

        {#if responseText}
        <div id="apiResponse" class="apiResponse">{responseText}</div>
        {/if}

        <div class="chats-main">

            <div class="answer-section">
             <button class="start-chat" onclick={buttonClick}>chat</button>
            </div>

            {#if sendingQuestion && clicked }
                <div class="loader-container">
                    <div class="loader spinner"></div>
                </div>
            {/if}

            {#each chatText as eachText}
                <div class="chat-Display"><p class="question-response">{eachText}</p></div>
            {/each}

            {#if errorText}
                <div class="chat-Display"><p class="question-response">{errorText}</p></div>
            {/if}

             {#if clicked}
            <div class="chat-form">
                <form class="chat-form" onsubmit={question}>
                    <label for="questionInput">Ask a question</label>
                    <div class="question-area">
                    <input type="text" name="chat" bind:value={chatQuestion} class="question-input" required/>
                    <button type="submit" class="answer-button">Send</button>
                    </div>
                </form>
            </div>

            <div class="save-container">
                <a href = "/chats" class="save-button cta-button">Open Chats</a>
            </div>
            {/if}
        </div> 
    </div>
</div>

    <section class="faq-section">
        <h2>Frequently Asked Questions</h2>
        <p class="faq-intro">Answers to commonly asked questions.</p>
        <div class="faqs-content">
            {#each questions as q}
                <details class="faq-card">
                    <summary>{q["question"]}</summary>
                    <div class="faq-answer">
                        <p>{q["answer"]}</p>
                    </div>
                </details>
            {/each}
        </div>
    </section>

<style>
    .chat-Display{
        margin:10px 0px;
        padding:10px;
        background-color:ivory;
        border-radius:20px;

    }

    .chats-main, .chat-form{
        margin:20px 0px;
    }

    .question-area{
        display:flex;
        background-color:ivory;
        border-radius:20px;
        padding:0px 10px;
    }
    .question-input{
        border:none;
    }
    .answer-button{
        width:fit-content;
        background-color:ivory;
        color:var(--primary);
        border: 1px solid var(--primary);
        border-radius:10px;
    }

    .photo-button {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #2c7a7b 0%, #4a9fa8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1.05rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        max-width: 400px;
        margin: 1.5rem auto;
        font-family: inherit;
        text-transform: capitalize;
        letter-spacing: 0.5px;
    }

    .photo-icon {
        width: 24px;
        height: 24px;
        flex-shrink: 0;
    }

    .photo-text {
        display: inline-block;
    }

    .photo-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(44, 122, 123, 0.4);
    }

    .photo-button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(44, 122, 123, 0.3);
    }

    .preview-section {
        flex: 1;
    }

    .value-input {
        flex: 1;
    }

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
        border-color: #2c7a7b;
        background-color: rgba(44, 122, 123, 0.05);
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

    .question-response{
        font-family:monospace:
    }

.cta-button {
        display: inline-block;
        padding: 14px 37px;
        background: white;
        color: var(--primary);
        text-decoration: none;
        border-radius: 8px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        margin: 20px 0px;
    }

    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }

    .features-section {
        max-width: 1100px;
        margin: 200px auto;
        padding: 0 20px;
    }

    .features-section h2 {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 50px;
        color: var(--text-main);
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 32px;
    }

    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 11px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        text-align: center;
        width:fit-content;
    }

    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 11px 24px rgba(0, 0, 0, 0.12);
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 16px;
        font-weight: 500;
        color: var(--primary);
    }

    .feature-card h3 {
        font-size: 1.25rem;
        margin-bottom: 12px;
        color: var(--text-main);
    }

    .feature-card p {
        color: var(--text-main);
        font-size: 0.95rem;
        line-height: 1.7;
    }
.faq-section {
        background: white;
        padding: 80px 20px;
        margin-top: 200px;
    }

    .faq-section h2 {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 17px;
        color: var(--text-main);
    }

    .faq-intro {
        text-align: center;
        color: gray;
        font-size: 1.05rem;
        margin-bottom: 10px;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }

    details{
        background-color:ivory;
        border-radius: 10px;
        margin:20px 0px;
        padding:20px;
        transition: box-shadow 0.5s ease;
    }

    details[open]{
        box-shadow: 0 4px 5px -1px rgba(0, 0, 0, 0.2); 
    }

    summary{
        font-weight:500;
        cursor:pointer;
        list-style:none;
        display:flex;
        justify-content: space-between;
    }

    summary::after{
        content: "\002B";
        font-weight:bold;
        color:(var --text-main);
        transiton: transform 0.2s ease;
    }

    details[open] summary::after{
        content:"\2212";
    }

    summary::-webkit-details-marker{
        display: none;
    }

    .faqs-content{
        margin:5px 0px;
        padding:10px;
        color: var(--text-main)
    }

    .faq-answer{
        color: gray;
        margin:10px 0px;
    }
</style>