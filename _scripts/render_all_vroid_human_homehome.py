

import sys
sys.path.append('/HOME/HOME/data/panic3d/gameday-3d-human-reconstruction-panic3d_renderer-')
sys.path.append('/HOME/HOME/data/panic3d/')
from _util.util_v1 import * ; import _util.util_v1 as uutil
import time


DEBUG = False

bns = uutil.read_bns('/HOME/HOME/data/panic3d/_data/lustrous/subsets/human_rutileEB_three.csv') \
    if not DEBUG else ['6152365338188306398',]
for bn in bns:
    querystr = ','.join([
        'human_rutileE',
        bn[-1],
        bn,
        f'/HOME/HOME/data/panic3d/_data/lustrous/raw/vroid/{bn[-1]}/{bn}/{bn}.vrm',
    ])
    for dtype in [
        # 'ortho',
        # 'ortho_xyza',                                                              
        'rgb_homehome',
        # 'xyza',
    ]:
        print(f'{bn}: {dtype}')
        os.system(' '.join([
            'DEBUG=' if DEBUG else '',
            f'python3 /HOME/HOME/data/panic3d/gameday-3d-human-reconstruction-panic3d_renderer-/_scripts/render_human_{dtype}.py',
            # f'xvfb-run python3 -m _scripts.render_{dtype}',
            querystr,
        ]))
        # time.sleep(1)
        # break
    # break







