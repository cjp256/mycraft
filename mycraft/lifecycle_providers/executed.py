import pathlib
from typing import Dict, List

from xcraft.providers.executed_provider import ExecutedProvider


class MycraftExecutedProvider:
    """Manages the lifecycle of a project."""

    def __init__(
        self,
        *,
        env_provider: ExecutedProvider,
        env_artifacts_dir: pathlib.Path = pathlib.Path("/root/mycraft-artifacts"),
        env_project_dir: pathlib.Path = pathlib.Path("/root/mycraft-project"),
        host_project_dir: pathlib.Path,
    ) -> None:
        self.env_provider = env_provider
        self.env_artifacts_dir = env_artifacts_dir
        self.env_project_dir = env_project_dir
        self.host_project_dir = host_project_dir

    def _run(self, command: List[str]):
        return self.env_provider.executor.execute_run(
            command, env=self._run_env(), cwd=self._run_cwd()
        )

    def _run_env(self) -> Dict[str, str]:
        return {
            "MYCRAFT_BUILD_ENVIRONMENT": "host",
            "PATH": "/snap/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        }

    def _run_cwd(self) -> str:
        return self.env_project_dir.as_posix()

    def setup(self) -> None:
        """Run any required setup prior to executing lifecycle steps."""
        self.env_provider.executor.sync_to(
            source=self.host_project_dir, destination=self.env_project_dir
        )

    def pull(self, *, parts: List[str]) -> None:
        """Run pull phase."""
        self._run(["mycraft", "pull", *parts])

    def catalog(self) -> None:
        """Run pull phase."""
        self._run(["mycraft", "catalog"])

    def craft(self) -> List[pathlib.Path]:
        """Craft project, executing lifecycle steps as required.

        Write output snaps to host project directory.

        :param output_dir: Directory to write snaps to.

        :returns: Path to snap(s) created from build.
        """
        self._run(["mycraft", "craft", "--output", self.env_artifacts_dir.as_posix()])
        return []

    def clean_parts(self, *, parts: List[str]) -> None:
        """Clean specified parts.

        :param parts: List of parts to clean.
        """
        self._run(["mycraft", "clean", *parts])

    def clean(self) -> None:
        """Clean all artifacts of project and build environment.

        Purges all artifacts from using the provider to build the
        project.  This includes build-instances (containers/VMs) and
        associated metadata and records.

        This does not include any artifacts that have resulted from
        a call to snap(), i.e. snap files or build logs.
        """
        self.env_provider.clean()
