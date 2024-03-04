import track_info
import models.sheet as sheet


def send_video_url(
    track: str
) -> str:
    
    track_name, track_id = track_info.search(track)
    if track_name is None:
        return '`Input error: No track found`'

    return sheet.fetch_video_url(track_id)