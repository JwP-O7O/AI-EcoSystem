# PWA Icons

Place your app icons here:

- `icon-192.png` - 192x192px icon
- `icon-512.png` - 512x512px icon
- `icon-maskable-512.png` - 512x512px maskable icon (optional)

## Generate Icons

You can generate icons from a logo using:

1. **Online tool**: https://www.pwabuilder.com/imageGenerator
2. **CLI**: `npx pwa-asset-generator logo.svg ./public/icons`

## Placeholder Icons

For now, you can use simple colored squares as placeholders.
The app will work without custom icons (browser will use defaults).

## Requirements

- PNG format
- Transparent background or solid color
- Square aspect ratio (1:1)
- Optimized for mobile (< 50KB per icon)
