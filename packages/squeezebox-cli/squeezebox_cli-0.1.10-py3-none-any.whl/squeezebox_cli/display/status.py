from itertools import count
from tabulate import tabulate


def format_status(status):
    text = (f"[{status['name']}] <{status['mode']}>"
            f" vol:{status['volume']}/100"
            f" {status['playlist_cur_index']+1}/{len(status['playlist'])}"
            f" {status['playlist'][status['playlist_cur_index']][1]}")
    try:
        text += (
            f" [>>{status['playlist'][status['playlist_cur_index']+1][1]}]")
    except IndexError:
        pass
    return text


def format_playlist(playlist, cur_index, max_tracks=None):
    if max_tracks is None or max_tracks >= len(playlist):
        start = 0
        indices = count(0)
    else:
        start = min(max(0, cur_index - 1), len(playlist) - max_tracks)
        indices = range(start, start + max_tracks)
    tracks = [('>>>' if i == cur_index else '',
               i, t['title'], t['album'], t['artist'])
              for i, t in zip(indices, playlist[start:])]
    if start > 0:
        tracks = [(f'[-{start}]',)] + tracks
    if max_tracks and start + max_tracks < len(playlist):
        tracks.append((f'[+{len(playlist) - (start + max_tracks)}]',))
    return tabulate(
            tracks,
            headers=['   ', 'index', 'title', 'album', 'artist'])
