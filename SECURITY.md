# Security policy

## Reporting a problem

Open an issue or a pull request. You can also report privately from the repository's **Security** tab with **Report a vulnerability**.

This is a one-person project with no bug bounty and no response deadline.

## Supported versions

Only the latest release on the default branch gets fixes.

## Scope

`sw.py` runs on your machine with your agent's permissions. It writes only under `~/.steerwright` (or `STEERWRIGHT_HOME`). It reads askwright, chainwright and grindwright state and project folders, and never writes them. `sw.py serve` binds 127.0.0.1 only, serves read-only pages and makes no outbound requests. `sw.py up` starts the sibling page servers and `down` stops only the processes it started, by PID.
