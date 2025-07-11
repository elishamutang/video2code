import type { Timestamp, VideoData } from './dataTypes';

function extractYoutubeVideoId(link: string): string | null {
	const youtubeIdRegex: RegExp =
		/(?:youtube(?:-nocookie)?\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;

	const id = link.match(youtubeIdRegex);
	return id ? id[1] : null;
}

// Client side validation for timestamp.
function validateTimestamp(timestamp: Timestamp, videoData: VideoData): string[] | true {
	const isPlural = {
		hours: videoData.duration_hours > 1 ? true : false,
		minutes: videoData.duration_minutes > 1 ? true : false,
		seconds: videoData.duration_seconds > 1 ? true : false
	};

	const errors = [];

	if (timestamp.hours === 0 && timestamp.minutes === 0 && timestamp.seconds === 0) {
		errors.push(
			'Hours, minutes and seconds cannot all be zero at the same time.'
		)
	}

	if (timestamp.hours > videoData.duration_hours) {
		errors.push(
			`${isPlural.hours ? 'Hours' : 'Hour'} must not exceed ${videoData.duration_hours} ${isPlural.hours ? 'hours' : 'hour'}`
		);
	}

	if (timestamp.minutes > videoData.duration_minutes) {
		errors.push(
			`${isPlural.minutes ? 'Minutes' : 'Minute'} must not exceed ${videoData.duration_minutes} ${isPlural.minutes ? 'minutes' : 'minute'} `
		);
	}

	if (videoData.duration_minutes >= 1 && timestamp.seconds > 60) {
		errors.push(`Seconds must not exceed 60 seconds.`);
	}

	return errors.length > 0 ? errors : true;
}

// Check whether localStorage is both supported and available:
function localStorageAvailable(type: string) {
	let storage: Storage;

	try {
		storage = window[type]
		const x = "__storage_test__";
		storage.setItem(x, x)
		storage.removeItem(x)
		return true;
	} catch (e: any) {
		return (
			e instanceof DOMException &&
			e.name === "QuotaExceededError" &&
			// acknowledge QuotaExceededError only if there's something already stored.
			storage && storage.length! == 0
		)
	}
}

export { extractYoutubeVideoId, validateTimestamp, localStorageAvailable };
