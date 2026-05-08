import ffmpeg
from pathlib import Path

def convert_with_ffmpeg_python(input_file: str, output_file: str = None):
    if output_file is None:
        output_file = Path(input_file).with_suffix('.mp4')
    
    try:
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, str(output_file), vcodec='copy', acodec='copy', movflags='+faststart')
        ffmpeg.run(stream, overwrite_output=True)
        print(f"Success: {output_file}")
    except ffmpeg.Error as e:
        print("Error:", e.stderr.decode())

convert_with_ffmpeg_python("J:\Zona Downloads\Invincible S04\Invincible S04E05-00.41.22.397-00.45.51.958.mkv")