## Needs

Python 3.9 or later. The script uses the standard library only. The repository is private, so installing the plugin needs access to `m4bwav/steerwright`.

## Install

Add the repository as a plugin source in Claude Code and install `steerwright`. The skill loads on requests such as "how are my projects doing" or "review my projects". The script lives at `skills/steerwright/scripts/sw.py`.

## First run

Discovery only proposes entries until you pass `--apply`:

```sh
python skills/steerwright/scripts/sw.py discover
python skills/steerwright/scripts/sw.py discover --apply
```

It looks at askwright projects, chain ledgers, grind states and `ai-docs/HANDOFF.md` files with activity in the last 30 days (`--since` changes that). Related projects are grouped unless you pass `--no-group`.

Add a project by hand:

```sh
python skills/steerwright/scripts/sw.py add "My game" --path D:/code/mygame --kind game --goal "Ship a demo" --done-when "Demo on itch.io" --target 2026-12-01
```

## Open the pages

```sh
python skills/steerwright/scripts/sw.py up
```

This starts the steerwright server, the askwright dashboard and the chainwright and grindwright indexes, then opens the main page in a browser. `sw.py down` stops only the processes `up` started. `sw.py shortcut` writes a desktop `.cmd` that runs `up`.

## Where things are kept

The registry is `~/.steerwright/projects.json`. Set `STEERWRIGHT_HOME` to keep it somewhere else. Weekly review sets are written under `~/.steerwright/reviews`.
