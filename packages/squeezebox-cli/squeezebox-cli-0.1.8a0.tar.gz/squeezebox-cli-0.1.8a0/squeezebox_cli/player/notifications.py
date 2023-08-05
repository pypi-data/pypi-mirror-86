from itertools import count

from squeezebox_cli.core.protocol import parse_tags
from squeezebox_cli.database import tracks
from squeezebox_cli.player import status


def pause_handler(player_status, msg, tn):
    if msg[1:3] == ['playlist', 'pause']:
        player_status['mode'] = 'pause' if msg[3] == '1' else 'play'
        return True
    return False


def play_handler(player_status, msg, tn):
    if msg[1] == 'play':
        player_status['mode'] = 'play'
        return True
    return False


def volume_handler(player_status, msg, tn):
    if msg[1:4] == ['prefset', 'server', 'volume']:
        player_status['volume'] = int(msg[4])
        return True
    return False


def newsong_handler(player_status, msg, tn):
    if msg[1:3] == ['playlist', 'newsong']:
        player_status.clear()
        player_status.update(status(tn, msg[0]))
        return True
    return False


def playlistcontrol_handler(player_status, msg, tn):
    if msg[1:3] == ['playlist', 'delete']:
        index = int(msg[3])
        del player_status['playlist'][index]
        if index < player_status['playlist_cur_index']:
            player_status['playlist_cur_index'] = \
                    player_status['playlist_cur_index'] - 1
        return True
    elif msg[1] == 'playlistcontrol':
        tags = dict(parse_tags(msg[2:]))
        try:
            ts = tracks(tn, track_id=int(tags['track_id']))
        except KeyError:
            try:
                ts = tracks(tn, album_id=int(tags['album_id']))
            except KeyError:
                ts = tracks(tn, artist_id=int(tags['artist_id']))

        def add():
            for t in ts:
                player_status['playlist'].append((t['id'], t['title']))

        def insert():
            for i, t in zip(
                    count(player_status['playlist_cur_index'] + 1), ts):
                player_status['playlist'].insert(i, (t['id'], t['title']))

        def load():
            player_status['playlist'] = [(t['id'], t['title']) for t in ts]
            player_status['playlist_cur_index'] = 0
            player_status['mode'] = 'play'

        try:
            dict(add=add, insert=insert, load=load)[tags['cmd']]()
            return True
        except KeyError:
            print(tags)
    return False
