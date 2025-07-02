<script lang="ts">
	import Skeleton from './ui/skeleton/skeleton.svelte';

	let { vidId } = $props();

	let iframeLoaded = $state(false);
	let showLoading = $state(true);

	function handleIframeLoad() {
		iframeLoaded = true;
		showLoading = false;
		console.log('Iframe loaded successfully');
	}

	function handleIframeError() {
		showLoading = false;
		console.log('Iframe failed to load');
	}
</script>

{#if showLoading}
	<Skeleton class="max-w-[1000px] w-full h-[500px] bg-gray-200 my-10" />
{/if}

<iframe
	class="max-w-[1000px] my-10 w-full h-[500px]"
	src="https://www.youtube.com/embed/{vidId}"
	title="YouTube video player"
	frameborder="0"
	allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
	referrerpolicy="strict-origin-when-cross-origin"
	allowfullscreen
	onload={handleIframeLoad}
	onerror={handleIframeError}
	hidden={iframeLoaded ? false : true}
></iframe>
