import sys
import textwrap
import urllib.parse
from pathlib import Path
from typing import List, Optional

import attr
import cli_ui as ui
import docopt

import tbump
import tbump.config
import tbump.git
import tbump.init
from tbump.config import Config
from tbump.executor import Executor
from tbump.file_bumper import FileBumper
from tbump.git_bumper import GitBumper
from tbump.hooks import HooksRunner

TBUMP_VERSION = "6.2.0"

USAGE = textwrap.dedent(
    """
Usage:
  tbump [options] <new_version>
  tbump [options] init <current_version>
  tbump --help
  tbump --version

Options:
   -h --help          Show this screen.
   -v --version       Show version.
   -C --cwd=<path>    Set working directory to <path>.
   --non-interactive  Never prompt for confirmation. Useful for automated scripts.
   --dry-run          Only display the changes that would be made.
   --only-patch       Only patches files, skipping any git operations or hook commands.
"""
)


class InvalidConfig(tbump.Error):
    def __init__(
        self,
        io_error: Optional[IOError] = None,
        parse_error: Optional[Exception] = None,
    ):
        super().__init__()
        self.io_error = io_error
        self.parse_error = parse_error

    def print_error(self) -> None:
        if self.io_error:
            ui.error("Could not read config file:", self.io_error)
        if self.parse_error:
            ui.error("Invalid config:", self.parse_error)


class Cancelled(tbump.Error):
    def print_error(self) -> None:
        ui.error("Cancelled by user")


@attr.s
class BumpOptions:
    working_path = attr.ib()  # type: Path
    new_version = attr.ib()  # type: str
    interactive = attr.ib(default=True)  # type: bool
    dry_run = attr.ib(default=False)  # type: bool
    only_patch = attr.ib(default=False)  # type: bool


def run(cmd: List[str]) -> None:
    opt_dict = docopt.docopt(USAGE, argv=cmd)
    if opt_dict["--version"]:
        print("tbump", TBUMP_VERSION)
        return

    # when running `tbump init` (with current_version missing),
    # docopt thinks we are runnig `tbump` with new_version = "init"
    # bail out early in this case
    if opt_dict["<new_version>"] == "init":
        sys.exit(USAGE)

    if opt_dict["--cwd"]:
        working_path = Path(opt_dict["--cwd"])
    else:
        working_path = Path.cwd()

    if opt_dict["init"]:
        current_version = opt_dict["<current_version>"]
        tbump.init.init(working_path, current_version=current_version)
        return

    new_version = opt_dict["<new_version>"]
    bump_options = BumpOptions(working_path=working_path, new_version=new_version)
    if opt_dict["--dry-run"]:
        bump_options.dry_run = True
    if opt_dict["--non-interactive"]:
        bump_options.interactive = False
    if opt_dict["--only-patch"]:
        bump_options.only_patch = True
    bump(bump_options)


def parse_config(working_path: Path) -> Config:
    tbump_path = working_path / "tbump.toml"
    try:
        config = tbump.config.parse(tbump_path)
    except IOError as io_error:
        raise InvalidConfig(io_error=io_error)
    except Exception as parse_error:
        raise InvalidConfig(parse_error=parse_error)
    return config


def bump(options: BumpOptions) -> None:
    working_path = options.working_path
    new_version = options.new_version
    interactive = options.interactive
    only_patch = options.only_patch
    dry_run = options.dry_run

    config = parse_config(options.working_path)

    # fmt: off
    ui.info_1(
        "Bumping from", ui.bold, config.current_version,
        ui.reset, "to", ui.bold, new_version,
    )
    # fmt: on

    git_bumper = GitBumper(working_path)
    git_bumper.set_config(config)
    git_state_error = None
    try:
        git_bumper.check_dirty()  # Avoid data loss
        if not only_patch:
            git_bumper.check_branch_state(new_version)
    except tbump.git.GitError as e:
        if dry_run:
            git_state_error = e
        else:
            raise

    file_bumper = FileBumper(working_path)
    file_bumper.set_config(config)

    hooks_runner = HooksRunner(working_path, config.current_version)
    if not only_patch:
        for hook in config.hooks:
            hooks_runner.add_hook(hook)

    executor = Executor(new_version, file_bumper)
    if not only_patch:
        executor.add_git_and_hook_actions(new_version, git_bumper, hooks_runner)

    if interactive:
        executor.print_self(dry_run=True)
        if not dry_run:
            proceed = ui.ask_yes_no("Looking good?", default=False)
            if not proceed:
                raise Cancelled()

    if dry_run:
        if git_state_error:
            ui.error("Git repository state is invalid")
            git_state_error.print_error()
            sys.exit(1)
        else:
            return

    executor.print_self(dry_run=False)
    executor.run()

    if config.github_url:
        tag_name = git_bumper.get_tag_name(new_version)
        suggest_creating_github_release(config.github_url, tag_name)


def suggest_creating_github_release(github_url: str, tag_name: str) -> None:
    query_string = urllib.parse.urlencode({"tag": tag_name})
    if not github_url.endswith("/"):
        github_url += "/"
    full_url = github_url + "releases/new?" + query_string
    ui.info()
    ui.info("Note: create a new release on GitHub by visiting:")
    ui.info(ui.tabs(1), full_url)


def main(args: Optional[List[str]] = None) -> None:
    # Supress backtrace if exception derives from tbump.Error
    if not args:
        args = sys.argv[1:]
    try:
        run(args)
    except tbump.Error as error:
        error.print_error()
        sys.exit(1)
