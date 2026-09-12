"""Configuration parser module."""

from pathlib import Path
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


class ConfigError(Exception):
    """Custom exception raised for configuration errors."""


class Coordinates(BaseModel):
    """A coordinate inside the maze."""

    x: int
    y: int


class Config(BaseModel):
    """Validated application configuration."""

    model_config = ConfigDict(extra="ignore")

    WIDTH: int = Field(gt=0)
    HEIGHT: int = Field(gt=0)
    ENTRY: Coordinates
    EXIT: Coordinates
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: str | None = None

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def parse_coordinates(cls, value: Any) -> Coordinates:
        """Parse x,y coordinate strings into Coordinates."""
        if isinstance(value, Coordinates):
            return value

        if not isinstance(value, str):
            raise ValueError("must be in 'x,y' format")

        parts = [part.strip() for part in value.split(",")]

        if len(parts) != 2:
            raise ValueError("must be in 'x,y' format")

        try:
            x = int(parts[0])
            y = int(parts[1])
        except ValueError:
            raise ValueError("must be in 'x,y' format") from None

        return Coordinates(x=x, y=y)

    @field_validator("PERFECT", mode="before")
    @classmethod
    def parse_perfect(cls, value: Any) -> bool:
        """Accept only true/false, case-insensitively."""
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            normalized = value.strip().lower()

            if normalized == "true":
                return True

            if normalized == "false":
                return False

        raise ValueError("must be either 'true' or 'false'")

    @model_validator(mode="after")
    def validate_coordinates(self) -> "Config":
        """Validate ENTRY and EXIT against maze dimensions."""
        if not (
            0 <= self.ENTRY.x < self.WIDTH and 0 <= self.ENTRY.y < self.HEIGHT
        ):
            raise ValueError("ENTRY coordinates are out of maze bounds")

        if not (
            0 <= self.EXIT.x < self.WIDTH and 0 <= self.EXIT.y < self.HEIGHT
        ):
            raise ValueError("EXIT coordinates are out of maze bounds")

        if self.ENTRY == self.EXIT:
            raise ValueError("Entry and EXIT coordinates cannot be identical")

        return self


def parse_config(filepath: str) -> dict[str, Any]:
    """Parse and validate a configuration file."""
    try:
        raw_config = _read_config_file(filepath)
    except FileNotFoundError:
        raise ConfigError(
            f"Error: Configuration file '{filepath}' not found"
        ) from None
    except OSError as error:
        raise ConfigError(
            f"Error reading configuration file: {error}"
        ) from None

    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    missing = required_keys - raw_config.keys()

    if missing:
        keys = ", ".join(sorted(missing))
        raise ConfigError(
            f"Missing mandatory configuration keys: {keys}"
        )

    try:
        config = Config.model_validate(raw_config)
    except ValidationError as error:
        raise ConfigError(_format_validation_error(error)) from None

    result: dict[str, Any] = config.model_dump()

    result["ENTRY"] = (config.ENTRY.x, config.ENTRY.y)
    result["EXIT"] = (config.EXIT.x, config.EXIT.y)

    return result


def _read_config_file(filepath: str) -> dict[str, str]:
    """Read KEY=VALUE pairs from a configuration file."""
    raw_config: dict[str, str] = {}

    with Path(filepath).open("r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                continue

            if "=" not in stripped:
                raise ConfigError(
                    f"Syntax error on line {line_num}: "
                    f"expected 'KEY=VALUE', got '{stripped}'"
                )

            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                raise ConfigError(
                    f"Syntax error on line {line_num}: "
                    "configuration key cannot be empty"
                )

            raw_config[key] = value

    return raw_config


def _format_validation_error(error: ValidationError) -> str:
    """Convert Pydantic errors into ConfigError-friendly messages."""
    messages: list[str] = []

    for err in error.errors():
        location = err["loc"]
        message = err["msg"]

        # Model-level validation errors.
        if not location:
            messages.append(message)
            continue

        field = str(location[0])

        if field in {"WIDTH", "HEIGHT"}:
            messages.append(f"Invalid value for {field}")
        elif field in {"ENTRY", "EXIT"}:
            if "must be in 'x,y' format" in message:
                messages.append(f"Invalid format for {field}")
            elif "out of maze bounds" in message:
                messages.append(f"{field} coordinates are out of maze bounds")
            else:
                messages.append(f"Invalid value for {field}")
        elif field == "PERFECT":
            messages.append("Invalid value for PERFECT")
        else:
            messages.append(f"{field}: {message}")

    return "\n".join(messages)
