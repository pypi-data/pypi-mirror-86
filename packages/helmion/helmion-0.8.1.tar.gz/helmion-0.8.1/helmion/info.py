import pathlib
import posixpath
import tarfile
from datetime import datetime
from io import BytesIO
from typing import Mapping, Any, Sequence, List, Dict, Optional

import requests
import semver
import yaml
from dateutil.parser import isoparse

from .config import Config
from .exception import NetworkError, ConfigurationError, InputOutputError
from .util import remove_prefix, is_absolute


class ChartVersionInfo:
    """
    Information for a version of a Helm chart.

    :param chart: chart info
    :param rawinfo: the chart version raw info
    :raises ConfigurationError: on chart configuration error
    """
    chart: 'ChartInfo'
    name: str
    version: str
    version_info: semver.VersionInfo
    description: str
    appVersion: Optional[str]
    digest: str
    home: str
    sources: List[str]
    urls: List[str]
    created: datetime
    rawinfo: Mapping[Any, Any]

    archiveFiles: Optional[Dict[Any, Any]]
    """Relevant archive files. Available after caling :func:`readArchiveFiles`"""

    _files: Optional[Dict[Any, Any]]

    def __init__(self, chart: 'ChartInfo', rawinfo: Mapping[Any, Any]):
        self.rawinfo = rawinfo
        self.chart = chart
        self.name = rawinfo['name']
        self.version = rawinfo['version']
        self.description = rawinfo['description']
        self.digest = rawinfo['digest']
        self.appVersion = rawinfo['appVersion'] if 'appVersion' in rawinfo else None
        self.home = rawinfo['home'] if 'home' in rawinfo else None
        self.sources = rawinfo['sources'] if 'sources' in rawinfo else None
        self.urls = rawinfo['urls'] if 'urls' in rawinfo else None
        if isinstance(rawinfo['created'], datetime):
            self.created = rawinfo['created']
        else:
            self.created = isoparse(rawinfo['created'])
        try:
            self.version_info = semver.VersionInfo.parse(remove_prefix(self.version, 'v'))
        except ValueError as e:
            raise ConfigurationError(str(e)) from e
        self.archiveFiles = None
        self._files = {}

    def fileUrl(self) -> str:
        """
        Returns the chart .tar.gz file absolute url.

        :return: chart file
        """
        if self.urls is None or len(self.urls) == 0:
            raise InputOutputError('Chart version does not have file urls')

        if is_absolute(self.urls[0]):
            return self.urls[0]
        return posixpath.join(self.chart.repository.url, self.urls[0])

    def fileOpen(self) -> tarfile.TarFile:
        """
        Opens the chart .tar.gz as a stream and returns a :class:`tar.TarFile` ready to use.
        No files are written on disk.

        :return: the open tar file
        :raises NetworkError: on network error
        :raises InputOutputError: on file IO error
        """
        try:
            r = response = requests.get(self.fileUrl(), stream=True)
            r.raise_for_status()
            return tarfile.open(fileobj=BytesIO(response.raw.read()), mode="r:gz")
        except requests.RequestException as e:
            raise NetworkError(str(e)) from e
        except tarfile.TarError as e:
            raise InputOutputError(str(e)) from e

    def getChartFile(self) -> Mapping[str, Any]:
        """
        Returns the parsed ```Chart.yaml``` file as a class:`Mapping`.

        :return: parsed file
        """
        return self._getFile('Chart.yaml')

    def getValuesFile(self) -> Mapping[str, Any]:
        """
        Returns the parsed ```values.yaml``` file as a class:`Mapping`.

        :return: parsed file
        """
        return self._getFile('values.yaml')

    def _getFile(self, name: str) -> Mapping[Any, Any]:
        """
        Returns the requested file as a class:`Mapping`.
        Only ```'Chart.yaml``` and ```values.yaml'`` are supported.

        :return: parsed file
        :raises NetworkError: on network error
        :raises InputOutputError: on file IO or parsing error
        """
        if name not in ['Chart.yaml', 'values.yaml']:
            raise InputOutputError('Unknown file: {}'.format(name))
        if name in self._files:
            return self._files[name]
        try:
            self._files[name] = yaml.load(self.readArchiveFiles().archiveFiles[name], Loader=yaml.SafeLoader)
            return self._files[name]
        except yaml.YAMLError as e:
            raise InputOutputError(str(e)) from e

    def readArchiveFiles(self) -> 'ChartVersionInfo':
        """
        Search the archive files for relevant files.

        Searched files are: ```['Chart.yaml', 'Chart.lock', 'values.yaml', 'values.schema.json']```.
        They can be accessed using :data:`archiveFiles` after calling this function.

        :return: the instance itself
        :raises InputOutputError: on file IO error
        """
        if self.archiveFiles is not None:
            return self
        archiveFiles = {}
        try:
            with self.fileOpen() as tar_file:
                for tarinfo in tar_file.getmembers():
                    if tarinfo.isreg():
                        parsename = pathlib.PurePosixPath(tarinfo.name)
                        if parsename.is_absolute():
                            raise InputOutputError('All files in chart archive must be relative')
                        basename = str(pathlib.PurePosixPath(*parsename.parts[1:]))
                        if basename in ['Chart.yaml', 'Chart.lock', 'values.yaml', 'values.schema.json']:
                            with tar_file.extractfile(tarinfo.name) as file:
                                archiveFiles[basename] = file.read().decode('utf-8')
        except tarfile.TarError as e:
            raise InputOutputError(str(e)) from e
        self.archiveFiles = archiveFiles
        return self


class ChartInfo:
    """
    Information for a Helm chart in a repository.

    :param repository: repository info
    :param name: chart name
    :param rawinfo: the chart raw info
    """
    repository: 'RepositoryInfo'
    name: str
    latest: Optional[ChartVersionInfo]
    versions: List[ChartVersionInfo]

    def __init__(self, repository: 'RepositoryInfo', name: str, rawinfo: Optional[Sequence[Any]] = None):
        self.repository = repository
        self.name = name
        self.latest = None
        self.versions = []
        self._parseRawInfo(rawinfo)

    def _parseRawInfo(self, rawinfo: Optional[Sequence[Any]] = None) -> None:
        """
        Parses the raw information.
        """
        if rawinfo is not None:
            for version in rawinfo:
                cversion = ChartVersionInfo(self, version)
                if self.latest is None or cversion.version_info > self.latest.version_info:
                    self.latest = cversion
                self.versions.append(cversion)
            sorted(self.versions, key=lambda x: x.version_info, reverse=True)

    def version(self, version: Optional[str]) -> Optional[ChartVersionInfo]:
        """
        Returns a chart version info.

        :param version: version to locate. If None, returns the latest version.
        :return: the chart version information, or None if not found
        """
        if version is None or version == "":
            return self.latest

        for r in self.versions:
            if r.version == version:
                return r
        return None


class RepositoryInfo:
    """
    Downloader for Helm repository info.

    All information is downloaded directly, there is no need for the ```helm``` executable.

    :param url: Helm repository url.
    :param config: Optional configuration.
    :param rawinfo: Optional raw repository info (index.yaml). If not provided, will be downloaded.

    :raises NetworkError: on network errors
    :raises InputOutputError: on parsing errors
    """
    config: Config
    url: str
    entries: Dict[str, ChartInfo]

    def __init__(self, url: str, config: Optional[Config] = None, rawinfo: Optional[Mapping[Any, Any]] = None):
        self.config = config if config is not None else Config()
        self.url = url

        if rawinfo is None:
            try:
                r = requests.get(posixpath.join(url, 'index.yaml'))
                r.raise_for_status()
                rawinfo = yaml.load(r.text, yaml.SafeLoader)
            except requests.RequestException as e:
                raise NetworkError(str(e)) from e
            except yaml.YAMLError as e:
                raise InputOutputError(str(e)) from e

        self.entries = {}
        self._parseRawInfo(rawinfo)

    def _parseRawInfo(self, rawinfo: Optional[Mapping[Any, Any]] = None) -> None:
        """
        Parses the raw information.
        """
        if rawinfo is not None:
            if 'entries' in rawinfo:
                for entryname, entry in rawinfo['entries'].items():
                    self.entries[entryname] = ChartInfo(self, entryname, entry)

    def chart(self, name: str) -> Optional[ChartInfo]:
        """
        Returns a chart by name.

        :param name: chart name
        :return: the chart information, of None if not found
        """
        if name in self.entries:
            return self.entries[name]
        return None

    def chartVersion(self, name: str, version: Optional[str] = None) -> Optional[ChartVersionInfo]:
        """
        Returns a chart version info.

        :param name: chart name
        :param version: version to locate. If None, returns the latest version.
        :return: the chart version information, or None if not found
        """
        chart = self.chart(name)
        if chart is not None:
            return chart.version(version)
        return None
