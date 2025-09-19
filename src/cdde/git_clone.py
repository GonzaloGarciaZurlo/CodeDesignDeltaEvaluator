"""
This module contains the GitClone class, 
which is used to create the before and after directories of a PR.
"""
import os
import subprocess
import shutil
from typing import Generator
from git import Repo


class GitClone:
    """
    Class that creates the before and after directories of a PR.
    """

    def __init__(self, repo_url: str, main_branch: str,
                 pr_number: int) -> None:
        """
        repo_url: The URL of the repository.
        pr_number: The number of the PR.
        main_branch: the branch you want to merge into. Default is master.
        """
        self.repo_url = repo_url
        self.pr_number = pr_number
        self.branch = main_branch
        self.work_dir = os.getcwd()
        self.repo_dir = os.path.join(self.work_dir, "repo-git")
        self.repo = None
        self.before_dir = ""
        self.after_dir = ""

    def run(self) -> tuple[str, str]:
        """
        Runs the process of cloning the repo and checking out the PR.
        """
        self._create_dirs()
        self._clone_repo()
        self._before_dir()
        self._after_dir()
        self._return_paths()
        return self.before_dir, self.after_dir

    def _create_dirs(self) -> None:
        """
        Creates the before and after directories,
        using mktemp to create a temporary directory.
        """
        os.makedirs(self.work_dir, exist_ok=True)
        self.before_dir = subprocess.run(
            ["mktemp", "-d", "before.XXXX", "-p", self.work_dir],
            capture_output=True,
            check=True).stdout.decode().strip()
        self.after_dir = subprocess.run(
            ["mktemp", "-d", "after.XXXX", "-p", self.work_dir],
            capture_output=True,
            check=True).stdout.decode().strip()

    def _clone_repo(self) -> None:
        """
        Clones the repository into the repo directory,
        using the gitpython library.
        """
        os.makedirs(self.repo_dir, exist_ok=True)
        shutil.rmtree(self.repo_dir)
        self.repo = Repo.clone_from(self.repo_url, self.repo_dir)

    def _before_dir(self) -> None:
        """
        Move repo snapshot using fetch and checkout.
        Later, it copies the repo to the before directory.
        """
        os.chdir(self.repo_dir)
        self.repo.git.fetch("origin", self.branch)
        self.repo.git.checkout(self.branch)
        shutil.copytree(self.repo_dir, self.before_dir, dirs_exist_ok=True)

    def _after_dir(self) -> None:
        """
        Move repo snapshot using fetch and checkout.
        Later, it copies the repo to the after directory.
        """
        os.chdir(self.repo_dir)
        self.repo.git.fetch("origin",
                            f"pull/{self.pr_number}/head:pr-{self.pr_number}")
        self.repo.git.checkout(f"pr-{self.pr_number}")
        shutil.copytree(self.repo_dir, self.after_dir, dirs_exist_ok=True)

    def _return_paths(self) -> None:
        """
        Brings back to the initial working directory.
        """
        os.chdir(self.work_dir)

    def delete_dir(self) -> None:
        """
        Deletes the before and after directories.
        """
        shutil.rmtree(self.before_dir)
        shutil.rmtree(self.after_dir)
        shutil.rmtree(self.repo_dir)


class TraverseGitLog:
    """
    Class that traverses the git log of a repository.
    """

    def __init__(self, repo_url: str, main_branch: str = "master") -> None:
        """
        repo_url: The URL of the repository.
        main_branch: the branch you want to merge into. Default is master.
        """
        self.repo_url = repo_url
        self.branch = main_branch
        self.git_log: list[str] = []
        self.work_dir = os.getcwd()
        self.repo_dir = os.path.join(self.work_dir, "git-log-traverse")
        self.repo = None
        self.before_dir = ""
        self.after_dir = ""

    def run(self) -> Generator[str, str, None]:
        """
        Runs the process of cloning all version of the repository.
        """
        self._clone_repo()
        self._set_git_log()
        if len(self.git_log) > 501:
            # set the maximum number of iterations
            iter_range = 500
        else:
            iter_range = len(self.git_log) - 1
        for n_commit in range(iter_range):
            self._create_dirs()
            self._before_dir(n_commit)
            self._after_dir(n_commit + 1)
            self._return_paths()
            yield self.before_dir, self.after_dir

    def _set_git_log(self) -> None:
        """
        Sets the git log for the repository.
        """
        self.git_log = [
            commit.hexsha for commit in self.repo.iter_commits(self.branch)
        ][::-1]

    def _clone_repo(self) -> None:
        """
        Clones the repository into the repo directory,
        using the gitpython library.
        """
        os.makedirs(self.repo_dir, exist_ok=True)
        shutil.rmtree(self.repo_dir)
        self.repo = Repo.clone_from(self.repo_url, self.repo_dir)

    def _create_dirs(self) -> None:
        """
        Creates the before and after directories,
        using mktemp to create a temporary directory.
        """
        os.makedirs(self.work_dir, exist_ok=True)
        self.before_dir = subprocess.run(
            ["mktemp", "-d", "before.XXXX", "-p", self.work_dir],
            capture_output=True,
            check=True).stdout.decode().strip()
        self.after_dir = subprocess.run(
            ["mktemp", "-d", "after.XXXX", "-p", self.work_dir],
            capture_output=True,
            check=True).stdout.decode().strip()

    def _before_dir(self, n_commit: int) -> None:
        """
        Move the before repo to specific commit.
        """
        os.chdir(self.repo_dir)
        self.repo.git.fetch("origin", self.branch)
        self.repo.git.checkout(self.git_log[n_commit])
        shutil.copytree(self.repo_dir, self.before_dir, dirs_exist_ok=True)
        self.repo.git.checkout(self.branch)

    def _after_dir(self, n_commit: int) -> None:
        """
        Move the after repo to specific commit.
        """
        os.chdir(self.repo_dir)
        self.repo.git.fetch("origin", self.branch)
        self.repo.git.checkout(self.git_log[n_commit])
        shutil.copytree(self.repo_dir, self.after_dir, dirs_exist_ok=True)
        self.repo.git.checkout(self.branch)

    def _return_paths(self) -> None:
        """
        Brings back to the initial working directory.
        """
        os.chdir(self.work_dir)

    def delete_dir(self, directory: str) -> None:
        """
        Deletes the specified directory.
        """
        shutil.rmtree(directory)
