"""
This module contains the GitClone class, 
which is used to create the before and after directories of a PR.
"""
import os
import subprocess
import shutil
from git import Repo


class GitClone:
    """
    Class that creates the before and after directories of a PR.
    """

    def __init__(self, repo_url: str, pr_number: int, branch: str = "master") -> None:
        """
        repo_url: The URL of the repository.
        pr_number: The number of the PR.
        branch: the branch you want to merge into. Default is master.
        """
        self.repo_url = repo_url
        self.pr_number = pr_number
        self.branch = branch
        self.work_dir = os.getcwd()
        self.repo_dir = os.path.join(self.work_dir, "repo-git")
        self.before_dir = ""
        self.after_dir = ""

    def run(self) -> None:
        """
        Runs the process of cloning the repo and checking out the PR.
        """
        self._create_dirs()
        self._clone_repo()
        self._before_dir()
        self._after_dir()
        self._return_paths()

    def _create_dirs(self) -> None:
        """
        Creates the before and after directories,
        using mktemp to create a temporary directory.
        """
        os.makedirs(self.work_dir, exist_ok=True)
        self.before_dir = subprocess.run(
            ["mktemp", "-d", "before.XXXX", "-p", self.work_dir],
            capture_output=True, check=True).stdout.decode().strip()
        self.after_dir = subprocess.run(
            ["mktemp", "-d", "after.XXXX", "-p", self.work_dir],
            capture_output=True, check=True).stdout.decode().strip()

    def _clone_repo(self) -> None:
        """
        Clones the repository into the repo directory,
        using the gitpython library.
        """
        os.makedirs(self.repo_dir, exist_ok=True)
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
        self.repo.git.fetch(
            "origin", f"pull/{self.pr_number}/head:pr-{self.pr_number}")
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
