export interface VideoData {
	message: string;
	video_filename: string;
	duration_hours: number;
	duration_minutes: number;
	duration_seconds: number;
	duration_formatted: string;
	fps: number;
	total_frames: number;
}

export interface FrameData {
	frame_filename: string;
	frame_path: string;
	frame_url: string;
	message: string;
	timestamp: string;
	timestamp_seconds: number;
	video_filename: string;
	extracted_code: string;
	formatted_code: string;
}

export interface Timestamp {
	hours: number;
	minutes: number;
	seconds: number;
}
