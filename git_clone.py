"""
This module contains the GitClone class, 
which is used to create the before and after directories of a PR.
"""
import os
import subprocess
import shutil


class GitClone:
    """
    Class that creates the before and after directories of a PR.
    """

    def __init__(self, repo_url: str, pr_number: int, branch: str = "master"):
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

    def run(self):
        """
        Runs the process of cloning the repo and checking out the PR.
        """
        self._create_dirs()
        self._clone_repo()
        self._before_dir()
        self._after_dir()
        self._return_paths()

    def _create_dirs(self):
        """
        Creates the before and after directories.
        """
        os.makedirs(self.work_dir, exist_ok=True)
        self.before_dir = subprocess.run(
            ["mktemp", "-d", "before.XXXX", "-p", self.work_dir],
            capture_output=True, check=True).stdout.decode().strip()
        self.after_dir = subprocess.run(
            ["mktemp", "-d", "after.XXXX", "-p", self.work_dir],
            capture_output=True, check=True).stdout.decode().strip()

    def _clone_repo(self):
        """
        Clones the repo and saves the before directory.
        """
        os.makedirs(self.repo_dir, exist_ok=True)
        subprocess.run(["git", "clone", self.repo_url, self.repo_dir],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    def _before_dir(self):
        """
        Creates the before directory snapshot using git archive.
        """
        os.chdir(self.repo_dir)
        subprocess.run(["git", "fetch", "origin", self.branch],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["git", "checkout", self.branch],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # Create the before snapshot using git archive
        subprocess.run(f"git archive {self.branch} | tar -x -C {self.before_dir}",
                       shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    def _after_dir(self):
        """
        Creates the after directory snapshot using git archive.
        """
        os.chdir(self.repo_dir)
        subprocess.run(["git", "fetch", "origin",
                       f"pull/{self.pr_number}/head:pr-{self.pr_number}"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["git", "checkout", f"pr-{self.pr_number}"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # Create the after snapshot using git archive
        subprocess.run(f"git archive pr-{self.pr_number} | tar -x -C {self.after_dir}",
                       shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    def _return_paths(self):
        """
        Brings back to the initial working directory.
        """
        os.chdir(self.work_dir)

    def delete_dir(self):
        """
        Deletes the before and after directories.
        """
        shutil.rmtree(self.before_dir)
        shutil.rmtree(self.after_dir)
        shutil.rmtree(self.repo_dir)
