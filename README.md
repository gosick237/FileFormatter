# FileFormatter
Unified file name for my storage

1. prerequsite
 python3
 pip install pillow
2. getting start
 python .\fileFormatter.py {FOLDER_PATH}
 python .\fileFormatter.py .\resource
 python .\fileFormatter.py C:\Users\Tmax_YH\Desktop\FileFomatter\image

3. Prompt (GPT3.5):
    please make python code under below conditions :
    1. program description:
        reading images or video in given folder and change file name as the file name and file format.
    2. conditions :
        "Input argument" : "folder path",
        "main function" : "change name if input file name include text \"IMG\"",
        "file name form" : "{taken_date_of_photo}_{taken_time_of_photo}.{file_format}",
        "format change rule" : [
            "change file format into .jpg if file is image",
            "change file format into .mp4 if file is video"
        ],
        "format infomation": {
            "Image format list" : [jpg, jpeg, "HEIC"],
            "Video format list" : ["avi", "mp4", "mov", "HEVC"]
        }
        "limitation": [
            "use "DataTimeOriginal" attribute of file property for file name change, refering to EXIF information",
            "don't change scale or size of frame",
            "don't use pyheif, since pyheif doesn't support window",
            "make it put the Input argument at running source code"
        ],