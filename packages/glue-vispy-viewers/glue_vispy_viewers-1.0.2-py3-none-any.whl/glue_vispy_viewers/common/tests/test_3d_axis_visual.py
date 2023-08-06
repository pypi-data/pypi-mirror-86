from vispy import scene
from ..axes import AxesVisual3D


def test_3d_axis_visual():

    canvas = scene.SceneCanvas(keys=None, size=(800, 600), show=True)
    view = canvas.central_widget.add_view()
    scene_transform = scene.STTransform()
    view.camera = scene.cameras.TurntableCamera(parent=view.scene,
                                                fov=0., distance=4.0)
    AxesVisual3D(view=view, axis_color='red', transform=scene_transform)

    canvas.native.show()
    canvas.native.close()
