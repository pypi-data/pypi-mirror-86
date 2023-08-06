
"""
Registry for GitHub event handlers.
"""

import datetime
import fnmatch
import logging
import sys
import threading
import typing as t
from dataclasses import dataclass, field
import requests
from . import __version__
from .event import Event
from .token import InstallationTokenSupplier, JwtSupplier, TokenInfo

T = t.TypeVar('T')
logger = logging.getLogger(__name__)
user_agent = f'python/{sys.version.split()[0]} github-bot-api/{__version__}'

if t.TYPE_CHECKING:
  import github


@dataclass
class GithubApp:

  PUBLIC_GITHUB_V3_API_URL = 'https://api.github.com'

  #: User agent of the application. This will be respected in #get_user_agent().
  user_agent: str

  #: GitHub Application ID.
  app_id: int

  #: RSA private key to sign the JWT with.
  private_key: str

  #: GitHub API base URL. Defaults to the public GitHub API.
  v3_api_url: str = PUBLIC_GITHUB_V3_API_URL

  def __post_init__(self):
    self._jwt_supplier = JwtSupplier(self.app_id, self.private_key)
    self._lock = threading.Lock()
    self._installation_tokens: t.Dict[int, InstallationTokenSupplier] = {}

  def get_user_agent(self, installation_id: t.Optional[int] = None) -> str:
    """
    Create a user agent string for the PyGithub client, for an installation if the ID is
    specified.
    """

    user_agent = f'{self.user_agent} PyGithub/python (app_id={self.app_id}'
    if installation_id:
      user_agent += f', installation_id={installation_id})'
    return user_agent

  @property
  def jwt(self) -> TokenInfo:
    return self._jwt_supplier()

  @property
  def jwt_supplier(self) -> JwtSupplier:
    return JwtSupplier(self.app_id, self.private_key)

  @property
  def client(self) -> 'github.Github':
    assert github is not None
    return github.Github(
      jwt=self.jwt.value,
      base_url=self.v3_api_url,
      user_agent=self.get_user_agent())

  def __requestor(self, auth_header: str, installation_id: int) -> t.Dict[str, str]:
    return requests.post(
      self.v3_api_url.rstrip('/') + f'/app/installations/{installation_id}/access_tokens',
      headers={'Authorization': auth_header, 'User-Agent': user_agent},
    ).json()

  def get_installation_token_supplier(self, installation_id: int) -> InstallationTokenSupplier:
    with self._lock:
      return self._installation_tokens.setdefault(
        installation_id,
        InstallationTokenSupplier(
          self._jwt_supplier,
          installation_id,
          self.__requestor,
        )
      )

  def installation_token(self, installation_id: int) -> TokenInfo:
    return self.get_installation_token_supplier(installation_id)()

  def installation_client(self, installation_id: int) -> 'github.Github':
    assert github is not None
    return github.Github(
      login_or_token=self.installation_token(installation_id).value,
      base_url=self.v3_api_url,
      user_agent=self.get_user_agent(installation_id))
