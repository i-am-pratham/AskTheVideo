"""
Handles fetching YouTube video transcripts.
This is the only file that talks to youtube-transcript-api —
if that library's interface changes again, this is the only
place that needs updating.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import(
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

def get_transcript(video_id : str, languages=("en",))-> str:
    """
     Fetches a YouTube transcript and returns it as one plain-text string.

    Args:
        video_id: the YouTube video ID (not the full URL)
        languages: preferred caption languages, in priority order

    Returns:
        The full transcript as a single string.

    Raises:
        RuntimeError: with a clear, specific message for each failure case.
    
    """
    ytt_api=YouTubeTranscriptApi()

    try:

        fetched= ytt_api.fetch(video_id, languages=list(languages))

        transcript= " ".join(snippet.text for snippet in fetched)
        return transcript
    
    except TranscriptsDisabled:
        raise RuntimeError("Captions are disabled for this video.")
    
    except NoTranscriptFound:
        raise RuntimeError(f"No transcript found in languages: {languages}")
    
    except VideoUnavailable:
        raise RuntimeError(
            "Video is unavailable (private, deleted, or region-locked)."
        )

    except Exception as e:
        raise RuntimeError(
            f"Transcript fetch failed ({e}). If this happens consistently, "
            "it may be YouTube blocking the server's IP — consider a proxy "
            "or a hosted transcript API as fallback."
        )
