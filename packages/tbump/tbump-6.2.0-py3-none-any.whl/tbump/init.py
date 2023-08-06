import textwrap
from pathlib import Path
from typing import List

import cli_ui as ui

import tbump.git


def find_files(working_path: Path, current_version: str) -> List[str]:
    ui.info_2("Looking for files matching", ui.bold, current_version)
    cmd = ["grep", "--fixed-strings", "--files-with-matches", current_version]
    _, out = tbump.git.run_git_captured(working_path, *cmd, check=True)
    res = []  # type: List[str]
    ui.info("Found following matching files")
    for file in out.splitlines():
        ui.info(" * ", file)
        res.append(file)
    return res


def init(working_path: Path, *, current_version: str) -> None:
    """ Interactively creates a new tbump.toml """
    ui.info_1("Generating tbump config file")
    tbump_path = working_path / "tbump.toml"
    if tbump_path.exists():
        ui.fatal(tbump_path, "already exists")
    template = textwrap.dedent(
        """\
        # Uncomment this if your project is hosted on GitHub:
        # github_url = https://github.com/<user or organization>/<project>/

        [version]
        current = "@current_version@"

        # Example of a semver regexp.
        # Make sure this matches current_version before
        # using tbump
        regex = '''
          (?P<major>\\d+)
          \\.
          (?P<minor>\\d+)
          \\.
          (?P<patch>\\d+)
          '''

        [git]
        message_template = "Bump to {new_version}"
        tag_template = "v{new_version}"
     """
    )

    file_template = textwrap.dedent(
        """
        # For each file to patch, add a [[file]] config section containing
        # the path of the file, relative to the tbump.toml location.
        [[file]]
        src = "..."
    """
    )

    hooks_template = textwrap.dedent(
        """
        # You can specify a list of commands to
        # run after the files have been patched
        # and before the git commit is made

        #  [[before_commit]]
        #  name = "check changelog"
        #  cmd = "grep -q {new_version} Changelog.rst"

        # Or run some commands after the git tag and the branch
        # have been pushed:
        #  [[after_push]]
        #  name = "publish"
        #  cmd = "./publish.sh"
    """
    )

    to_write = template.replace("@current_version@", current_version)
    to_write += file_template
    to_write += hooks_template
    tbump_path.write_text(to_write)
    ui.info_2(ui.check, "Generated tbump.toml")
