import re, os, cv2, pytesseract, os
from PIL import Image
import numpy as np
from django.conf import settings
from groq import Groq
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Videos directory
vid_folder_path = os.path.join(settings.BASE_DIR, 'adv_ui_ocrroo_app', 'media', 'videos')

# Set Tesseract OCR path (WINDOWS ONLY)
# tesseract_path = os.environ.get('TESSERACT_PATH')
# pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Get video duration 
def get_vid_duration(video_filename):
    try:
        video_path = os.path.join(vid_folder_path, video_filename)
        
        if not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            return None
        
        video = cv2.VideoCapture(video_path)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps
        video.release()
        
        return duration
    
    except Exception as e:
        print(f"Error fetching video duration: {str(e)}")
        return None


# Parse timestamp to seconds
def parse_timestamp_to_seconds(timestamp):
    """ Convert timestamp string (HH:MM:SS or MM:SS) to seconds"""
    timestamp = timestamp.strip()

    if ':' not in timestamp:
        raise ValueError("Timestamp must be in HH:MM:SS or MM:SS format")
    
    parts = timestamp.split(':')

    if len(parts) == 2: # MM:SS format
        minutes, seconds = parts
        hours = 0
    elif len(parts) == 3: # HH:MM:SS format
        hours, minutes, seconds = parts
    else:
        raise ValueError("Timestamp must be in HH:MM:SS or MM:SS format")

    try:
        hours = int(hours) if hours else 0
        minutes = int(minutes)
        seconds = float(seconds) # Allow decimal seconds

        if minutes >= 60 or seconds >= 60:
            raise ValueError("Minutes and seconds must be less than 60")
        
        if hours < 0 or minutes < 0 or seconds < 0:
            raise ValueError("Time values cannot be negative")
        
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    
    except ValueError:
        raise ValueError("Invalid timestamp format - ensure all parts are valid number")


# Extract frame based on timestamp input.
def extract_frame(vid_filename, timestamp_seconds, original_timestamp):
    """Extract frame from video at specific timestamp"""
    vid_path = os.path.join(vid_folder_path, vid_filename)
    frames_folder = os.path.join(vid_folder_path, 'frames')

    # Generate frame filename and path (using video filename instead of vid_id)
    timestamp_formatted = original_timestamp.replace(':', '_')
    frame_filename = f"{vid_filename}_frame_at_{timestamp_formatted}.png"
    frame_path = os.path.join(frames_folder, frame_filename)

    # Return existing frame if found
    if os.path.exists(frame_path):
        print(f"Frame already exists at {frame_path}")
        return {
            'frame_path': frame_path,
            'frame_filename': frame_filename
        }

    # Proceed with extraction if frame doesn't exist
    if not os.path.exists(vid_path):
        print(f"Video {vid_filename} not found")
        return None
    
    # Open video
    cap = cv2.VideoCapture(vid_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    if timestamp_seconds > duration:
        cap.release()
        print(f"Timestamp {timestamp_seconds}s exceeds video duration {duration:.2f}s")
        return None

    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp_seconds * 1000)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(f"Could not extract frame at {timestamp_seconds} seconds")
        return None

    # Create frames folder if needed
    os.makedirs(frames_folder, exist_ok=True)

    # Save new frame
    success = cv2.imwrite(frame_path, frame)
    if success:
        print(f"Frame extracted and saved as {frame_path}")
        return {
            'frame_path': frame_path,
            'frame_filename': frame_filename
        }

    print("Failed to save frame")
    return None


# Extract code from frame.
def extract_code_from_frame(frame_path):
    try:
        # Load the image
        img = cv2.imread(frame_path)
        if img is None:
            raise Exception("Could not load image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect if it's a dark theme
        is_dark_theme = np.mean(gray) < 128
        
        if is_dark_theme:
            gray = cv2.bitwise_not(gray)
        
        # Apply thresholding
        _, processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Enhance for better OCR
        height, width = processed.shape
        processed = cv2.resize(processed, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)
        
        # Python-optimized OCR configuration
        config = (
            "--psm 6 "
            "--oem 3 "
            "-c preserve_interword_spaces=1 "
            "-c textord_tabfind_find_tables=0 "
        )
        
        # Extract text
        text = pytesseract.image_to_string(Image.fromarray(processed), config=config)
        
        # Process lines while preserving Python indentation
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            # Preserve leading whitespace (indentation) but clean trailing
            cleaned_line = line.rstrip()
            
            # Convert tabs to 4 spaces (Python standard)
            cleaned_line = cleaned_line.expandtabs(4)
            
            processed_lines.append(cleaned_line)
        
        # Join and apply Python-specific corrections
        result = '\n'.join(processed_lines)
        
        # Python keyword corrections
        python_keywords = {
            r'\bdef\b': 'def',
            r'\bclass\b': 'class',
            r'\bimport\b': 'import',
            r'\bfrom\b': 'from',
            r'\bif\b': 'if',
            r'\belif\b': 'elif',
            r'\belse\b': 'else',
            r'\btry\b': 'try',
            r'\bexcept\b': 'except',
            r'\bfinally\b': 'finally',
            r'\bfor\b': 'for',
            r'\bwhile\b': 'while',
            r'\breturn\b': 'return',
            r'\bprint\b': 'print',
            r'\bTrue\b': 'True',
            r'\bFalse\b': 'False',
            r'\bNone\b': 'None',
            r'\band\b': 'and',
            r'\bor\b': 'or',
            r'\bnot\b': 'not',
            r'\bin\b': 'in',
            r'\bis\b': 'is',
        }
        
        for pattern, replacement in python_keywords.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Fix operators and punctuation
        result = re.sub(r'\s*=\s*', ' = ', result)
        result = re.sub(r'\s*==\s*', ' == ', result)
        result = re.sub(r'\s*!=\s*', ' != ', result)
        result = re.sub(r'\s*:\s*', ':', result)
        result = re.sub(r'\s*,\s*', ', ', result)
        result = re.sub(r'\(\s*', '(', result)
        result = re.sub(r'\s*\)', ')', result)
        result = re.sub(r'\[\s*', '[', result)
        result = re.sub(r'\s*\]', ']', result)
        
        # Clean up excessive whitespace while preserving structure
        result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)
        result = result.strip()
        
        return result
        
    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")


# Clean extracted code using AI
def ai_response(ocr_text: str) -> Optional[object]:
    """
    Clean up OCR-extracted Python code using Groq AI.

    Args:
        ocr_text (str): The raw OCR-extracted code text

    Returns:
        Optional[object]: AI response or None if processing fails.
    """

    try:
        client = Groq(api_key=os.environ.get('GROQ_KEY'))

        if not client.api_key:
            raise ValueError("GROQ_KEY environment variable not set")

        # Construct prompt with the actual OCR text.

        user_prompt = f"""Clean up this OCR-extracted Python code and fix any syntax errors. Please correct common OCR mistakes like:
        - Missing colons after function/class definitions
        - Incorrect method names (e.g., 'init__' should be '__init__')
        - Variable names with spaces (e.g., 'full _ name' should be 'full_name')
        - Missing indentation and line breaks
        - Misrecognized characters

        Return only the corrected Python code:

        This is the extracted Python code:
        "{ocr_text}" """

        response = client.chat.completions.with_raw_response.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that cleans and corrects Python code extracted from OCR. Return only the corrected code without explanations or markdown formatting."
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.1,
            max_completion_tokens=1024,
            top_p=0.9,
            stream=False,
            stop=None,
        )

        # Extract the cleaned code
        cleaned_code = response.parse().choices[0].message.content.strip()
        
        # Get information about API rate limits.
        headers = response.headers

        if cleaned_code.startswith('```python'):
            cleaned_code = cleaned_code.replace('```python', '')
        
        if cleaned_code.endswith('```'):
            cleaned_code = cleaned_code.replace('```', '')

        return {
            'cleaned_code': cleaned_code,
            'daily_requests_remaining': headers.get("x-ratelimit-remaining-requests"),
            'request_reset_time': headers.get("x-ratelimit-reset-requests")
            }

    except Exception as e:
        print(f"Error cleaning code with Groq AI: {str(e)}")
        return None

    