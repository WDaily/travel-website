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
				start: "_app/immutable/entry/start.Bc94nqKn.js",
				app: "_app/immutable/entry/app.Sux4o_v5.js",
				imports: [
					"_app/immutable/entry/start.Bc94nqKn.js",
					"_app/immutable/chunks/nKYU_8Mg.js",
					"_app/immutable/chunks/CSxDU9W6.js",
					"_app/immutable/entry/app.Sux4o_v5.js",
					"_app/immutable/chunks/CSxDU9W6.js",
					"_app/immutable/chunks/C8mohMXa.js",
					"_app/immutable/chunks/D1hYfEew.js"
				],
				stylesheets: [],
				fonts: [],
				uses_env_dynamic_public: false
			},
			nodes: [
				__memo(() => import("./chunks/0-C-xVz35E.js")),
				__memo(() => import("./chunks/1-BsfoKp6u.js")),
				__memo(() => import("./chunks/2-Bt2sAGZy.js")),
				__memo(() => import("./chunks/3-CaEOkQ02.js")),
				__memo(() => import("./chunks/4-x-jli2c0.js"))
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