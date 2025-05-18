# Video Upscaler

A Python-based video upscaler that uses deep learning to enhance video quality. This tool can upscale low-resolution videos (360p, 480p) to Full HD (1080p) or higher while maintaining good quality.

## Features

- Uses state-of-the-art deep learning models (EDSR or ESPCN) for high-quality upscaling
- Maintains aspect ratio during upscaling
- Supports various input video formats
- Progress bar to track upscaling progress
- GPU acceleration when available

## Requirements

- Python 3.7 or higher
- CUDA-capable GPU (optional, but recommended for faster processing)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd upscaler
```

2. Install the required dependencies:
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

## How it Works

The upscaler uses a combination of deep learning-based super-resolution and traditional upscaling techniques:

1. The EDSR (Enhanced Deep Super Resolution) model is used for the initial upscaling
2. Lanczos interpolation is applied for final resizing to ensure smooth results
3. The process maintains the original aspect ratio while reaching the target resolution

## Notes

- Processing time depends on your hardware, video length, and target resolution
- GPU acceleration is automatically enabled if a CUDA-capable GPU is available
- The output video is saved in MP4 format using the H.264 codec

## License

This project is licensed under the MIT License - see the LICENSE file for details.