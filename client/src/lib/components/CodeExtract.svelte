<script lang="ts">
	import Highlight from 'svelte-highlight';
	import python from 'svelte-highlight/languages/python';
	import 'svelte-highlight/styles/github.css';

	let { data, idx, goToTimestamp, getCode, timestampCollectionReversed } = $props();
</script>

<section
	id={`timestamp-${timestampCollectionReversed.length - idx}`}
	aria-labelledby="Timestamp at 0 hours, 0 minutes, and 0 seconds."
	class="my-3 py-2 border-b border-b-slate-300"
>
	<h2 class="font-bold text-slate-600">
		<span class="px-1">{timestampCollectionReversed.length - idx}.</span>Code at timestamp
		<span
			><button
				onclick={() => goToTimestamp(idx)}
				class="cursor-pointer border transition-all delay-150 hover:bg-red-400 hover:text-white hover:border-red-500 px-1 rounded-md text-red-500"
				>{data.timestamp}</button
			></span
		>
	</h2>
	<pre class="border border-slate-300 p-4 m-4 relative rounded-lg bg-slate-100">
				<div
			class="p-1 text-slate-700 bg-slate-300 border border-transparent absolute top-0 left-0 rounded-tl-md rounded-br-lg">python</div>
				<code class="text-(length:--code-text) md:text-base">	
					<Highlight language={python} code={data.formatted_code} />
				</code>
				<button
			aria-label="Copy code from timestamp {data.timestamp}"
			onclick={() => getCode(idx)}
			type="button"
			class="text-slate-700 cursor-pointer top-2 right-2 absolute border py-1 px-2 bg-slate-300 rounded-md border-slate-400 hover:border-blue-500 transition delay-100"
			>Copy</button
		>
				</pre>
</section>
