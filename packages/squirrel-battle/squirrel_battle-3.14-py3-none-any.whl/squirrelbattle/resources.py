from pathlib import Path


class ResourceManager:
    """
    The ResourceManager loads resources at their right place,
    and stores files in config directory.
    """
    BASE_DIR = Path(__file__).resolve().parent / 'assets'
    # FIXME This might not work on not-UNIX based systems.
    CONFIG_DIR = Path.home() / '.config' / 'squirrel-battle'

    @classmethod
    def get_asset_path(cls, filename: str) -> str:
        return str(cls.BASE_DIR / filename)

    @classmethod
    def get_config_path(cls, filename: str) -> str:
        cls.CONFIG_DIR.mkdir(parents=True) if not cls.CONFIG_DIR.is_dir() \
            else None
        return str(cls.CONFIG_DIR / filename)
