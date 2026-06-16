"""
下载广西甘蔗主产区离线地图瓦片
使用 CartoDB dark_all 暗色底图，覆盖广西主要甘蔗种植区域

用法: python download_tiles.py
"""
import os
import time
import urllib.request

# 广西甘蔗主产区范围 (经纬度)
# 北: 25.5°N (柳州北部), 南: 21.5°N (崇左南部)
# 西: 105.5°E (百色西部), 东: 111.0°E (贺州东部)
BOUNDS = {
    'north': 25.5,
    'south': 21.5,
    'west': 105.5,
    'east': 111.0,
}

# 下载的缩放级别 (7-15 足够覆盖乡镇级别)
# 级别越高瓦片越多，7-15约需下载 ~50000 张瓦片 (~500MB)
ZOOM_LEVELS = range(7, 16)

# CartoDB dark_all 瓦片URL
TILE_URL = 'https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'public', 'tiles')


def lng2tile(lng, zoom):
    return int((lng + 180) / 360 * 2 ** zoom)


def lat2tile(lat, zoom):
    import math
    return int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 2 ** zoom)


def download_tiles():
    total = 0
    downloaded = 0
    skipped = 0
    failed = 0

    for zoom in ZOOM_LEVELS:
        x_min = lng2tile(BOUNDS['west'], zoom)
        x_max = lng2tile(BOUNDS['east'], zoom)
        y_min = lat2tile(BOUNDS['north'], zoom)
        y_max = lat2tile(BOUNDS['south'], zoom)

        level_total = (x_max - x_min + 1) * (y_max - y_min + 1)
        total += level_total
        print(f'\n级别 {zoom}: x=[{x_min},{x_max}] y=[{y_min},{y_max}] 共 {level_total} 张瓦片')

        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                tile_dir = os.path.join(OUTPUT_DIR, str(zoom), str(x))
                tile_path = os.path.join(tile_dir, f'{y}.png')

                # 跳过已下载的瓦片
                if os.path.exists(tile_path):
                    skipped += 1
                    continue

                os.makedirs(tile_dir, exist_ok=True)

                url = TILE_URL.format(z=zoom, x=x, y=y)
                try:
                    urllib.request.urlretrieve(url, tile_path)
                    downloaded += 1
                except Exception as e:
                    failed += 1
                    if failed <= 10:
                        print(f'  下载失败: {url} - {e}')

                # 限速，避免被服务器拒绝
                time.sleep(0.05)

        print(f'  级别 {zoom} 完成: 已下载={downloaded}, 跳过={skipped}, 失败={failed}')

    print(f'\n下载完成!')
    print(f'  总计: {total} 张瓦片')
    print(f'  已下载: {downloaded}')
    print(f'  已存在跳过: {skipped}')
    print(f'  失败: {failed}')
    print(f'  瓦片目录: {OUTPUT_DIR}')


if __name__ == '__main__':
    print('桂收 · 甘蔗专用版 - 离线地图瓦片下载工具')
    print(f'覆盖范围: 广西甘蔗主产区 ({BOUNDS["south"]}°N - {BOUNDS["north"]}°N, {BOUNDS["west"]}°E - {BOUNDS["east"]}°E)')
    print(f'缩放级别: {ZOOM_LEVELS.start} - {ZOOM_LEVELS.stop - 1}')
    print(f'输出目录: {OUTPUT_DIR}')
    print()

    confirm = input('确认下载? (预计 500MB 磁盘空间，需要联网) [y/N]: ')
    if confirm.lower() != 'y':
        print('已取消')
        exit(0)

    download_tiles()
