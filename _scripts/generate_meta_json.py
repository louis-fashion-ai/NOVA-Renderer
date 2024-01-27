DEBUG = False

import os
import argparse
from _util.util_v1 import np_seed, jwrite
import numpy as np
from tqdm import tqdm


ap = argparse.ArgumentParser()
ap.add_argument('--path')
ap.add_argument('--category')
assert ap.parse_args().category in{"rutileE", "human_rutileE"} 
root_folder = ap.parse_args().path

def list_files_with_extension(root_folder, extension):
    vrm_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(extension):
                vrm_files.append(os.path.join(root, file))
    return vrm_files


bns = sorted(list_files_with_extension(root_folder, '.vrm'))
n_generations = 16 if not DEBUG else 16
if ap.parse_args().category == "rutileE":
    near_rgb = 0.5
    far_rgb = 1.5
    boxwarp_rgb = 0.7
    elevation_mu, elevation_sig = 0.0, 20
    azimuth_mu, azimuth_sig = 0.0, 100000  # basically uniform
    distance_mu, distance_sig = 1.0, 0.0
    fov_mu, fov_sig = 30.0, 0.0  # full-fov, only zero std supported atm

else:
    near_rgb = 2.5
    far_rgb = 4.5
    boxwarp_rgb = 2.1
    elevation_mu, elevation_sig = 0.0, 20
    azimuth_mu, azimuth_sig = 0.0, 100000  # basically uniform
    distance_mu, distance_sig = 3.5, 0.0
    fov_mu, fov_sig = 30.0, 0.0  # full-fov, only zero std supported atm

meta = {}
num_ng = 0
# bns = bns[:100]
good_bns = []

for bni, bn in enumerate(tqdm(bns)):
    querystr = [
        # 'rutileE',
        ap.parse_args().category,
        bn.split('/')[-1].split('.')[0][-1],
        bn.split('/')[-1].split('.')[0],
        bn,
    ]
    name,franch,bn,ifn = querystr
    # odn = f'./_data/lustrous/renders/{name}' if not DEBUG else f'./shm/_mgl_test/{name}'
    odn = f'/hy-tmp/panic3d_renderer/_data/lustrous/renders/{name}' if not DEBUG else f'./shm/_mgl_test/{name}'

    render_dtype = 'rgb'
    # print(f'{odn}/{render_dtype}/_logs/fails/{bn}.txt')
    if os.path.isfile(f'{odn}/{render_dtype}/_logs/fails/{bn}.txt'):
        print('no rendered images:', bn)
        num_ng += 1
        continue

    render_dtype = 'xyza'
    if os.path.isfile(f'{odn}/{render_dtype}/_logs/fails/{bn}.txt'):
        print('no rendered images:', bn)
        num_ng += 1
        continue

    elevations = []
    azimuths = []
    distances = []
    fovs = []
    for i in range(n_generations):
        with np_seed(f'{bn}/{bni}'):
            elevations.append(elevation_mu + elevation_sig*np.random.randn())
            azimuths.append(azimuth_mu + azimuth_sig*np.random.randn())
            distances.append(distance_mu + distance_sig*np.random.randn())
            fovs.append(fov_mu + fov_sig*np.random.randn())
    
    for i in range(n_generations):
        labeli = {
            "render_params": {
                "elev": elevations[i],
                "azim": azimuths[i],
                "dist": distances[i],
                "fov": 30.0,
                "near": near_rgb,
                "far": far_rgb,
                "boxwarp": boxwarp_rgb,
            }
        }

        render_dtype = 'rgb'
        meta.update({
            f'rutileE/{render_dtype}/{franch}/{bn}/{i:04d}': labeli
        })

        render_dtype = 'xyza'
        meta.update({
            f'rutileE/{render_dtype}/{franch}/{bn}/{i:04d}': labeli
        })

    elevations = [90., 0.,0.,0.,0.]
    azimuths = [0., -180.,-90.,0.,90.]
    # distances = [1.0,]*5
    fovs = [30.0,]*5
    render_idxs = ['top', 'back', 'right', 'front', 'left']
    if ap.parse_args().category == "rutileE":
        near_ortho = 0.5
        far_otho = 1.5
        boxwarp_otho = 0.7
        distances = [1.0,]*5
    else: 
        near_ortho = 1.0
        far_otho = 3.0
        boxwarp_otho = 2.1
        distances = [2.0,]*5
    for i, render_idx in enumerate(render_idxs):
        labeli = {
            "render_params": {
                "elev": elevations[i],
                "azim": azimuths[i],
                "dist": distances[i],
                "fov": 30.0,
                "near": near_ortho,
                "far": far_otho,
                "boxwarp": boxwarp_otho,
            }
        }

        render_dtype = 'ortho'
        meta.update({
            f'rutileE/{render_dtype}/{franch}/{bn}/{render_idx}': labeli
        })

    good_bns.append(bn)

# print(meta)
# jwrite(meta, '_data/lustrous/renders/rutileE/rutileE_meta.json')
jwrite(meta, f'/hy-tmp/panic3d_renderer/_data/lustrous/renders/{ap.parse_args().category}/{ap.parse_args().category}_meta.json')
print('num succ:', len(bns) - num_ng, 'num fail:', num_ng)


os.makedirs('/hy-tmp/panic3d_renderer/_data/lustrous/subsets/', exist_ok=True)
# with open('_data/lustrous/subsets/rutileEB_train.csv', 'w') as f:
with open(f'/hy-tmp/panic3d_renderer/_data/lustrous/subsets/{ap.parse_args().category}_train.csv', 'w') as f:
   for bn in good_bns:
       f.write("%s\n" % bn)