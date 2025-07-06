<script lang="ts">
	let { children } = $props();
	import '../app.css';

	export const prerender = true;
</script>

{@render children()}
