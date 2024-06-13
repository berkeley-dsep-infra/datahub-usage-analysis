# Jupyterhub Usage Analysis
Code for Berkeley's DataHub JupyterHub installation anaylsis.

Mostly focused around server/user usage, files opened and nbgitpuller links are clicked.

# Working in this repo

## SSH keys
If you've created `ssh` keys previously, please skip to the next step.

### ubuntu/WSL2
If you're running Ubuntu, regular installation/VM or WSL2, and have NOT previously generated SSH keys please execute the following commands:
```
ssh-keygen -t id_rsa -b 8192
```
For added security, you can choose to enter a passphrase during key creation.  This is optional.

### macos
If you're using macos, and have NOT previously generated SSH keys please execute the following commands:
```
ssh-keygen -t id_rsa -b 8192
```
For added security, you can choose to enter a passphrase during key creation.  This is optional.

### windows
If you're running Windows, please install either [WSL2 native linux](https://learn.microsoft.com/en-us/windows/wsl/install) or [gitbash](https://www.git-scm.com/download/win).

open a terminal, and run the following command.  WSL2 is preferred, but there are a couple of additional steps required.

**TODO**
get jose up and running w/ubunto WSL, update docs

```
ssh-keygen -t id_rsa -b 8192
```
For added security, you can choose to enter a passphrase during key creation.  This is optional.

## Setting up your fork and clones

When you log in to your terminal, you will be in your home directory.  We
recomend creating a sub-directory named something like `src` or `repos`.  This
will help you manage any other repos you might download.

```
$ pwd
/home/sknapp
$ mkdir src
$ cd src
```

Next, go to the [Datahub Usage Analysis github repo](https://github.com/berkeley-dsep-infra/datahub-usage-analysis/)
and create a fork.  To do this, click on the `fork` button and then `Create fork`.

Now clone the primary Datahub Usage Analysis repo on your local device.  You
can get the URL to do this by clicking on the green `Code` button in the 
primary Datahub repo (*not* your fork) and clicking on `ssh`:
```
$ pwd
/home/sknapp/src
$ git clone git@github.com:berkeley-dsep-infra/datahub-usage-analyis.git
```


Now `cd` in to `datahub` and set up your local repo to point both at the primary
Datahub repo (`upstream`) and your fork (`origin`).  After the initial clone,
`origin` will be pointing to the main repo and we'll need to change that.
```
$ cd datahub
$ git remote -v
origin	git@github.com:berkeley-dsep-infra/datahub.git (fetch)
origin	git@github.com:berkeley-dsep-infra/datahub.git (push)
$ git remote rename origin upstream
$ git remote add origin git@github.com:<your github username>/datahub.git
$ git remote -v
origin	git@github.com:<your github username>/datahub.git (fetch)
origin	git@github.com:<your github username>/datahub.git (push)
upstream	git@github.com:berkeley-dsep-infra/datahub.git (fetch)
upstream	git@github.com:berkeley-dsep-infra/datahub.git (push)
```

Now you can sync your local repo from `upstream`, and push those changes to your
fork (`origin`):
```
git checkout staging && \
git fetch --prune --all && \
git rebase upstream/staging && \
git push origin staging
```


## Procedure

When developing for this deployment, always work in a fork of this repo.
You should also make sure that your repo is up-to-date with this one prior
to making changes. This is because other contributors may have pushed changes
after you last synced with this repo but before you upstreamed your changes.

```
git checkout staging && \
git fetch --prune --all && \
git rebase upstream/staging && \
git push origin staging
```

To create a new branch and switch to it, run the following command:
```
git checkout -b <branch name>
```

After you make your changes, you can use the following commands to see
what's been modified and check out the diffs:  `git status` and `git diff`.


When you're ready to push these changes, first you'll need to stage them for a
commit:
```
git add <file1> <file2> <etc>
```

Commit these changes locally:
```
git commit -m "some pithy commit description"
```

Now push to your fork:
```
git push origin <branch name>
```

Once you've pushed to your fork, you can go to the
[Datahub repo](https://github.com/berkeley-dsep-infra/datahub) and there
should be a big green button on the top that says `Compare and pull request`.
Click on that, check out the commits and file diffs, edit the title and
description if needed and then click `Create pull request`.
Data is stored in a shared GDrive folder.
