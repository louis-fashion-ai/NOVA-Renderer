

import sys
# sys.path.append('/HOME/HOME/HOME/data/panic3d/gameday-3d-human-reconstruction-panic3d_renderer-')
# sys.path.append('/HOME/HOME/HOME/data/panic3d/')
from _util.util_v1 import * ; import _util.util_v1 as uutil
import time


DEBUG = False

bns = uutil.read_bns('./_data/lustrous/subsets/human_rutileEB_all.csv') \
    if not DEBUG else ['6152365338188306398',]
for bn in bns:
    querystr = ','.join([
        'human_rutileE',
        bn[-1],
        bn,
        f'./_data/lustrous/raw/vroid/{bn[-1]}/{bn}/{bn}.vrm',
    ])
    for dtype in [
        # 'ortho',
        # 'ortho_xyza',                                                              
        # 'rgb',
        # 'xyza',
        'rgb60',
        'xyza60',
    ]:
        print(f'{bn}: {dtype}')
        os.system(' '.join([
            'DEBUG=' if DEBUG else '',
            f'xvfb-run python3 -m _scripts.render_human_{dtype}',
            # f'xvfb-run python3 -m _scripts.render_{dtype}',
            querystr,
        ]))
        # time.sleep(1)
        # break
    # break







