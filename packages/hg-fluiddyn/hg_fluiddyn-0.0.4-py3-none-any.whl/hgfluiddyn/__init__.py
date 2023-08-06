"""
## Example of configuration for this extension (in ~/.hgrc)

```
[fluiddyn]
root = ~/Dev
maintainer = 1
```

## Writing Mercurial extentions

- https://www.mercurial-scm.org/wiki/WritingExtensions
- https://www.mercurial-scm.org/wiki/MercurialApi

"""

import os
import subprocess

from mercurial import registrar
from mercurial import hg
from mercurial import commands
from mercurial import extensions
from mercurial import error

github_base = "git+ssh://git@github.com/fluiddyn/"
heptapod_base = "ssh://hg@foss.heptapod.net/fluiddyn"

cmdtable = {}
command = registrar.command(cmdtable)

testedwith = "4.9.1 5.1 5.2"
buglink = "https://foss.heptapod.net/fluiddyn/hg-fluiddyn/issues"

all_fluiddyn_packages = [
    "fluiddyn",
    "transonic",
    "fluidfft",
    "fluidsim",
    "fluidlab",
    "fluidimage",
    "fluidsht",
    "fluiddevops",
    "hg-fluiddyn",
    "conda-app",
]


def s2b(string):
    return bytes(string, "utf-8")


def uisetup(ui):
    global maintainer
    maintainer = ui.configbool(
        b"fluiddyn", b"maintainer", default=False, untrusted=False
    )

    global fluiddyn_packages
    fluiddyn_packages = [
        "fluiddyn",
        "transonic",
        "fluidfft",
        "fluidsim",
        "fluidlab",
        "fluidimage",
        "fluidsht",
    ]

    if maintainer:
        fluiddyn_packages = all_fluiddyn_packages

    tweakdefaults = ui.configbool(b"ui", b"tweakdefaults", untrusted=False)
    if not tweakdefaults:
        ui.warn(
            b"You should activate tweakdefaults in your ~/.hgrc:\n\n"
            b"[ui]\ntweakdefaults = True\n\n"
        )

    global root
    root = os.path.expanduser(
        ui.config(b"fluiddyn", b"root", default="~/Dev", untrusted=False)
    )


@command(b"fluiddyn-clone-repositories", [], norepo=True)
def fluiddyn_clone_repositories(ui, **opts):
    ui.write(b"Hello FluidDyn developer!\n")
    for package_name in fluiddyn_packages:
        check_clone(ui, package_name)


def check_clone(ui, package_name):
    ui.write(s2b(package_name + "\n"))
    path_repo = os.path.join(root, package_name)
    try:
        hg.repository(ui, s2b(path_repo))
    except error.RepoError:
        ui.write(s2b("the repository {} needs to be cloned\n".format(package_name)))
        address = heptapod_base + "/" + package_name
        commands.clone(ui, s2b(str(address)), dest=s2b(path_repo))
    else:
        ui.write(s2b("the repository {} is already cloned\n".format(package_name)))


@command(b"fluiddyn-pull-update-default", [], norepo=True)
def fluiddyn_pull_update_default(ui, **opts):
    ui.write(b"Hello FluidDyn developer!\n")
    for package_name in fluiddyn_packages:
        pull_update_default(ui, package_name)


def pull_update_default(ui, package_name):
    ui.write(s2b(package_name + "\n"))
    path_repo = os.path.join(root, package_name)
    try:
        repo = hg.repository(ui, s2b(path_repo))
    except error.RepoError:
        ui.write(b"the repository needs to be cloned\n")
        address = heptapod_base + "/" + package_name
        commands.clone(ui, str(address), dest=path_repo)
    else:
        ui.write(b"the repository exists: pull and update to default\n")
        commands.pull(repo.ui, repo)
        commands.update(ui, repo, b"default")


@command(b"fluiddyn-set-paths", [], norepo=True)
def fluiddyn_set_paths(ui, **opts):
    ui.write(b"Hello FluidDyn developer!\n")
    for package_name in fluiddyn_packages:
        set_path(ui, package_name)


def set_path(ui, package_name):

    path_repo = os.path.join(root, package_name)
    try:
        repo = hg.repository(ui, s2b(path_repo))
    except error.RepoError:
        return
    paths = dict(repo.ui.configitems(b"paths", untrusted=False))
    path_default = paths[b"default"]

    has_to_fix = False

    if b"bitbucket.org" in path_default:
        ui.warn(
            s2b(
                "default for {} is still pointing towards Bitbucket.org\n".format(
                    package_name
                )
            )
        )
        has_to_fix = True

    if maintainer and "bitbucket" not in paths:
        has_to_fix = True

    if not has_to_fix:
        ui.write(s2b("paths {} ok\n".format(package_name)))
        return

    nb_paths = len(paths)

    path_hgrc = os.path.join(path_repo, ".hg/hgrc")

    with open(path_hgrc, "r") as file:
        lines = file.readlines()

    index_path = -1
    in_paths = False
    for index, line in enumerate(lines):
        if line.strip() == "[paths]":
            index_paths = index
            in_paths = True

        if in_paths and any(line.startswith(key.decode()) for key in paths.keys()):
            index_path += 1
            if index_path == nb_paths - 1:
                index_end_paths = index
                break

    lines_new = lines[: index_paths + 1]
    lines_new.append(
        "default = ssh://hg@foss.heptapod.net/fluiddyn/{}\n".format(package_name)
    )

    lines_new += lines[index_end_paths + 1 :]
    text = "".join(lines_new)
    ui.write(s2b("Modify {}\n".format(path_hgrc)))

    with open(path_hgrc, "w") as file:
        file.write(text)


def check_default_path(repo):
    default = dict(repo.ui.configitems(b"paths", untrusted=False))[b"default"]
    if b"foss.heptapod.net" not in default:
        repo.ui.write(b"default points to a wrong path")
        return
    return 1


def get_package_name(repo):
    default = dict(repo.ui.configitems(b"paths", untrusted=False))[b"default"]
    return os.path.split(default)[1]


# @command(b"fluiddyn-push-github", [])
# def fluiddyn_push_github(ui, repo, **opts):
#     if not check_default_path(repo):
#         return
#     commands.pull(ui, repo)
#     commands.bookmark(ui, repo, b"master", rev=b"head() and branch(default) and public()")
#     package_name = get_package_name(repo)
#     path_github = os.path.join(github_base, package_name)
#     # ui.write(path_github + "\n")
#     # commands.push(ui, repo, dest=path_github, bookmark="master")
#     subprocess.call(["hg", "push", path_github, "-B", "master"])
#     commands.bookmark(ui, repo, "master", delete=True)


def extsetup(ui):
    """To check the activated extensions"""

    extensions_to_check = [b"evolve", b"topic", b"rebase"]
    if maintainer:
        extensions_to_check.append(b"hggit")

    for ext in extensions_to_check:
        try:
            extensions.find(ext)
        except KeyError:
            ui.warn(b"extension %s not activated!\n" % ext)


def precommit_hook(ui, repo, **kwargs):
    try:
        subprocess.check_output(["black", "--version"])
    except OSError:
        ui.warn(b"please install black")
        return 1

    ui.pushbuffer()
    commands.status(ui, repo, no_status=True, added=True, modified=True)
    output = [path for path in ui.popbuffer().split("\n") if path.endswith(".py")]

    if not output:
        return

    return subprocess.call("black -l 82".split() + output)


def reposetup(ui, repo):
    try:
        package_name = get_package_name(repo)
    except KeyError:
        return

    if package_name not in all_fluiddyn_packages:
        return

    ui.setconfig("hooks", "precommit.hgfluiddyn", precommit_hook)
