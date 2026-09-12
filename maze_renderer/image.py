from typing import Any, Protocol


class MlxProtocol(Protocol):
    """Interface for the MiniLibX methods used by MlxImage."""

    def mlx_new_image(self, mlx_ptr: Any, width: int, height: int) -> Any:
        """Create a new MLX image."""
        ...

    def mlx_get_data_addr(self, image: Any) -> tuple[Any, int, int, int]:
        """Get an image's memory address and format information."""
        ...

    def mlx_pixel_put(
        self,
        mlx_ptr: Any,
        win_ptr: Any,
        x: int,
        y: int,
        color: int,
    ) -> Any:
        """Draw a pixel directly to an MLX window."""
        ...

    def mlx_destroy_image(self, mlx_ptr: Any, image: Any) -> Any:
        """Destroy an MLX image."""
        ...


class MlxImage:
    """Manage an image buffer used for MiniLibX rendering."""

    def __init__(
        self,
        mlx: MlxProtocol,
        mlx_ptr: Any,
        width: int,
        height: int,
        win_ptr: Any | None = None,
    ) -> None:
        """Initialize an MLX image.

        Args:
            mlx: MiniLibX instance.
            mlx_ptr: MiniLibX connection pointer.
            width: Image width in pixels.
            height: Image height in pixels.
            win_ptr: Optional MLX window pointer.
        """
        self.mlx: MlxProtocol = mlx
        self.mlx_ptr: Any = mlx_ptr
        self.win_ptr: Any | None = win_ptr
        self.width: int = width
        self.height: int = height

        self.image: Any | None = mlx.mlx_new_image(mlx_ptr, width, height)

        if self.image is None:
            raise RuntimeError("mlx_new_image failed")

        (
            self.data,
            self.bits_per_pixel,
            self.line_size,
            self.endian,
        ) = mlx.mlx_get_data_addr(self.image)

        self.bytes_per_pixel: int = self.bits_per_pixel // 8
        self.pixel_format: int = self.endian

    def put_pixel(self, x: int, y: int, color: int) -> None:
        """Write a pixel to the image buffer.

        Args:
            x: Horizontal pixel coordinate.
            y: Vertical pixel coordinate.
            color: RGB color encoded as an integer.
        """
        if not self._inside(x, y):
            return

        offset: int = (y * self.line_size + x * self.bytes_per_pixel)
        pixel: bytes = self._encode_color(color)

        self.data[offset:offset + len(pixel)] = pixel

    def draw_pixel(self, x: int, y: int, color: int) -> None:
        """Draw a pixel to the image and optionally to the window.

        Args:
            x: Horizontal pixel coordinate.
            y: Vertical pixel coordinate.
            color: RGB color encoded as an integer.
        """
        self.put_pixel(x, y, color)

        if self.win_ptr is None:
            return

        self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def fill(self, color: int) -> None:
        """Fill the entire image with one color.

        Args:
            color: RGB color encoded as an integer.
        """
        pixel: bytes = self._encode_color(color)
        row: bytes = pixel * self.width

        if len(row) < self.line_size:
            padding: bytes = pixel * (
                (self.line_size - len(row) + len(pixel) - 1) // len(pixel)
            )
            row += padding[: self.line_size - len(row)]

        for y in range(self.height):
            start: int = y * self.line_size
            self.data[start:start + self.line_size] = row

    def _encode_color(self, color: int) -> bytes:
        """Convert an RGB integer to the MLX pixel format.

        Args:
            color: RGB color encoded as an integer.

        Returns:
            Color encoded as raw pixel bytes.
        """
        red: int = (color >> 16) & 0xFF
        green: int = (color >> 8) & 0xFF
        blue: int = color & 0xFF

        if self.bytes_per_pixel == 3:
            if self.pixel_format == 1:
                return bytes((red, green, blue))
            return bytes((blue, green, red))
        if self.pixel_format == 1:
            return bytes((255, red, green, blue))

        return bytes((blue, green, red, 255))

    def _inside(self, x: int, y: int) -> bool:
        """Check whether coordinates are inside the image.

        Args:
            x: Horizontal pixel coordinate.
            y: Vertical pixel coordinate.

        Returns:
            True if the coordinates are inside the image.
        """
        return (0 <= x < self.width and 0 <= y < self.height)

    def destroy(self) -> None:
        """Destroy the MLX image and release its resources."""
        if self.image is None:
            return

        self.mlx.mlx_destroy_image(self.mlx_ptr, self.image)
        self.image = None
