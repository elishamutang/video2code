import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os, cv2
from django.conf import settings
from ranged_response import RangedFileResponse
from .helpers import parse_timestamp_to_seconds, \
    extract_frame, extract_code_from_frame, clean_extracted_text


@api_view(['GET'])
def serve_video(request):
    filename = 'oop.mp4'
    video_path = os.path.join(settings.BASE_DIR, 'videos', filename)
    
    if not os.path.exists(video_path):
        return Response({'error': 'Video not found'}, status=404)
    
    # Use RangedFileResponse instead of FileResponse
    response = RangedFileResponse(
        request, 
        open(video_path, 'rb'), 
        content_type='video/mp4'
    )
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    
    return response


@api_view(['GET'])
def get_vid_duration(request):
    try:
        # Set the video filename
        video_filename = 'oop.mp4'  # Add extension if needed
        
        # Construct the path to the video file
        video_path = os.path.join(settings.BASE_DIR, 'videos', video_filename)
        
        # Check if the file exists
        if not os.path.exists(video_path):
            return Response({
                'error': f'Video file not found: {video_filename}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get video duration using OpenCV
        video = cv2.VideoCapture(video_path)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        duration_seconds = frame_count / fps if fps > 0 else 0
        video.release()
        
        # Convert seconds to HH:MM:SS format
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        
        duration_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        return Response({
            'message': 'Video duration retrieved successfully',
            'video_filename': video_filename,
            'duration_hours': hours,
            'duration_minutes': minutes,
            'duration_seconds': seconds,
            'duration_formatted': duration_formatted,
            'fps': fps,
            'total_frames': frame_count
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Error fetching video duration: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_vid_frame(request, timestamp):
    # Set the video filename to 'oop'
    video_filename = 'oop.mp4'
    
    # Convert timestamp to seconds
    try:
        timestamp_seconds = parse_timestamp_to_seconds(timestamp)
    except ValueError as e:
        return Response({
            'error': f'Invalid timestamp format: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Check if video file exists in videos folder
    video_path = os.path.join(settings.BASE_DIR, 'videos', video_filename)
    if not os.path.exists(video_path):
        return Response({
            'error': f'Video file not found: {video_filename}'
        }, status=status.HTTP_404_NOT_FOUND)

    # Extract frame
    frame_info = extract_frame(video_filename, timestamp_seconds, timestamp)

    if frame_info:
        # Read the image file and encode as base64
        try:
            with open(frame_info['frame_path'], 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            return Response({
                'error': f'Failed to read frame: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create URL for accessing the frame
        frame_url = f"data:image/jpeg;base64,{image_data}"

        # Extract code frame using OCR
        try:
            extracted_code = extract_code_from_frame(frame_info['frame_path'])

            # Pass to AI to clean up and format.
            cleaned_code = clean_extracted_text(extracted_code)

        except Exception as e:
            extracted_code = f"OCR error: {str(e)}"

        return Response({
            'message': 'Frame extracted successfully',
            'video_filename': video_filename,
            'timestamp': timestamp,
            'timestamp_seconds': timestamp_seconds,
            'frame_path': frame_info['frame_path'],
            'frame_filename': frame_info['frame_filename'],
            'frame_url': frame_url,
            'extracted_code': extracted_code,
            'formatted_code': cleaned_code,
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Failed to extract frame from video'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
