import { O as head, o as attr } from "./dev-Eb_17b05.js";
//#region .svelte-kit/adapter-bun/entries/pages/_layout.svelte.js
var favicon_default = "data:image/svg+xml,%3csvg%20xmlns='http://w3.org'%20viewBox='0%200%2032%2032'%20width='32'%20height='32'%3e%3cg%20fill='none'%20stroke='currentColor'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3e%3cpath%20d='M12,%207%20C12,%203%2020,3%2020,6'%20stroke-width='1.7'/%3e%3crect%20x='5.8'%20y='8'%20width='20'%20height='19'%20rx='3'/%3e%3cpath%20d='M6,%2013%20L26,%2013'/%3e%3crect%20x='9'%20y='17'%20width='14'%20height='7'%20rx='1.5'/%3e%3cpath%20d='M10,%208%20L10,%2025'%20stroke-width='1.5'%20stroke-dasharray='3,2'/%3e%3cpath%20d='M22,%208%20L22,%2025'%20stroke-width='1.5'%20stroke-dasharray='3,2'/%3e%3c/g%3e%3c/svg%3e";
function _layout($$renderer, $$props) {
	let { children } = $$props;
	head("12qhfyh", $$renderer, ($$renderer) => {
		$$renderer.push(`<link rel="icon"${attr("href", favicon_default)}/>`);
	});
	$$renderer.push(`<header><h2>Easy Travel</h2> <nav><a href="/">Home</a> | <a href="/chats">Chats</a> | <a href="/recommendations">Recommendations</a></nav></header> `);
	children($$renderer);
	$$renderer.push(`<!----> <footer>© All rights reserved.</footer>`);
}
//#endregion
export { _layout as default };

//# sourceMappingURL=_layout.svelte-CRNDL83T.js.map