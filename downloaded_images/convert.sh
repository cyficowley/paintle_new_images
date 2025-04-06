for i in *.jpg; do
    ffmpeg -i "$i" -c:v libwebp -q:v 80 "${i%.jpg}.webp"
done
