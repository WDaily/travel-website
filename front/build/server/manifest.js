//#region .svelte-kit/adapter-bun/manifest.js
const manifest = (() => {
	function __memo(fn) {
		let value;
		return () => value ??= value = fn();
	}
	return {
		appDir: "_app",
		appPath: "_app",
		assets: new Set(["robots.txt"]),
		mimeTypes: { ".txt": "text/plain" },
		_: {
			client: {
				start: "_app/immutable/entry/start.CflfysgT.js",
				app: "_app/immutable/entry/app.DuICR1Rh.js",
				imports: [
					"_app/immutable/entry/start.CflfysgT.js",
					"_app/immutable/chunks/44Gwhtzw.js",
					"_app/immutable/chunks/CSxDU9W6.js",
					"_app/immutable/entry/app.DuICR1Rh.js",
					"_app/immutable/chunks/CSxDU9W6.js",
					"_app/immutable/chunks/C8mohMXa.js",
					"_app/immutable/chunks/D1hYfEew.js"
				],
				stylesheets: [],
				fonts: [],
				uses_env_dynamic_public: true
			},
			nodes: [
				__memo(() => import("./chunks/0-B3HcdOyX.js")),
				__memo(() => import("./chunks/1-ChkU_jMV.js")),
				__memo(() => import("./chunks/2-uNpzi4F1.js")),
				__memo(() => import("./chunks/3-25AxP1L8.js")),
				__memo(() => import("./chunks/4-DNzkAYVG.js"))
			],
			remotes: {},
			routes: [
				{
					id: "/",
					pattern: /^\/$/,
					params: [],
					page: {
						layouts: [0],
						errors: [1],
						leaf: 2
					},
					endpoint: null
				},
				{
					id: "/chats",
					pattern: /^\/chats\/?$/,
					params: [],
					page: {
						layouts: [0],
						errors: [1],
						leaf: 3
					},
					endpoint: null
				},
				{
					id: "/recommendations",
					pattern: /^\/recommendations\/?$/,
					params: [],
					page: {
						layouts: [0],
						errors: [1],
						leaf: 4
					},
					endpoint: null
				}
			],
			prerendered_routes: /* @__PURE__ */ new Set([]),
			matchers: async () => {
				return {};
			},
			server_assets: {}
		}
	};
})();
const prerendered = /* @__PURE__ */ new Set([]);
const base = "";
//#endregion
export { base, manifest, prerendered };

//# sourceMappingURL=manifest.js.map