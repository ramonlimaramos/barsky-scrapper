#!/usr/bin/env bash
set -e

case $1 in
local-web)
  echo "Local Web with watchmedo"
  alembic upgrade head
  watchmedo auto-restart -d barsky_scrapper -p '*.py' --recursive -- gunicorn -w 2 -b 0.0.0.0:5000 barsky_scrapper.main:app --log-level=debug --reload
  ;;
local-worker)
  echo "Local worker with watchmedo"
  celery worker -A barsky_scrapper.services.background.main --loglevel=DEBUG --autoscale=${CELERY_CONCURRENCY_MAX:-4},${CELERY_CONCURRENCY_MIN:-4}
  ;;
*)
  echo "Fail!"
  ;;
esac
