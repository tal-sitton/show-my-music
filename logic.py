from dataclasses import dataclass

from winsdk.windows.media import MediaPlaybackType
from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.storage import streams
from winsdk.windows.storage.streams import IRandomAccessStreamReference


@dataclass
class MediaInfo:
    """
    Data class to represent media information
    """
    album_artist: str
    album_title: str
    album_track_count: int
    artist: str
    genres: list
    playback_type: MediaPlaybackType
    subtitle: int
    thumbnail: bytes
    title: str
    track_number: int
    current_position: int
    length: int


async def get_image(image: IRandomAccessStreamReference) -> bytes:
    """
    Asynchronously retrieves image data from an IRandomAccessStreamReference
    """
    stream = await image.open_read_async()
    data_reader = streams.DataReader(stream.get_input_stream_at(0))
    await data_reader.load_async(stream.size)
    data = bytearray(stream.size)
    data_reader.read_bytes(data)
    return bytes(data)


# Asynchronously retrieve media information for the specified target program
async def get_media_info(target_program: str) -> MediaInfo:
    """
    Asynchronously retrieves media information for the specified target program.
    """
    # Request the media manager for active media sessions
    media_manager = await MediaManager.request_async()
    active_sessions = media_manager.get_sessions()

    # Iterate through active media sessions to find the target program
    for session in active_sessions:
        # Check if the target program matches the current session
        if target_program.lower() not in session.source_app_user_model_id.lower():
            continue

        # Retrieve media properties asynchronously
        info = await session.try_get_media_properties_async()

        # Convert media properties to a dictionary
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        # Retrieve thumbnail image data if available
        if info.thumbnail:
            image = await get_image(info.thumbnail)
        else:
            image = None

        info_dict['thumbnail'] = image

        # Calculate current position and length of the media session
        info_dict['current_position'] = session.get_timeline_properties().position.total_seconds()
        info_dict['length'] = session.get_timeline_properties().end_time.total_seconds()

        # Convert genres to a list
        info_dict['genres'] = list(info_dict['genres'])

        # Create and return a MediaInfo object using the gathered information
        return MediaInfo(**info_dict)

    # Raise an exception if the target program is not the current media session
    raise Exception('TARGET_PROGRAM is not the current media session')
