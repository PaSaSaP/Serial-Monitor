#!/bin/sh

if [[ ! $VSCA_BUILD_MODE = Uploading ]]; then
    exit 0
fi

ps aux|grep -w $(basename "$VSCA_SERIAL"|cut -d. -f2)|grep -w SerialMonitor|grep -v -w grep|awk '{print $2}'|xargs kill -SIGFPE

