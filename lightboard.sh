#!/usr/bin/env bash

BASE="./lights.sh"

while read -n1 ans; do
	case $ans in
		g)
			${BASE} glitter
			;;
		G)
			${BASE} glitter_rave
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
		R)
			${BASE} rave_fast
			;;
		*)
			;;
	esac
done
