"""
Handles fetching YouTube video transcripts via the Supadata API.
Using a hosted transcript API instead of scraping YouTube directly
avoids cloud-IP blocking entirely, since Supadata's servers do the
fetching, not ours.
"""
import requests
import config

SUPADATA_URL = "https://api.supadata.ai/v1/youtube/transcript"


def get_transcript(video_id: str, languages=("en",)) -> str:
    """
    Fetches a YouTube transcript via Supadata and returns it as one
    plain-text string.

    Args:
        video_id: the YouTube video ID (not the full URL)
        languages: preferred caption language (first one is used)

    Returns:
        The full transcript as a single string.

    Raises:
        RuntimeError: with a clear, specific message for each failure case.
    """
    params = {
        "videoId": video_id,
        "lang": languages[0],
        "text": "true",
    }
    headers = {"x-api-key": config.SUPADATA_API_KEY}

    try:
        response = requests.get(SUPADATA_URL, params=params, headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Transcript fetch failed (network error): {e}")

    if response.status_code == 404:
        raise RuntimeError("Video not found or is private.")
    elif response.status_code == 403:
        raise RuntimeError("Video requires authentication or is region-restricted.")
    elif response.status_code == 206:
        raise RuntimeError("Transcript unavailable for this video.")
    elif not response.ok:
        raise RuntimeError(
            f"Transcript fetch failed (HTTP {response.status_code}): {response.text}"
        )

    data = response.json()
    transcript = data.get("content", "")

    if not transcript:
        raise RuntimeError("No transcript content returned for this video.")

    return transcript