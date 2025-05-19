# Video Upscaler

A Python-based video upscaler that uses deep learning to enhance video quality. This tool can upscale low-resolution videos (360p, 480p) to Full HD (1080p), 2K, 4K, or any other resolution while maintaining good quality.

## Overview

This upscaler provides a comprehensive solution for video enhancement:

1. **High-Quality Video Upscaling**:
   - Upscales videos to any resolution (default 1080p)
   - Supports 2K (1440p) and 4K (2160p) resolutions
   - Maintains aspect ratio
   - Uses deep learning (ESPCN model) for better quality
   - Applies Lanczos interpolation for final resizing

2. **Audio Preservation**:
   - Preserves all audio tracks from the original video
   - Maintains original audio quality and format
   - Supports multiple audio streams (languages, commentary, etc.)
   - Keeps subtitles and other streams

3. **User-Friendly Features**:
   - Progress bar to track the upscaling process
   - Automatic model download
   - GPU acceleration when available
   - Temporary file cleanup

## Features

- Uses ESPCN (Efficient Sub-Pixel Convolutional Network) model for high-quality upscaling
- Maintains aspect ratio during upscaling
- Supports various input video formats
- Preserves all audio tracks and streams
- Progress bar to track upscaling progress
- GPU acceleration when available
- Automatic cleanup of temporary files
- Customizable target resolution (1080p, 2K, 4K, etc.)

## Requirements

- Python 3.9 or higher
- FFmpeg (for audio handling)
- CUDA-capable GPU (optional, but recommended for faster processing)

## Installation

1. Install FFmpeg (if not already installed):
```bash
# On macOS
brew install ffmpeg

# On Ubuntu/Debian
sudo apt-get install ffmpeg

# On Windows
# Download from https://ffmpeg.org/download.html
```

2. Clone this repository:
```bash
git clone <repository-url>
cd upscaler
```

3. Create and activate a virtual environment:
```bash
python3.9 -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python upscaler.py
```

2. When prompted, enter the path to your input video file.

3. The upscaled video will be saved in the same directory as the input video with "_upscaled" added to the filename.

### Customizing Target Resolution

To upscale to a different resolution, you can modify the `target_height` parameter in the code. Common resolutions are:

- 1080p (Full HD): 1080 pixels height
- 1440p (2K): 1440 pixels height
- 2160p (4K): 2160 pixels height

To change the target resolution, modify the `upscale_video` call in the `main()` function:

```python
# For 2K (1440p)
upscaler.upscale_video(str(input_path), str(output_path), target_height=1440)

# For 4K (2160p)
upscaler.upscale_video(str(input_path), str(output_path), target_height=2160)
```

The width will be automatically calculated to maintain the original aspect ratio.

## How it Works

The upscaler uses a combination of deep learning-based super-resolution and traditional upscaling techniques:

1. The ESPCN model is used for the initial upscaling
2. Multiple upscaling passes are applied if needed to reach the target resolution
3. Lanczos interpolation is applied for final resizing to ensure smooth results
4. FFmpeg is used to merge the upscaled video with all original audio tracks
5. The process maintains the original aspect ratio while reaching the target resolution

## Notes

- Processing time depends on your hardware, video length, and target resolution
- Higher resolutions (2K, 4K) will require more processing time and memory
- GPU acceleration is automatically enabled if a CUDA-capable GPU is available
- The output video is saved in MP4 format using the H.264 codec
- All audio tracks from the original video are preserved
- Temporary files are automatically cleaned up after processing

## License

This project is licensed under the MIT License - see the LICENSE file for details.