if [ $1 = "fetch" ]; then
	edge-tts --text "$(xsel)" --rate=+80% 2>/dev/null | mpv --input-ipc-server=/tmp/mpvsocket -
elif [ $1 = "pause" ]; then
	echo '{ "command": ["cycle", "pause"] }' | socat - /tmp/mpvsocket
fi

