# import de back-end
from core.meta.repository.filtering import Filtering
from core.meta.repository.tasks import Task


# Estratégias de resolução por fase
def medium_strategy():
    return {
        'artist_for_search' : lambda song: Filtering.clean_feat(song.id3_data["filtered_data"].get("song_artist_id3_filtered")),
        'calculate_score' : lambda song, item: (
            0.6 * Task.similarity(
                song.id3_data["filtered_data"].get("title"),
                item['title']
            ) + 0.4 * max(
                Task.similarity(
                    Filtering.clean_feat(song.id3_data["filtered_data"].get("song_artist_id3_filtered")),
                    item['artist']['name']
                ),
                Task.similarity(
                    song.id3_data["original_data"].get("original_artist_id3"),
                    item['artist']['name']
                )
            )
        )
    }


def artist_filtered_strategy():
    return {
        'artist_for_search' : lambda song: Filtering.clean_feat(song.id3_data["filtered_data"].get("song_artist_id3_filtered")),
        'calculate_score' : lambda song, item: (
            0.6 * Task.similarity(
                song.id3_data["filtered_data"].get("title"),
                item['title']
            ) + 0.4 * Task.similarity(
                song.id3_data["filtered_data"].get("artist"),
                item['artist']['name']
            )
        )
    }


def artist_id3_strategy():
    return {
        'artist_for_search' : lambda song: song.id3_data["original_data"].get("original_artist_id3"),
        'calculate_score' : lambda song, item: (
            0.6 * Task.similarity(
                song.id3_data["filtered_data"].get("title"),
                item['title']
            ) + 0.4 * Task.similarity(
                song.id3_data["original_data"].get("artist_id3"),
                item['artist']['name']
            )
        )
    }


def _strategy_title_only():
    from core.meta.pipeline.helpers.analysis import calculate_score_title_only
    
    return {
        'artist_for_search' : lambda song: None,
        'calculate_score' : calculate_score_title_only
    }