#!/bin/sh

# Fix ownership for the media directory
chown -R appuser:appuser /app/adv_ui_ocrroo_project/adv_ui_ocrroo_app/media

# Execute the main container command as appuser
exec gosu appuser "$@"