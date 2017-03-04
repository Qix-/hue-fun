#!/usr/bin/env bash

BASE="python main.py --layout="4,8,6,5,7" --resolution=0.1 192.168.1.122"

while read -n1 ans; do
	case $ans in
		g)
			${BASE} glitter
			;;
		p)
			${BASE} punch
			;;
		"[")
			${BASE} punch_long
			;;
		f)
			${BASE} fullbright_now
			;;
		"\`")
			${BASE} off_now
			;;
		r)
			${BASE} rave
			;;
		*)
			;;
	esac
done
