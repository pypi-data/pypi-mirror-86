import os
import tempfile
import subprocess
import shutil

from .recipe import Recipe
from .subprocess import call, check_call


class RecipeInWorktree:
    def __init__(self, recipe):
        self.recipe = recipe
        self.tmpdir = None

    async def __aenter__(self):
        self.tmpdir = tempfile.mkdtemp(prefix="ccb-")
        try:
            await check_call(
                ["git", "worktree", "add", "-q", "--checkout", "--detach", self.tmpdir],
                cwd=self.recipe.path,
            )
            return Recipe(self.tmpdir, self.recipe.name)
        except BaseException:
            self.cleanup()
            raise

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        await self.cleanup()

    async def cleanup(self):
        if self.tmpdir is None:
            return

        await call(
            ["git", "worktree", "remove", "-f", self.tmpdir], cwd=self.recipe.path
        )
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        self.tmpdir = None


async def branch_exists(recipe, branch_name):
    return (
        await call(
            ["git", "show-ref", "--verify", "-q", f"refs/heads/{branch_name}"],
            cwd=recipe.path,
        )
        == 0
    )


async def remote_branch_exists(recipe, branch_name, remote):
    return (
        await call(
            [
                "git",
                "show-ref",
                "--verify",
                "-q",
                f"refs/remotes/{remote}/{branch_name}",
            ],
            cwd=recipe.path,
        )
        == 0
    )


async def create_branch_and_commit(recipe, branch_name, commit_msg):
    await check_call(["git", "checkout", "-q", "-b", branch_name], cwd=recipe.path)
    await check_call(
        [
            "git",
            "commit",
            "-q",
            "-a",
            "-m",
            commit_msg,
        ],
        cwd=recipe.path,
    )


async def remove_branch(recipe, branch_name):
    await check_call(["git", "branch", "-q", "-D", branch_name], cwd=recipe.path)


async def push_branch(recipe, remote, branch_name, force):
    await check_call(
        ["git", "push", "-q", "--set-upstream"]
        + (["-f"] if force else [])
        + [remote, branch_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=recipe.path,
    )