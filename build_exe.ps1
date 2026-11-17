# build_exe.ps1 - build portable single-file EXE from KeepActive.py
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Building KeepActive Portable Executable" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check / Install dependencies (if needed)
Write-Host "`n[1/3] Ensuring required packages are available..." -ForegroundColor Cyan
python -c "import pystray, PIL, PyInstaller; print('All dependencies found.')"

# 2. Generate app.ico for the EXE file icon
Write-Host "`n[2/3] Generating app icon..." -ForegroundColor Cyan
python -c @"
from PIL import Image, ImageDraw

sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
images = []
for s in sizes:
    img = Image.new('RGBA', s, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = max(1, s[0] // 8)
    draw.ellipse([pad, pad, s[0] - pad, s[1] - pad], fill=(50, 200, 80, 255))
    images.append(img)

images[0].save('app.ico', format='ICO', sizes=[(img.width, img.height) for img in images], append_images=images[1:])
print('Generated app.ico successfully.')
"@

# 3. Build single-file EXE using PyInstaller
Write-Host "`n[3/3] Building single-file EXE with PyInstaller..." -ForegroundColor Cyan
python -m PyInstaller `
    --clean `
    --onefile `
    --noconsole `
    --name "KeepActive" `
    --icon "app.ico" `
    --distpath "dist" `
    --workpath "build" `
    --specpath "." `
    KeepActive.py

Write-Host "`n==========================================" -ForegroundColor Green
Write-Host " Build Complete!" -ForegroundColor Green
Write-Host " Portable EXE -> $(Resolve-Path dist\KeepActive.exe)" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

