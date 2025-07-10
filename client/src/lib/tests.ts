import type { FrameData } from "./dataTypes";

const originalData = [
    {
        frame_filename: '',
        frame_path: '',
        frame_url: '',
        message: '',
        timestamp: '00:05:30',
        timestamp_seconds: 330,
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
    },
    {
        frame_filename: '',
        frame_path: '',
        frame_url: '',
        message: '',
        timestamp: '00:05:30',
        timestamp_seconds: 330,
        video_filename: '',
        extracted_code: '',
        formatted_code: `
class Teacher:
    def __init__(self, full_name, birthday):
        self.name = full_name
        self.birthday = birthday  # yyyymmdd

teacher = Teacher("Dave Bowman", 19710315)
`
    },
    {
        frame_filename: '',
        frame_path: '',
        frame_url: '',
        message: '',
        timestamp: '00:05:30',
        timestamp_seconds: 330,
        video_filename: '',
        extracted_code: '',
        formatted_code: `
class Student:
    def __init__(self, full_name, birthday):
        self.name = full_name
        self.birthday = birthday  # yyyymmdd
`
    }
]

let dataCopy = [...originalData]

// Mock success API response
function successAPIResponse(): Promise<FrameData> {
    let response: FrameData

    if (dataCopy.length === 0) {
        dataCopy = [...originalData]
    }

    response = dataCopy.shift() as FrameData
    console.log(dataCopy)

    return new Promise((resolve, _) => {
        setTimeout(() => {
            resolve(response)
        }, 2000)
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

export { successAPIResponse, failAPIResponse }