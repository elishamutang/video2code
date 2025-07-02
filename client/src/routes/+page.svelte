<script lang="ts">
	import Skeleton from '$lib/components/ui/skeleton/skeleton.svelte';
	import type { VideoData, FrameData } from '$lib/dataTypes';
	import { onMount } from 'svelte';
	import { validateTimestamp } from '$lib/helpers';

	let vidData: VideoData = $state({
		message: '',
		video_filename: '',
		duration_hours: 0,
		duration_minutes: 0,
		duration_seconds: 0,
		duration_formatted: '00:00',
		fps: 0,
		total_frames: 0
	});

	let frameData: FrameData = $state({
		frame_filename: '',
		frame_path: '',
		frame_url: '',
		message: '',
		timestamp: '',
		timestamp_seconds: 0,
		video_filename: '',
		extracted_code: '',
		formatted_code: ''
	});

	let isLoading: boolean = $state(true);
	let validationErrors: string[] = $state([]);
	let timestampCollection: FrameData[] = $state([]);

	let submitVidFrameFormBtn: HTMLButtonElement;

	const durationEndpoint = 'http://127.0.0.1:8000/api/video/duration/';

	onMount(async () => {
		// Get video and video duration.
		try {
			const response = await fetch(durationEndpoint, {
				method: 'GET'
			});

			vidData = await response.json();
			isLoading = false;
		} catch (error: any) {
			console.error('Error getting video duration');
		}
	});

	// Get specific frame.
	async function getVidFrame(e: Event): Promise<void> {
		e.preventDefault();

		// Type guard to ensure we have a form submit event
		if (!(e.target instanceof HTMLElement)) {
			console.error('Invalid event target');
			return;
		}

		const form = e.target.closest('form');

		if (!form) {
			console.error('No form found');
			return;
		}

		const formData = new FormData(form);

		// Safe extraction of form data
		let hours = formData.get('hours') as string;
		if (Array.from(hours).length === 1) {
			hours = `0${hours}`;
		}

		let minutes = formData.get('minutes') as string;
		if (Array.from(minutes).length === 1) {
			minutes = `0${minutes}`;
		}

		let seconds = formData.get('seconds') as string;
		if (Array.from(seconds).length === 1) {
			seconds = `0${seconds}`;
		}

		const timestamp = `${hours}:${minutes}:${seconds}`;
		isLoading = true;

		// Validate timestamp
		const validatedTimestamp = validateTimestamp(
			{
				hours: parseInt(hours),
				minutes: parseInt(minutes),
				seconds: parseInt(seconds)
			},
			vidData
		);

		if (validatedTimestamp !== true) {
			// Display custom validation to specific inputs.
			validationErrors = validatedTimestamp;
			isLoading = false;
		} else {
			validationErrors = [];

			try {
				const response = await fetch(`http://127.0.0.1:8000/api/video/frame/${timestamp}/`, {
					method: 'GET'
				});

				if (response.ok) {
					frameData = await response.json();
					timestampCollection.push(frameData);
				}
			} catch (error: any) {
				console.error('Error getting video frame');
			} finally {
				isLoading = false;
			}
		}
	}

	// Allow user to copy code snippet from a specific timestamp.
	function getCode(timestampIdx: number): void {
		const codeTarget = document.getElementById(`timestamp-${timestampIdx}`)

		if (codeTarget !== undefined && codeTarget !== null) {
			navigator.clipboard.writeText(codeTarget.textContent ?? '')
		}
	}

	$effect(() => {
		$inspect(frameData);

		if (!isLoading) {
			submitVidFrameFormBtn.disabled = false;
		}
	});
</script>

<main class="m-5 flex gap-5">
	<div
		class="border border-slate-500 bg-slate-100 max-w-[1000px] flex flex-col items-center p-10 rounded-lg"
	>
		<form
			class="my-5 w-xl bg-slate-600 p-3 rounded-lg border flex gap-2 flex flex-col"
			id="timestampForm"
		>
			<h2 class="text-white text-2xl border-b pb-2 font-semibold">
				Get a specific frame - Video duration: {vidData.duration_formatted}
			</h2>

			<div class="flex-start flex-col gap-2 flex text-white font-semibold">
				<p class="w-full text-center text-xl my-2">Enter a timestamp below:</p>

				{#if validationErrors.length > 0}
					<ul>
						{#each validationErrors as errorMsg}
							<li class="border p-2 my-2 bg-red-800 border-red-800 rounded-md">
								{errorMsg}
							</li>
						{/each}
					</ul>
				{/if}

				<div class="flex gap-10 items-center justify-center w-full mb-2">
					<div class="flex items-center gap-2 w-max mt-2">
						<label for="hours" class="text-white"> Hours: </label>
						{#if isLoading}
							<Skeleton class="w-[80px] min-h-[40px] bg-gray-300" />
						{:else}
							<input
								type="number"
								name="hours"
								id="hours"
								max={vidData.duration_hours}
								min="0"
								value="0"
								aria-busy={isLoading ? 'true' : 'false'}
								class={`truncate text-black flex-1 border p-2 border-transparent rounded-lg ${isLoading ? 'bg-gray-400' : 'bg-gray-200'}`}
							/>
						{/if}
					</div>

					<div class="flex items-center gap-2 w-max mt-2">
						<label for="minutes" class="text-white"> Minutes: </label>
						{#if isLoading}
							<Skeleton class="w-[80px] min-h-[40px] bg-gray-300" />
						{:else}
							<input
								type="number"
								name="minutes"
								id="minutes"
								max={vidData.duration_minutes}
								min="0"
								value="0"
								aria-busy={isLoading ? 'true' : 'false'}
								class="truncate text-black flex-1 border p-2 border-transparent bg-gray-200 rounded-lg"
							/>
						{/if}
					</div>

					<div class="flex items-center gap-2 w-max mt-2">
						<label for="seconds" class="text-white"> Seconds: </label>
						{#if isLoading}
							<Skeleton class="w-[80px] min-h-[40px] bg-gray-300" />
						{:else}
							<input
								type="number"
								name="seconds"
								id="seconds"
								max={vidData.duration_seconds}
								min="0"
								value="0"
								aria-busy={isLoading ? 'true' : 'false'}
								class="truncate text-black flex-1 border p-2 border-transparent bg-gray-200 rounded-lg"
							/>
						{/if}
					</div>
				</div>
			</div>

			<button
				bind:this={submitVidFrameFormBtn}
				type="submit"
				disabled
				aria-disabled="true"
				class={`text-xl border disabled:cursor-disabled disabled:bg-gray-300 disabled:border-gray-400 border-red-500 font-semibold p-2 rounded-lg bg-red-500 text-white ${isLoading ? 'cursor-not-allowed' : 'cursor-pointer'}`}
				onclick={getVidFrame}>Submit</button
			>
		</form>

		<video controls class="my-10 max-w-[800px]">
			<source src="http://127.0.0.1:8000/api/video/" type="video/mp4" />
			<track kind="captions" />
		</video>

		<!-- Extracted frame here -->
		{#if frameData.frame_url !== ''}
			<h1 class="text-2xl font-semibold border-b py-2 border-black">
				Video selected at {frameData.timestamp}
			</h1>
			<img
				class="my-5 max-w-[1000px] w-full h-[500px]"
				src={frameData.frame_url}
				alt={`Extracted frame at ${frameData.timestamp}`}
			/>
		{/if}
	</div>

	<!-- Timestamps section here -->
	<section class="border border-transparent w-full max-h-[900px] h-vh overflow-auto rounded-lg">
		<h1 class="text-3xl p-2 font-semibold">Timestamps</h1>
		{#each timestampCollection as _, idx}
			{@const entry = timestampCollection[timestampCollection.length - 1 - idx]}
			<section
				aria-labelledby="Timestamp at 0 hours, 0 minutes, and 0 seconds."
				class="border m-2 p-2 rounded-lg"
			>
				<h2 class="font-bold">
					<span class="px-1">{timestampCollection.length - idx}</span> Timestamp at {entry.timestamp}
				</h2>
				<pre class="border border-slate-300 p-4 m-4 relative rounded-lg bg-slate-100">
				<div
						class="p-1 text-blue-800 bg-slate-300 border border-transparent absolute top-0 left-0 rounded-tl-lg rounded-br-lg">python</div>
				<code id={`timestamp-${timestampCollection.length - idx}`}>	
					{entry.formatted_code}
				</code>
				<button
						aria-label="Copy code from timestamp {entry.timestamp}"
						onclick={() => getCode(timestampCollection.length - idx)}
						type="button"
						class="cursor-pointer top-2 right-2 absolute border py-1 px-2 bg-slate-300 rounded-md border-slate-400"
						>Copy</button
					>
				</pre>
			</section>
		{/each}
	</section>
</main>
