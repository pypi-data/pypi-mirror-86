from enum import Enum
from typing import Optional, Sequence


class Config:
    """
    Global configuration.

    :param helm_bin: path of the ```helm``` executable
    :param kube_version: Kubernetes version used as ```Capabilities.KubeVersion.Major/Minor```
    :param api_versions: Kubernetes api versions used for ```Capabilities.APIVersions```
    :param sort_objects: whether to sort Kubernetes objects returned from Helm
    :param parse_list_resource: whether to parse ```List``` Kubernetes resource and process each
        item separatelly. See `Any official docs around Kind: List? <https://github.com/kubernetes/kubectl/issues/837>`_.
    """
    helm_bin: str
    kube_version: Optional[str]
    api_versions: Optional[Sequence[str]]
    sort: bool
    parse_list_resource: bool

    def __init__(self, helm_bin: str = 'helm', kube_version: Optional[str] = None,
                 api_versions: Optional[Sequence[str]] = None, sort_objects: bool = False,
                 parse_list_resource: bool = True):
        self.helm_bin = helm_bin
        self.kube_version = kube_version
        self.api_versions = api_versions
        self.sort = sort_objects
        self.parse_list_resource = parse_list_resource


class BoolFilter(Enum):
    """
    Filter to use for boolean options.
    """
    ALL = 0
    IF_TRUE = 1
    IF_FALSE = 2
