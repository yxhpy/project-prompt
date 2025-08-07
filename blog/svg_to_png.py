import os
os.environ['PATH'] = os.path.join(os.path.dirname(__file__), 'vips/bin') + ';' + os.environ['PATH']
# 查询所有IMAGE_CHART_x.svg
svg_files = os.listdir()
import pyvips
for  i in svg_files:
    if i.endswith('.svg') and i.startswith('IMAGE_CHART_'):
        image = pyvips.Image.new_from_file(i, dpi=300)  # 高DPI
        image.write_to_file(i.replace('.svg', '.png'))
