import unittest

from squirrelbattle.settings import Settings


class TestSettings(unittest.TestCase):
    def test_settings(self) -> None:
        """
        Ensure that settings are well loaded.
        """
        settings = Settings()
        self.assertEqual(settings.KEY_UP_PRIMARY, 'z')
        self.assertEqual(settings.KEY_DOWN_PRIMARY, 's')
        self.assertEqual(settings.KEY_LEFT_PRIMARY, 'q')
        self.assertEqual(settings.KEY_RIGHT_PRIMARY, 'd')
        self.assertEqual(settings.KEY_UP_SECONDARY, 'KEY_UP')
        self.assertEqual(settings.KEY_DOWN_SECONDARY, 'KEY_DOWN')
        self.assertEqual(settings.KEY_LEFT_SECONDARY, 'KEY_LEFT')
        self.assertEqual(settings.KEY_RIGHT_SECONDARY, 'KEY_RIGHT')
        self.assertEqual(settings.TEXTURE_PACK, 'ascii')
        self.assertEqual(settings.get_comment(settings.TEXTURE_PACK),
                         settings.get_comment('TEXTURE_PACK'))
        self.assertEqual(settings.get_comment(settings.TEXTURE_PACK),
                         'Pack de textures utilisé')

        settings.TEXTURE_PACK = 'squirrel'
        self.assertEqual(settings.TEXTURE_PACK, 'squirrel')

        settings.write_settings()
        settings.load_settings()

        self.assertEqual(settings.TEXTURE_PACK, 'squirrel')
