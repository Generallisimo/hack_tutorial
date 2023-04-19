#!/bin/bash

ifconfig
ifconfig enp0s3 down
ifconfig enp0s3 hw ether 00:11:00:11:00:12
ifconfig enp0s3 up
ifconfig
