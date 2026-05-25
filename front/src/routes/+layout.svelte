<script>
	import favicon from '$lib/assets/favicon.svg';
	import "../app.css";
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header>
	<h2>Website</h2>
	<nav><a href="/"> Home</a> | <a href="/chats">Chats</a></nav>
</header>

{@render children()}

<footer>
	&copy; All rights reserved.
</footer>