# pico_lcd_gallery

## Converting images to bmp

```bash
% dwebp Meet_the_Ponies_main_crop.webp -o meet.png
% convert -define bmp:format=bmp3 -compress none -alpha off -resize 160x128 meet.png mlpmeet.bmp
% convert -define bmp:format=bmp3 -compress none -alpha off -resize 160x128 4962723b02c5b89d3907cc7e5c21cb37368523bf.jpg mlp6.bmp
```
