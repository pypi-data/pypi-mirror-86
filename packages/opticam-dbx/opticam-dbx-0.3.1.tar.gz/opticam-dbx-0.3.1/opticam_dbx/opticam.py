import datetime
import logging
import os
import re

import dropbox

_log = logging.getLogger('opticam')


class AlarmVideoDownloader(object):
    def __init__(self, auth_token, dest_root_dir, remove_downloaded):
        super().__init__()

        self.dbx = dropbox.Dropbox(auth_token)
        self.dest_root_dir = dest_root_dir
        self.remove_downloaded = remove_downloaded

    def download(self, after_download=None):
        for file in self._get_alarm_video_files():
            downloaded_file_path = self._download_file(file)

            if self.remove_downloaded:
                _log.info(f'Removing file {file.path_lower} from Dropbox')
                self.dbx.files_delete(file.path_lower)

            if after_download:
                after_download(downloaded_file_path)

    def _download_file(self, file):
        timestamp_match = re.match(
            r'MDalarm_(?P<timestamp>\d{8}_\d{6}).*\.avi',
            file.name,
        )
        assert timestamp_match, f'{file.name} is unexpected.'

        recording_time = datetime.datetime.strptime(timestamp_match.group('timestamp'), '%Y%m%d_%H%M%S')

        dest_path = os.path.join(
            self.dest_root_dir,
            '{} {}.avi'.format(
                recording_time.strftime('%Y-%m-%d %H-%M-%S'),
                file.rev
            ),
        )
        dest_path = os.path.abspath(dest_path)

        if os.path.isfile(dest_path):
            _log.info(f'Removing existing downloaded file {dest_path}')
            os.remove(dest_path)

        elif os.path.exists(dest_path):
            raise AssertionError('File {dest_path} exists but is not a file')

        _log.info(f'Downloading file {file.name} into {dest_path}')
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        self.dbx.files_download_to_file(dest_path, file.path_lower)

        return dest_path

    def _get_alarm_video_files(self):
        files_list_result = self.dbx.files_list_folder(
            '/apps/ipcamera',
            include_media_info=True,
        )

        for entry in files_list_result.entries:
            if entry.name.endswith('.avi'):
                for revision in self.dbx.files_list_revisions(entry.path_lower).entries:
                    yield revision
