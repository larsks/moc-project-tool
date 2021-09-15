import ansible_runner
import logging
import schedule
import time

from decouple import config
from pathlib import Path

LOG = logging.getLogger(__name__)

RUNNER_DATA_DIR = config("RUNNER_DATA_DIR", default=".")
RUNNER_PLAYBOOK = config("RUNNER_PLAYBOOK", default="playbook.yml")
RUNNER_ARTIFACT_DIR = config("RUNNER_ARTIFACT_DIR", default="artifacts")
RUNNER_KEEP_ARTIFACTS = config("RUNNER_KEEP_ARTIFACTS", cast=int, default=10)
RUNNER_INTERVAL = config("RUNNER_INTERVAL", cast=int, default=300)
RUNNER_SKIPFILE = config("RUNNER_SKIPFILE", default=None)
RUNNER_LOGLEVEL = config("RUNNER_LOGLEVEL", cast=int, default=0)

if RUNNER_SKIPFILE:
    LOG.info("using skipfile %s", RUNNER_SKIPFILE)
    skip_file = Path(RUNNER_SKIPFILE)
else:
    skip_file = None


def run_playbook():
    if skip_file is not None and skip_file.exists():
        LOG.warning("skip file exists, skipping this run")
        return

    LOG.info("run playbook %s", RUNNER_PLAYBOOK)
    res = ansible_runner.run(
        private_data_dir=RUNNER_DATA_DIR,
        playbook=RUNNER_PLAYBOOK,
        artifact_dir=RUNNER_ARTIFACT_DIR,
        rotate_artifacts=RUNNER_KEEP_ARTIFACTS,
    )
    LOG.info("finished playbook %s, exit code = %d", RUNNER_PLAYBOOK, res.rc)


def main():
    loglevel = ["WARNING", "INFO", "DEBUG"][min(RUNNER_LOGLEVEL, 2)]
    logging.basicConfig(
        level=loglevel,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)s %(message)s",
    )

    schedule.every(RUNNER_INTERVAL).seconds.do(run_playbook)

    LOG.info("starting scheduler (interval=%d seconds)", RUNNER_INTERVAL)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
