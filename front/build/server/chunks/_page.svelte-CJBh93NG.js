import { _ as escape_html, g as ensure_array_like, h as derived, o as attr } from "./dev-Eb_17b05.js";
import "./index-server-ClQOS8T-.js";
import { t as public_env } from "./shared-server-BcrF-I88.js";
//#region .svelte-kit/adapter-bun/entries/pages/chats/_page.svelte.js
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let items = [];
		let images = [];
		let amount = [];
		public_env.PUBLIC_HTTPS;
		const results = derived(() => {
			let displayAreas = [];
			let itemIndex = 0;
			for (var i = 0; i < amount.length; i++) {
				let displayArea = {
					image_data: images[i]["image_data"],
					chats: []
				};
				for (var r = 0; r < amount[i]; r++) displayArea.chats.push(items[itemIndex + r]);
				itemIndex += amount[i];
				displayAreas.push(displayArea);
			}
			return displayAreas;
		});
		$$renderer.push(`<div class="page-header"><h1>Previous Chats</h1> <p class="tagline">Your previous chat history.</p></div> `);
		{
			$$renderer.push("<!--[0-->");
			$$renderer.push(`<div class="chats-section">`);
			$$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--]--> <!--[-->`);
			const each_array = ensure_array_like(results());
			for (let $$index_1 = 0, $$length = each_array.length; $$index_1 < $$length; $$index_1++) {
				let displayArea = each_array[$$index_1];
				$$renderer.push(`<div class="display-area">`);
				if (displayArea.image_data) {
					$$renderer.push("<!--[0-->");
					$$renderer.push(`<div class="image-area"><img${attr("src", displayArea.image_data)} alt="travel destination image, travel planning inspiration, vacation location preview" class="image-preview"/></div>`);
				} else $$renderer.push("<!--[-1-->");
				$$renderer.push(`<!--]--> <div class="chats-area"><span class="chat-section-label">Travel Planning Discussion</span> <!--[-->`);
				const each_array_1 = ensure_array_like(displayArea.chats);
				for (let $$index = 0, $$length = each_array_1.length; $$index < $$length; $$index++) {
					let chat = each_array_1[$$index];
					if (chat["model"]) {
						$$renderer.push("<!--[0-->");
						$$renderer.push(`<div class="chats model"><span class="chat-role">Response</span> ${escape_html(chat["model"])} <span class="type"></span> <p class="chat-text"></p></div>`);
					} else $$renderer.push("<!--[-1-->");
					$$renderer.push(`<!--]--> `);
					if (chat["user"]) {
						$$renderer.push("<!--[0-->");
						$$renderer.push(`<div class="chats user"><span class="chat-role">Your Query</span> ${escape_html(chat["user"])} <span class="type"></span> <p class="chat-text"></p></div>`);
					} else $$renderer.push("<!--[-1-->");
					$$renderer.push(`<!--]-->`);
				}
				$$renderer.push(`<!--]--></div></div>`);
			}
			$$renderer.push(`<!--]--></div>`);
		}
		$$renderer.push(`<!--]-->`);
	});
}
//#endregion
export { _page as default };

//# sourceMappingURL=_page.svelte-CJBh93NG.js.map