from mlx import Mlx


class MlxWindow:
    """Thin wrapper that creates a MiniLibX window.

    It initializes the MiniLibX context, opens a new window with the requested
    size and title, and stores the relevant pointers for later use by the
    renderer.
    """
    def __init__(
        self,
        width: int,
        height: int,
        title: str,
    ) -> None:
        """Create a MiniLibX window.

        Args:
            width: Desired window width in pixels.
            height: Desired window height in pixels.
            title: Window title shown in the title bar.
        """
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        if self.mlx_ptr is None:
            raise RuntimeError("mlx_init failed")

        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            width,
            height,
            title,
        )

        if self.win_ptr is None:
            raise RuntimeError("mlx_new_window failed")
