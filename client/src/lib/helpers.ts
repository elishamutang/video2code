import type { FrameData, Timestamp, VideoData } from './dataTypes';

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

// Mock success API response
function successAPIResponse(): Promise<FrameData> {
	return new Promise((resolve, _) => {
		setTimeout(() => {
			const result = {
				frame_filename: '',
				frame_path: '',
				frame_url: '',
				message: '',
				timestamp: '',
				timestamp_seconds: 0,
				video_filename: '',
				extracted_code: '',
				formatted_code: `
class User:
    def __init__(self, full_name, birthday):
        self.name = full_name
        self.birthday = birthday  # yyyymmdd
        # Extract first and last names
        name_pieces = full_name.split(" ")
        self.first_name = name_pieces[0]
        self.last_name = name_pieces[-1]

user = User("Dave Bowman", 19710315)
`
			}

			resolve(result)
		}, 2000);
	})
}

// Mock fail API response
function failAPIResponse(): Promise<FrameData> {
	return new Promise((_, reject) => {
		setTimeout(() => {
			const result = {
				frame_filename: '',
				frame_path: '',
				frame_url: '',
				message: '',
				timestamp: '',
				timestamp_seconds: 0,
				video_filename: '',
				extracted_code: 'OCR error: ERROR',
				formatted_code: '',
			}

			reject(result)
		}, 2000)
	})
}

export { extractYoutubeVideoId, validateTimestamp, successAPIResponse, failAPIResponse };
