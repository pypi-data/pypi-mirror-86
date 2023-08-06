import json
import os
import tempfile
from zipfile import ZipFile

from .posterior_database import PosteriorDatabase
from .util import drop_keys


class Dataset:
    def __init__(self, name: str, posterior_db: PosteriorDatabase):
        self.name = name
        self.posterior_db = posterior_db
        full_information = self.posterior_db.get_data_info(name=self.name)
        self.information = drop_keys(full_information, "data_file")

    def file_path(self):
        data = self.values()
        # make a temp file with unzipped data
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(data, f)
            file_name = f.name
        return file_name

    def values(self):
        # unzip the file on the fly
        # return contents
        path = self.posterior_db.get_dataset_path(self.name)
        with ZipFile(path) as zipfile:
            namelist = zipfile.namelist()
            n_archives = len(namelist)
            if n_archives != 1:
                raise ValueError(
                    f"Expected a zip archive that contains one file, {path} has {n_archives} files in it"
                )
            archive_file_name = namelist[0]
            with zipfile.open(archive_file_name) as f:
                data = json.load(f)
        return data
