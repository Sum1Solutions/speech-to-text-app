# HIPAA-Compliant Voice-to-Text Transcription

This is a simple, local voice-to-text transcription tool that uses OpenAI's Whisper model to provide a HIPAA-compliant transcription solution. The application runs entirely on your local machine, ensuring that no audio data is sent to the cloud.

## Features

*   **Local Transcription:** All transcription is done locally, so your data remains private.
*   **GUI Interface:** A simple graphical interface allows you to record and transcribe audio with the click of a button.
*   **HIPAA Compliant:** By keeping all data on your local machine, this tool helps you meet HIPAA privacy requirements.

## Usage

1.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the application:
    ```bash
    python app.py
    ```

## Troubleshooting

### Blank Transcriptions

If you are getting blank or nonsensical transcriptions, it might be due to an issue with the audio recording format. This can happen if the audio is recorded in a format that is not compatible with the transcription model.

The application has been updated to address a known issue where the audio was recorded in 32-bit float format but the Whisper model expects 16-bit integer format. This mismatch resulted in corrupted audio files and blank transcriptions.

If you continue to experience issues, please ensure that your microphone is correctly configured and that the audio is being recorded in a compatible format.
