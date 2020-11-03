import pathlib
from typing import Dict, List

from xcraft.providers.provider import ExecutedProvider


class MycraftExecutedProvider:
    """Manages the lifecycle of a project."""

    def __init__(
        self,
        env_provider: ExecutedProvider,
        artifacts_dir: pathlib.Path = pathlib.Path("/root/mycraft-artifacts"),
        project_dir: pathlib.Path = pathlib.Path("/root/mycraft-project"),
    ) -> None:
        self.env_provider = env_provider
        self.artifacts_dir = artifacts_dir
        self.project_dir = project_dir

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
        return self.project_dir.as_posix()

    def pull(self, *, parts: List[str]) -> None:
        """Run pull phase."""
        self._run(["mycraft", "pull", *parts])

    def catalog(self) -> None:
        """Run pull phase."""
        self._run(["mycraft", "catalog"])

    def craft(self, output_dir: pathlib.Path) -> List[pathlib.Path]:
        """Craft project, executing lifecycle steps as required.

        Write output snaps to host project directory.

        :param output_dir: Directory to write snaps to.

        :returns: Path to snap(s) created from build.
        """
        self._run(["mycraft", "craft", "--output", self.artifacts_dir.as_posix()])
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
