Changelog for fishnet
=====================

v1.82.2
-------

* Nag about update to fishnet 2.x.

v1.18.1
-------

* Lichess-hosted instances: Make `UCI_Elo` gradient steeper. Reintroduce depth
  limits to limit resource consumption of low levels.

v1.18.0
-------

* New command: Use `python -m fishnet systemd-user` to generate a systemd user
  service file.
* New command: Use `python -m fishnet benchmark` to try running the engine
  before getting a fishnet key.
* Fix process shutdown order with systemd.
* Fix race condition during shutdown on Python 2.7.
* Lichess-hosted instances: Use `UCI_Elo` instead of `Skill Level` and expand
  the range significantly. Low skill levels should now play much weaker.

v1.17.2
-------

* Reduce maximum move time from 20s to 6s. Clients that frequently hit this
  limit should be stopped in favor of clients with better hardware.
* Support future proof constants `--user-backlog short` and
  `--system-backlog long` (to be used instead of hardcoded durations).
* Fix some ignored command line flags during `python -m fishnet configure`
  and on intial run.

v1.17.1
-------

* Bring back `--threads-per-process`. Most contributors should not use this.

v1.17.0
-------

* Option to join only if a backlog is building up. Added `--user-backlog`
  and `--system-backlog` to configure threshold for oldest item in queue.
  Run `python -m fishnet configure` to rerun the setup dialog.
* Slow clients no longer work on young user requested analysis jobs. The
  threshold is continuously adjusted based on performance on other jobs.

v1.16.1
-------

* Fix false positive slowness warning.

v1.16.0
-------

* Removed `--threads-per-process`.
* Warning if client is unsustainably slow.
