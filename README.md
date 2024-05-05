# pico_lcd_gallery

## Converting images to bmp

Images downloaded from the web are sometimes in `.webp` format - to convert to `.png`:

```bash
% dwebp downloaded.webp -o input.png
```

To scale the image, convert to `.bmp`, turn off compression and transparency:

```bash
% convert -define bmp:format=bmp3 -compress none -alpha off -resize 160x128 input.png output.bmp
```

The resulting `.bmp` image can then be uploaded to the bucket and referenced by the `list.json` file.
