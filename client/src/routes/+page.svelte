<script lang="ts">
	import Skeleton from '$lib/components/ui/skeleton/skeleton.svelte';
	import { toast } from 'svelte-sonner';
	import type { VideoData, FrameData } from '$lib/dataTypes';
	import { onMount } from 'svelte';
	import { localStorageAvailable, validateTimestamp } from '$lib/helpers';
	import CodeExtract from '$lib/components/CodeExtract.svelte';

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
	let timestampCollectionReversed: FrameData[] = $derived(timestampCollection.toReversed());

	let submitVidFrameFormBtn: HTMLButtonElement;
	let videoElem: HTMLMediaElement;

	onMount(async () => {
		// Check if local storage is available
		if (localStorageAvailable('localStorage')) {
			toast.success('Local storage loaded!');

			// Get video duration.
			try {
				const response = await fetch('https://video2code.xyz/api/video/duration/', {
					method: 'GET'
				});

				vidData = await response.json();
				isLoading = false;

				// Set localStorage
				if (!localStorage.getItem('data')) {
					localStorage.setItem('data', JSON.stringify(timestampCollection));
				} else {
					timestampCollection = JSON.parse(localStorage.getItem('data') ?? '[]');
				}
			} catch (error: any) {
				console.error('Error getting video duration');
				toast.error('Error getting video duration, please refresh the page!');
			}
		} else {
			toast.error('Local storage not supported :(');
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

			// Check if timestampCollection exists in localStorage
			const existingData = timestampCollection.find((data) => data.timestamp === timestamp);

			if (existingData) {
				isLoading = false;

				toast.info('Duplicate found!', {
					description: `Code at timestamp ${timestamp} has already been generated!`
				});
			} else {
				try {
					const response = await fetch(
						`https://video2code.xyz/api/media/video/frame/${timestamp}/`,
						{
							method: 'GET'
						}
					);

					if (!response.ok) {
						// Throw error
						const errorMsg = await response.json();
						throw new Error(errorMsg.detail);
					} else {
						// Get frame data.
						frameData = await response.json();

						// Throw an error if formatted_code is null.
						if (!frameData.formatted_code) {
							throw new Error('Error formatting the code...');
						}

						timestampCollection.push(frameData);
						toast.success('Code generated!');

						// Overwrite data in localStorage
						localStorage.setItem('data', JSON.stringify(timestampCollection));

						// Set currentTime for videoElem
						videoElem.currentTime = frameData.timestamp_seconds;
					}
				} catch (error: any) {
					console.error(error.message);
					toast.error(error.message ?? 'Error generating the extracted code, please try again!');
				} finally {
					isLoading = false;
				}
			}
		}
	}

	// Allow user to copy code snippet from a specific timestamp.
	function getCode(timestampIdx: number): void {
		const timestampCard = document.getElementById(`timestamp-${timestampIdx}`);

		if (timestampCard !== undefined && timestampCard !== null) {
			const code = timestampCard.querySelector('code');

			if (code) {
				navigator.clipboard.writeText(code.textContent ?? '');
			}
		}

		toast.info('Code copied to clipboard', {
			description: `Copied code from timestamp No.${timestampIdx}!`
		});
	}

	// Allow user to go to a specific point in time of the video based on timestamp.
	function goToTimestamp(timestampIdx: number) {
		frameData = timestampCollectionReversed[timestampIdx];
		videoElem.currentTime = frameData.timestamp_seconds;

		toast.info('Back in time!', {
			description: `Navigated back in time to ${frameData.timestamp}!`
		});
	}

	$effect(() => {
		if (!isLoading) {
			submitVidFrameFormBtn.disabled = false;
		}
	});
</script>

<main
	class="m-2 border-slate-300 rounded-lg sm:border md:p-5 max-w-7xl gap-6 sm:grid sm:grid-cols-2 sm:m-5"
>
	<!-- Title -->
	<section
		class="my-5 border-b border-b-slate-300 pb-5 md:my-0 flex flex-col items-center sm:col-start-1 sm:col-end-3 sm:row-start-1 sm:row-end-2"
	>
		<h1 class="md:text-5xl text-3xl font-bold text-slate-600">Video2Code.</h1>
		<a class="text-sm text-slate-400" target="_blank" href="https://elishamutang.xyz/"
			>by <span class="border-b border-b-slate-400 hover:text-slate-800">elishamutang</span></a
		>
	</section>

	<!-- Brief description -->
	<section
		class="sm:border-b sm:border-b-slate-300 w-full sm:col-start-1 sm:col-end-3 sm:row-start-2 sm:row-end-3"
	>
		<section class="pb-5">
			<h1 class="md:text-4xl text-2xl text-slate-600 font-bold mb-2">What is it?</h1>
			<p class="text-slate-700 text-lg">
				- A web application to <span class="italic">detect</span>,
				<span class="italic">extract</span>, and <span class="italic">display</span> code from a specific
				frame to the user in the appropriate format.
			</p>
		</section>
	</section>

	<section
		class="sm:row-start-3 sm:row-end-4 sm:border-none border-t border-b border-t-slate-300 border-b-slate-300 sm:max-w-[1000px] sm:col-1 w-full flex flex-col items-center p-2"
	>
		<!-- Disclaimer -->
		<section class="p-2 border border-slate-300 rounded-md mt-2 xl:md-0">
			<p class="text-slate-500 text-sm">
				<strong>Disclaimer: </strong> Requests are limited to <strong>20 requests</strong> per hour to
				prevent abuse and ensure fair access.
			</p>
		</section>

		<!-- Form -->
		<form
			class="md:place-self-center my-5 sm:w-max-content sm:max-w-[800px] w-full bg-slate-300 p-3 rounded-lg border flex gap-2 flex flex-col"
			id="timestampForm"
		>
			<h2 class="text-slate-700 text-2xl border-b pb-2 font-semibold">
				Get a specific frame - Video duration: {vidData.duration_formatted}
			</h2>

			<div class="flex-start flex-col gap-2 flex text-slate-700 font-semibold">
				<p class="w-full text-center text-xl my-2">Enter a timestamp below:</p>

				{#if validationErrors.length > 0}
					<ul>
						{#each validationErrors as errorMsg}
							<li class="flex border p-2 my-2 bg-red-400 border-red-800 rounded-md">
								<span class="font-semibold text-red-800 flex-1">Invalid input: </span>
								<div class="flex-4">{errorMsg}</div>
							</li>
						{/each}
					</ul>
				{/if}

				<div
					class="flex flex-col xl:justify-around xl:flex-row sm:gap-2 sm:justify-center items-center w-full mb-2"
				>
					<div class="flex items-center gap-2 w-[200px] xl:w-max max-w-content sm:mt-2">
						<label for="hours" class="text-slate-700 w-max text-end flex-1"> Hours: </label>
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
								class="text-slate-700 truncate text-black flex-1 w-[200px] lg:w-[80px] border p-2 border-transparent bg-gray-200 rounded-md"
							/>
						{/if}
					</div>

					<div class="flex items-center gap-2 w-[200px] max-w-content xl:w-max mt-2">
						<label for="minutes" class="text-slate-700 w-[100px] flex-1 text-end"> Minutes: </label>
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
								class="text-slate-700 w-[200px] flex-1 lg:w-[80px] truncate text-black border p-2 border-transparent bg-gray-200 rounded-md"
							/>
						{/if}
					</div>

					<div class="flex items-center xl:w-max gap-2 w-[200px] max-w-content mt-2">
						<label for="seconds" class="text-slate-700 w-[100px] flex-1 text-end"> Seconds: </label>
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
								class="text-slate-700 w-[200px] lg:w-[80px] truncate text-black flex-1 border p-2 border-transparent bg-gray-200 rounded-md"
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
				class={`text-xl border hover:bg-red-600 disabled:cursor-disabled disabled:bg-gray-300 disabled:border-gray-400 border-red-400 font-semibold p-2 rounded-lg bg-red-500 transition-all delay-150 motion-discrete text-white ${isLoading ? 'cursor-not-allowed opacity-75' : 'cursor-pointer'}`}
				onclick={getVidFrame}>{isLoading ? 'Generating frame & code...' : 'Submit'}</button
			>
		</form>

		<!-- Separator -->
		<div class="border w-full border-slate-300 my-2"></div>

		<!-- Video -->
		<section class="flex flex-col items-center">
			<h1 class="text-3xl mb-2 font-bold text-slate-600">Video</h1>
			<video
				bind:this={videoElem}
				poster="https://i.ytimg.com/vi/apACNr7DC_s/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLArfSCg8eIP-tmc8Q8YcbsZy5bwxA"
				controls
				class="mb-10 w-full max-w-[800px]"
			>
				<source src="https://video2code.xyz/api/media/video/" type="video/mp4" />
				<p class="text-red-500">Your browser does not support the video tag.</p>
				<track kind="captions" />
			</video>
		</section>

		<!-- Extracted frame here -->
		{#if frameData.frame_url !== ''}
			{#if isLoading}
				<Skeleton class="bg-slate-400 w-full h-[300px]" />
			{:else}
				<h1 class="text-3xl text-slate-600 font-semibold border-b py-2 border-b-slate-300">
					Frame selected at {frameData.timestamp}
				</h1>
				<img
					class="my-5 max-w-[1000px] w-full max-h-[500px]"
					src={frameData.frame_url}
					alt={`Extracted frame at ${frameData.timestamp}`}
				/>
			{/if}
		{/if}
	</section>

	<!-- Timestamps section here -->
	<section
		class="md:p-4 md:border-l md:border-l-slate-300 md:rounded-none sm:col-2 sm:row-start-3 sm:row-end-5 border border-transparent w-full max-h-[1000px] h-full overflow-auto rounded-lg"
	>
		<h1 class="md:mt-0 text-3xl my-2 mt-5 font-bold text-slate-600">Timestamps</h1>

		{#if timestampCollection.length === 0 && !isLoading}
			<p class="m-2 text-slate-500 italic">Nothing to see here...</p>
		{:else}
			{#if isLoading}
				<Skeleton class="bg-slate-400 w-full h-[300px]" />
			{/if}

			<!-- Code Extracts -->
			{#each timestampCollectionReversed as data, idx}
				<CodeExtract {data} {idx} {goToTimestamp} {getCode} {timestampCollectionReversed} />
			{/each}
		{/if}
	</section>
</main>
