


# vroid_renderer

This repo converts and renders the 3D datasets introduced in [PAniC-3D: Stylized Single-view 3D Reconstruction from Portraits of Anime Characters](https://github.com/ShuhongChen/panic3d-anime-reconstruction).  As described in that repo, these scripts will add to `./_data/lustrous`

## environment setup
```
apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
software-properties-common curl vim git zip unzip unrar p7zip-full wget cmake \
apache2 openssl libssl-dev

apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
libwebp-dev libcairo2-dev libjpeg-dev libgif-dev \
libboost-all-dev libopencv-dev libwxgtk3.0-gtk3-dev \
ffmpeg libgl1-mesa-glx libsm6 libxext6 libxrender-dev libx11-xcb1 \
mesa-utils xauth xorg openbox 0
pip install pyrr
pip install \
    'moderngl==5.6.4' \
    'moderngl-window==2.4.1' \
    'PyQt5==5.15.6' \
    'PyQt5-Qt5==5.15.2' \
    'PyQt5-sip==12.10.1' \
    'PySDL2==0.9.11' \
    'PySide2==5.15.2.1' \
    'cffi==1.15.0' \
    'glfw==1.12.0' \
    'pymunk==6.2.1' \
    'pywavefront==1.3.3' \
    'shiboken2==5.15.2.1'
pip install \
    'pyunpack==0.2.2'

pip install \
    'pygltflib==1.14.5'

pip install \
    'opencv-contrib-python==4.5.4.60'

pip install \
    'kornia==0.6.2'
pip install \
    'trimesh==3.12.3'
pip install \
    'torch-fidelity==0.3.0'
export DISPLAY=:0.0
```

## setup

Make a copy of `./_env/machine_config.bashrc.template` to `./_env/machine_config.bashrc`, and set `$PROJECT_DN` to the absolute path of this repository folder.  The other variables are optional.

This project requires docker with a GPU.  Run these lines from the project directory to pull the image and enter a container; note these are bash scripts inside the `./make` folder, not `make` commands.  Alternatively, you can build the docker image yourself.

    make/docker_pull
    make/shell_docker
    # OR
    make/docker_build
    make/shell_docker


## vroid-dataset

The [vroid-dataset](https://github.com/ShuhongChen/vroid-dataset) should have downloaded folders of `.vrm` with their metadata to `./_data/lustrous/raw/vroid/[0-9]/*`.  This script renders those to `./_data/lustrous/renders/rutileE/`

    # run render script
    export DISPLAY=:0.0
    ps -aux | grep Xorg
    startx
    nohup python -m _scripts.render_all_vroid_rutileE > nova_head.out &



## vroid-human dataset

    # run render script
test:
    xvfb-run python3 -m _scripts.render_human_ortho human_rutileE,7,1001275948686780577,./_data/lustrous/raw/vroid/7/1001275948686780577/1001275948686780577.vrm
    xvfb-run python3 -m _scripts.render_human_rgb60 human_rutileE,7,1001275948686780577,../_data/lustrous/raw/vroid/7/1001275948686780577/1001275948686780577.vrm
    nohup python -m _scripts.render_all_vroid_human > nova_human.out &
    python -m _scripts.generate_meta_json --path /hy-tmp/panic3d_renderer/_data/lustrous/raw/vroid --category human_rutileE


## animerecon-benchmark

The [animerecon-benchmark](https://github.com/ShuhongChen/animerecon-benchmark) should have downloaded compressed files to `./_data/lustrous/raw/[genshin,hololive]`.  Decompress all these files to a temp directory; each file becomes a directory carrying a `.pmx` MMD model.  Using a [DSSc converter](https://drive.google.com/drive/folders/1Zpt9x_OlGALi-o-TdvBPzUPcvTc7zpuV?usp=share_link), go to `PMX-to-VRM > Batch`, and select `./_data/lustrous/raw/dssc/dssc_mapping_daredemoE.txt`.  This should convert and put files to `./_data/lustrous/raw/dssc/[genshin,hololive]/*.vrm`.  The following script renders the `.vrm` files to `./_data/lustrous/renders/daredemoE/`

    # run render script
    python3 -m _scripts.render_all_animerecon_daredemoE

(Thanks to [Softmind Ltd.](https://www.softmind.tech/) for sharing their [DanSingSing converter](https://vtuber.itch.io/dssconverter), and Geng Lin for adding the batch function)


## citing

If you use our repo, please cite our work:

    @inproceedings{chen2023panic3d,
        title={PAniC-3D: Stylized Single-view 3D Reconstruction from Portraits of Anime Characters},
        author={Chen, Shuhong and Zhang, Kevin and Shi, Yichun and Wang, Heng and Zhu, Yiheng and Song, Guoxian and An, Sizhe and Kristjansson, Janus and Yang, Xiao and Matthias Zwicker},
        booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
        year={2023}
    }


