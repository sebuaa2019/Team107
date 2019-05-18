#!/bin/bash
ps -ef | grep python3 | cut -c 9-15| xargs kill -s 9
ps -ef | grep homebridge | cut -c 9-15| xargs kill -s 9