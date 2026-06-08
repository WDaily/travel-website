import { o as attr } from "./dev-Eb_17b05.js";
//#region .svelte-kit/adapter-bun/entries/pages/recommendations/_page.svelte.js
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { form } = $$props;
		let radius = "";
		let spot = "";
		$$renderer.push(`<div class="recommend-section svelte-1uxfyd3"><div class="hero-header svelte-1uxfyd3"><h1 class="svelte-1uxfyd3">Discover Your Next Adventure</h1> <p class="svelte-1uxfyd3">Find the perfect travel recommendations tailored to your interests</p></div> <div class="recommend-block svelte-1uxfyd3">`);
		$$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> `);
		$$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> `);
		$$renderer.push("<!--[0-->");
		$$renderer.push(`<form class="travel-form svelte-1uxfyd3"><div class="form-section svelte-1uxfyd3"><label for="options-block" class="section-label svelte-1uxfyd3">Location</label> `);
		$$renderer.push("<!--[0-->");
		$$renderer.push(`<div class="options-block svelte-1uxfyd3"><button class="location-button svelte-1uxfyd3" type="button">Use My Current Location</button> <button class="options-button svelte-1uxfyd3" type="button">Type Location Instead</button></div>`);
		$$renderer.push(`<!--]--></div> <div class="form-section svelte-1uxfyd3"><label for="spotValue" class="section-label svelte-1uxfyd3">Distance</label> <div class="input-group svelte-1uxfyd3"><input name="radius" type="number" id="spotValue"${attr("value", radius)} placeholder="50" required="" class="form-input svelte-1uxfyd3" min="1"/> <span class="unit svelte-1uxfyd3">km</span></div></div> <div class="form-section svelte-1uxfyd3"><label for="spotText" class="section-label svelte-1uxfyd3">Interest</label> <input name="spot" type="text" id="spotText"${attr("value", spot)} placeholder="e.g., hotels, museums, game parks" required="" class="form-input svelte-1uxfyd3"/></div> <button type="submit" class="submit-button svelte-1uxfyd3">Get Recommendations</button></form>`);
		$$renderer.push(`<!--]--></div></div>`);
	});
}
//#endregion
export { _page as default };

//# sourceMappingURL=_page.svelte-Dq96SmfF.js.map