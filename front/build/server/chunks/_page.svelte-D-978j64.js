import { _ as escape_html, g as ensure_array_like, o as attr, s as attr_class } from "./dev-Eb_17b05.js";
import "./index-server-ClQOS8T-.js";
import { t as public_env } from "./shared-server-BcrF-I88.js";
//#region .svelte-kit/adapter-bun/entries/pages/_page.svelte.js
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { form } = $$props;
		let textInput = "";
		let responseText = "Waiting for data input.....";
		let submitBtn = false;
		public_env.PUBLIC_HTTPS;
		let isDragOver = false;
		let chatText = [];
		let questions = [
			{
				"question": "How does the 'translate' and 'identify' feature work?",
				"answer": "Upload or take a photo (if on a mobile phone) then choose translate to translate non English text to English or identify to give the name and historical summary of a building, monument or any other landmark. "
			},
			{
				"question": "Is the app able to translate to other languages?",
				"answer": "The app currenlty only translates to English but can handle multiple popular languages that are to be translated"
			},
			{
				"question": "Can previous chats be viewed again?",
				"answer": "Yes. Through the chats page the previous chats can be viewed again."
			},
			{
				"question": "What does the app give recommendations on?",
				"answer": "It gives recommendations on the 'topic' given such as hotels, game parks within the given 'area' of the 'location' given."
			},
			{
				"question": "How many recommendations are given?",
				"answer": "Atleast one recommendation will be given based on input given. If there are non then nothing wil be shown."
			}
		];
		let features = [
			{
				"title": "Language",
				"subtitle": "Translation & Language",
				"contents": "Instantly translate text from images into English and break down language barriers while traveling"
			},
			{
				"title": "Landmarks",
				"subtitle": "Landmark Identification",
				"contents": "Identify famous monuments, buildings, and historical sites around the world"
			},
			{
				"title": "Chat",
				"subtitle": "Travel Chat Support",
				"contents": "Ask our AI travel advisor anything about your destination and get expert guidance"
			},
			{
				"title": "Storage",
				"subtitle": "Previous Prompts Storage",
				"contents": "View your previous language translations and previously identifed landmarks"
			},
			{
				"title": "Recommendations",
				"subtitle": "Smart Recommendations",
				"contents": "Get personalized travel recommendations and local insights for your destinations"
			}
		];
		$$renderer.push(`<section class="hero"><h1>Travel Made Simple</h1> <p>Translate or identify a buildings, monuments or any other landmark by uploading pictures and also get recommendations on where to visit next around the area you are located.</p> <a href="#preview-section" class="cta-button svelte-1uha8ag">Start Exploring</a></section> <section class="features-section svelte-1uha8ag"><h2 class="svelte-1uha8ag">Why Choose Our Travel Platform?</h2> <div class="features-grid svelte-1uha8ag"><!--[-->`);
		const each_array = ensure_array_like(features);
		for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
			let feature = each_array[$$index];
			$$renderer.push(`<div class="feature-card svelte-1uha8ag"><div class="feature-icon svelte-1uha8ag">${escape_html(feature["title"])}</div> <h3 class="svelte-1uha8ag">${escape_html(feature["subtitle"])}</h3> <p class="svelte-1uha8ag">${escape_html(feature["contents"])}</p></div>`);
		}
		$$renderer.push(`<!--]--></div></section> <div class="main-container"><h2 class="section-title">Translate or Identify</h2> <form><div id="preview-section" class="preview-section svelte-1uha8ag">`);
		$$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> `);
		$$renderer.push("<!--[0-->");
		$$renderer.push(`<button${attr_class("form-group drop-zone svelte-1uha8ag", void 0, { "drag-over": isDragOver })} type="button"><p class="text svelte-1uha8ag"><strong>Drag and Drop your image</strong> here, or click to pick</p> <input name="image" type="file" id="destinationImage" class="file-input svelte-1uha8ag" accept="image/*" required=""/></button>`);
		$$renderer.push(`<!--]--></div> <div class="value-input svelte-1uha8ag"><div class="form-group"><label for="destinationText">Type</label> `);
		$$renderer.select({
			name: "type",
			id: "destinationText",
			value: textInput,
			required: true
		}, ($$renderer) => {
			$$renderer.option({ value: "translate" }, ($$renderer) => {
				$$renderer.push(`translate`);
			});
			$$renderer.option({ value: "identify" }, ($$renderer) => {
				$$renderer.push(`identify`);
			});
		});
		$$renderer.push(`</div> <button type="submit" id="submitBtn"${attr("disabled", submitBtn, true)}>${escape_html("Analysis")}</button></div></form> <div class="response-container"><h3>Response</h3> `);
		$$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> `);
		$$renderer.push("<!--[0-->");
		$$renderer.push(`<div id="apiResponse" class="apiResponse">${escape_html(responseText)}</div>`);
		$$renderer.push(`<!--]--> <div class="chats-main svelte-1uha8ag"><div class="answer-section svelte-1uha8ag"><button class="start-chat svelte-1uha8ag">chat</button></div> `);
		$$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> <!--[-->`);
		const each_array_1 = ensure_array_like(chatText);
		for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
			let eachText = each_array_1[$$index_1];
			$$renderer.push(`<div class="chat-Display svelte-1uha8ag"><p class="question-response svelte-1uha8ag">${escape_html(eachText)}</p></div>`);
		}
		$$renderer.push(`<!--]--> `);
		$$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> `);
		$$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></div></div></div> <section class="faq-section svelte-1uha8ag"><h2 class="svelte-1uha8ag">Frequently Asked Questions</h2> <p class="faq-intro svelte-1uha8ag">Answers to commonly asked questions.</p> <div class="faqs-content svelte-1uha8ag"><!--[-->`);
		const each_array_2 = ensure_array_like(questions);
		for (let $$index_2 = 0, $$length = each_array_2.length; $$index_2 < $$length; $$index_2++) {
			let q = each_array_2[$$index_2];
			$$renderer.push(`<details class="faq-card svelte-1uha8ag"><summary class="svelte-1uha8ag">${escape_html(q["question"])}</summary> <div class="faq-answer svelte-1uha8ag"><p>${escape_html(q["answer"])}</p></div></details>`);
		}
		$$renderer.push(`<!--]--></div></section>`);
	});
}
//#endregion
export { _page as default };

//# sourceMappingURL=_page.svelte-D-978j64.js.map