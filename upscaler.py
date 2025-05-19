import cv2
import numpy as np
from tqdm import tqdm
import os
from pathlib import Path
import ffmpeg
import tempfile
import shutil

class VideoUpscaler:
    def __init__(self):
        """Initialize the video upscaler"""
        self.model = self._load_model()

    def _load_model(self):
        """Load the super-resolution model"""
        # Create DNN Super Resolution object
        sr = cv2.dnn_superres.DnnSuperResImpl_create()

        # Download the model if it doesn't exist
        model_path = "weights/ESPCN_x2.pb"
        if not os.path.exists(model_path):
            os.makedirs("weights", exist_ok=True)
            import urllib.request
            print("Downloading super-resolution model...")
            urllib.request.urlretrieve(
                "https://github.com/fannymonori/TF-ESPCN/raw/master/export/ESPCN_x2.pb",
                model_path
            )

        # Read and set the model
        sr.readModel(model_path)
        sr.setModel("espcn", 2)  # Set the model name and scale factor
        return sr

    def upscale_video(self, input_path, output_path, target_height=1080):
        """
        Upscale a video to the target resolution
        Args:
            input_path (str): Path to input video
            output_path (str): Path to save upscaled video
            target_height (int): Target height in pixels
        """
        # Create a temporary directory for intermediate files
        temp_dir = tempfile.mkdtemp()
        temp_video = os.path.join(temp_dir, "temp_video.mp4")

        try:
            # Open input video
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {input_path}")

            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Calculate new dimensions maintaining aspect ratio
            scale_factor = target_height / height
            new_width = int(width * scale_factor)
            new_height = target_height

            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_video, fourcc, fps, (new_width, new_height))

            # Process frames
            with tqdm(total=total_frames, desc="Upscaling video") as pbar:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Upscale frame
                    try:
                        # First upscale using the model
                        upscaled_frame = self.model.upsample(frame)

                        # Apply additional upscaling if needed
                        while upscaled_frame.shape[0] < new_height:
                            upscaled_frame = self.model.upsample(upscaled_frame)

                        # Then resize to target dimensions if needed
                        if upscaled_frame.shape[0] != new_height or upscaled_frame.shape[1] != new_width:
                            upscaled_frame = cv2.resize(upscaled_frame, (new_width, new_height),
                                                      interpolation=cv2.INTER_LANCZOS4)
                    except Exception as e:
                        print(f"Error upscaling frame: {str(e)}")
                        # If upscaling fails, use basic resize
                        upscaled_frame = cv2.resize(frame, (new_width, new_height),
                                                  interpolation=cv2.INTER_LANCZOS4)

                    # Write frame
                    out.write(upscaled_frame)
                    pbar.update(1)

            # Release resources
            cap.release()
            out.release()

            # Merge video with original audio using ffmpeg
            print("\nMerging video with original audio...")
            try:
                # Get all audio streams from the original video
                probe = ffmpeg.probe(input_path)
                audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']

                # Build ffmpeg command
                stream = ffmpeg.input(temp_video)
                audio_input = ffmpeg.input(input_path)

                # Create the output stream with all audio tracks
                output_args = {
                    'vcodec': 'copy',
                    'acodec': 'copy'
                }

                # Add mapping for video stream
                stream = ffmpeg.output(stream, audio_input.audio, output_path, **output_args)

                # Add mapping for each audio stream
                for i in range(len(audio_streams)):
                    stream = stream.global_args('-map', '0:v', '-map', f'1:a:{i}')

                # Run ffmpeg command
                ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
                print("Audio merging complete!")

            except ffmpeg.Error as e:
                print(f"Error merging audio: {str(e.stderr.decode())}")
                # If ffmpeg fails, just copy the video without audio
                shutil.copy2(temp_video, output_path)
                print("Warning: Could not merge audio. Output video will be without audio.")

        finally:
            # Clean up temporary files
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

def main():
    # Example usage
    upscaler = VideoUpscaler()

    # Get input video path from user
    input_path = input("Enter the path to your input video: ")
    if not os.path.exists(input_path):
        print("Error: Input file does not exist!")
        return

    # Create output path
    input_path = Path(input_path)
    output_path = input_path.parent / f"{input_path.stem}_upscaled{input_path.suffix}"

    # Upscale video
    try:
        upscaler.upscale_video(str(input_path), str(output_path))
        print(f"\nUpscaling complete! Output saved to: {output_path}")
    except Exception as e:
        print(f"Error during upscaling: {str(e)}")

if __name__ == "__main__":
    main()