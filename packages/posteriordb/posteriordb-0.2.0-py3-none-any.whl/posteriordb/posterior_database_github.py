import hashlib
import json
import os
import tempfile
from pathlib import Path
import requests


def temporary_no_assertions(x):
    return x


def get_requests(*args, n=3, **kwargs):
    for _ in range(n):
        try:
            response = requests.get(*args, **kwargs)
            if response.ok:
                break
        except Exception as e:
            print(e)
            continue
    else:
        print("response:", response.json())
        raise ValueError("response was not successful")
    return response


def github_pat():
    GITHUB_PAT = os.environ.get("GITHUB_PAT")
    headers = {}
    if GITHUB_PAT is not None:
        headers["Authorization"] = "token {}".format(GITHUB_PAT)
    else:
        print(
            "GitHub access token was not defined (env GITHUB_PAT not defined), using limited API rate limit."
        )
    return headers


def get_content(url, path=None, headers=None):
    """Download contents assuming GitHub API v3"""

    if headers is None:
        headers = github_pat()
    if path is not None:
        path = Path(path)
    verify = os.environ.get("REQUESTS_VERIFY", True)
    if str(verify).lower() in ("0", "false"):
        verify = False
    verify = bool(verify)

    response = get_requests(url, verify=verify, headers=headers)
    contents = {}

    for content in response.json():
        try:
            if content["type"] == "dir":
                contents.update(
                    get_content(content["_links"]["self"], path=path, headers=headers)
                )
            else:
                if path:
                    key = path / content["path"]
                else:
                    key = content["path"]
                contents[key] = content
        except Exception as e:
            print("Invalid content:", content, "Exception was raised (and ignored):", e)
            continue
    return contents


def download_file(url, path, overwrite=False, sha=None):
    """Download file with a requests.

    To manually disable requests verify
    set environmental variable REQUESTS_VERIFY to false.
    """
    if (not overwrite) and path.exists():
        return True
    if overwrite and (sha is not None) and path.exists():
        if sha == get_sha1_hash(path):
            return True

    verify = os.environ.get("REQUESTS_VERIFY", True)
    if str(verify).lower() in ("0", "false"):
        verify = False
    verify = bool(verify)

    headers = github_pat()
    try:
        response = get_requests(url, verify=verify, headers=headers)

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open(mode="wb") as f:
            f.write(response.content)
    except Exception as e:
        print("Exception was raised (and ignored):", e)
        return False
    return True


def get_sha1_hash(path):
    sha1_hash = hashlib.sha1()
    size = path.stat().st_size
    with path.open("rb") as f:
        sha1_hash.update(bytes("blob {}".format(size), encoding="utf-8") + b"\0")
        for byte_block in iter(lambda: f.read(4096), b""):
            sha1_hash.update(byte_block)
    return sha1_hash.hexdigest()


def load_json_file(path, metadata, overwrite=False):
    if not path.exists():
        if metadata is not None:
            download_file(metadata["download_url"], path)
        else:
            raise TypeError("File was not found in GitHub")
    elif overwrite:
        if metadata is not None:
            download_file(metadata["download_url"], path, sha=metadata["sha"])
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data


def load_info(path, assertion_function, metadata, overwrite=False):
    info = load_json_file(path, metadata, overwrite=overwrite)
    assertion_function(info)
    return info


def filenames_in_dir_no_extension(directory, gh_directory, extension):
    path = Path(directory)

    filenames = [p.with_suffix("").stem for p in path.glob("*" + extension)]
    gh_filenames = [p.with_suffix("").stem for p in gh_directory]
    return sorted(set(filenames + gh_filenames))


class PosteriorDatabaseGithub:
    def __init__(
        self,
        path: str = None,
        repo="MansMeg/posteriordb",
        ref="master",
        refresh=True,
        overwrite=False,
    ):
        if path is None:
            path = os.environ.get("POSTERIOR_DB_PATH")
            if path is None:
                path = Path.home() / ".posteriordb" / "posterior_database"
                path.mkdir(parents=True, exist_ok=True)
        self.path = Path(path)

        self.overwrite = overwrite
        self._repo = repo
        self._ref = ref

        self.refresh_url()

        self._progressbar_width = 30
        self._progressbar_marker = b"\xe2\x96\xa0".decode("utf-8")

        if refresh:
            self.refresh_github()
        else:
            self._links = {}

        # TODO assert that path is a valid posterior database

    def refresh_url(self, repo=None, ref=None):
        if repo is not None:
            self._repo = repo
        if ref is not None:
            self._ref = ref

        self._url = "https://api.github.com/repos/{repo}/contents/posterior_database?ref={ref}".format(
            repo=self._repo, ref=self._ref
        )

    def refresh_github(self):
        self._links = get_content(self._url, path=self.path.parent)

    def download_all(self, refresh=False, overwrite=None, show_progress=True):
        """Download all files for database."""
        if refresh:
            self.refresh_github()
        if overwrite is None:
            overwrite = self.overwrite
        n = len(self._links)
        for i, (path, metadata) in enumerate(self._links.items(), 1):
            print(
                "\rDownloading {:<30} ({}/{})".format(
                    self._progressbar_marker * int(i / n * self._progressbar_width),
                    i,
                    n,
                ),
                end="",
                flush=True,
            )
            download_file(
                metadata["download_url"], path, overwrite=overwrite, sha=metadata["sha"]
            )

    def full_path(self, path: str):
        return self.path / path

    def posterior(self, name):
        # inline import needed to avoid import loop
        from .posterior import Posterior

        return Posterior(name, self)

    def model(self, name):
        # inline import needed to avoid import loop
        from .model import Model

        return Model(name, self)

    def data(self, name):
        # inline import needed to avoid import loop
        from .dataset import Dataset

        return Dataset(name, self)

    def posterior_info_path(self, name: str):
        path = self.path / "posteriors" / (name + ".json")
        return path

    def get_posterior_info(self, name: str):
        path = self.posterior_info_path(name)
        return load_info(
            path,
            temporary_no_assertions,
            self._links.get(path),
            overwrite=self.overwrite,
        )

    def get_model_info(self, name: str):
        # load from the correct path
        file_name = name + ".info.json"
        path = self.path / "models" / "info" / file_name

        return load_info(
            path,
            temporary_no_assertions,
            self._links.get(path),
            overwrite=self.overwrite,
        )

    def get_data_info(self, name: str):
        file_name = name + ".info.json"
        path = self.path / "data" / "info" / file_name

        return load_info(
            path,
            temporary_no_assertions,
            self._links.get(path),
            overwrite=self.overwrite,
        )

    def get_reference_draws_path(self, name: str):
        reference_root = self.path / "reference_posteriors" / "draws" / "draws"
        reference_name = self.get_posterior_info(name).get("reference_posterior_name")
        assert reference_name is not None
        path = reference_root / (reference_name + ".json")
        return path

    def get_reference_draws_info(self, name: str):
        reference_root = self.path / "reference_posteriors" / "draws" / "info"
        reference_name = self.get_posterior_info(name).get("reference_posterior_name")
        assert reference_name is not None
        path = reference_root / (reference_name + ".info.json")
        return load_info(
            path,
            temporary_no_assertions,
            self._links.get(path, None),
            overwrite=self.overwrite,
        )

    def get_model_code_path(self, name, framework):
        model_info = self.get_model_info(name)
        path_within_posterior_db = model_info["model_implementations"][framework][
            "model_code"
        ]
        path = self.path / path_within_posterior_db

        # download model code
        if not path.exists() or self.overwrite:
            download_file(
                self._links[path]["download_url"],
                path,
                overwrite=self.overwrite,
                sha=self._links[path]["sha"],
            )

        return path

    def get_dataset_path(self, name):
        data_info = self.get_data_info(name)
        path = self.path / (data_info["data_file"] + ".zip")

        # download model code
        if not path.exists() or self.overwrite:
            download_file(
                self._links[path]["download_url"],
                path,
                overwrite=self.overwrite,
                sha=self._links[path]["sha"],
            )

        return path

    def posterior_names(self):
        directory = self.path / "posteriors"
        # walk directory, find json files
        # strip file extension
        gh_directory = [
            key for key in self._links if str(directory.resolve()) in str(key.resolve())
        ]
        return filenames_in_dir_no_extension(directory, gh_directory, ".json")

    def model_names(self):
        directory = self.path / "models" / "info"
        gh_directory = [
            key for key in self._links if str(directory.resolve()) in str(key.resolve())
        ]
        return filenames_in_dir_no_extension(directory, gh_directory, ".info.json")

    def dataset_names(self):
        directory = self.path / "data" / "info"
        gh_directory = [
            key for key in self._links if str(directory.resolve()) in str(key.resolve())
        ]
        return filenames_in_dir_no_extension(directory, gh_directory, ".info.json")

    def posteriors(self):
        names = self.posterior_names()
        # inline import needed to avoid import loop
        from .posterior import Posterior

        for name in names:
            yield Posterior(name, self)

    def models(self):
        names = self.model_names()
        # inline import needed to avoid import loop
        from .model import Model

        for name in names:
            yield Model(name, self)

    def datasets(self):
        names = self.dataset_names()
        # inline import needed to avoid import loop
        from .dataset import Dataset

        for name in names:
            yield Dataset(name, self)
