# Introduction to Body Pose Estimation and Gesture Recognition

This code is for the workshop "Introduction to Body Pose Estimation" by Alex Dillhoff at HackUTA 2023.

[Presentation Slides](https://docs.google.com/presentation/d/1yuIdRLyvbE97CH4Yq4NYgfeTLR9aiAfQ5C-4rDtXN6c/edit?usp=sharing)

## Setup

```bash
# Create a conda environment from the requirements file
conda env create -f requirements.yml
```

### Connecting to Spotify

To integrate the Spotify API using `spotipy`, you will need to create an application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and use the generated client ID and client secret to export them as environment variables. These will be read by `spotipy` to authenticate your application.

## Dependencies

- [MediaPipe](https://google.github.io/mediapipe/)
- [OpenCV](https://opencv.org/)
- [spotipy](https://spotipy.readthedocs.io/en/2.22.1/)

## References

- [MediaPipe](https://google.github.io/mediapipe/)
- [OpenCV](https://opencv.org/)
- [MobileNetV2](https://arxiv.org/abs/1801.04381)
- [BlazePose](https://arxiv.org/abs/2006.10204)
- [GHUM](https://openaccess.thecvf.com/content_CVPR_2020/papers/Xu_GHUM__GHUML_Generative_3D_Human_Shape_and_Articulated_Pose_CVPR_2020_paper.pdf)
- [MediaPipe Hands](https://arxiv.org/abs/2006.10214)