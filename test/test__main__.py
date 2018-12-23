import unittest
import unittest.mock

import denonavr.__main__ as avr


class TestDenonAVR(unittest.TestCase):
    def test_valid_input_source(self):
        self.assertTrue(avr._is_valid_input_source("DVD"))
        self.assertTrue(avr._is_valid_input_source("BD"))
        self.assertTrue(avr._is_valid_input_source("GAME"))
        self.assertTrue(avr._is_valid_input_source("SAT/CBL"))
        self.assertFalse(avr._is_valid_input_source("VHS"))

    def test_convert_input_source(self):
        self.assertEqual(avr._convert_input_source("satcbl"), "SAT/CBL")
        self.assertEqual(avr._convert_input_source("vhs"), "VHS")

    def test_execute(self):
        with unittest.mock.patch("telnetlib.Telnet") as telnet_mock:
            telnet_mock.return_value.read_until.return_value = "b'Test\\r'"
            self.assertEqual(avr.execute("?Test", avr.CONFIG), "Test")
            telnet_mock.return_value.write.assert_called_once_with(b'?Test\r')
            telnet_mock.return_value.close.assert_called_once()

    def test_execute_error(self):
        with unittest.mock.patch("telnetlib.Telnet") as telnet_mock:
            telnet_mock.return_value.write.side_effect = OSError
            self.assertEqual(avr.execute("CMD", avr.CONFIG), "ERROR")

            telnet_mock.return_value = unittest.mock.MagicMock(spec=["write", "read_until", "close"])
            telnet_mock.side_effect = None
            telnet_mock.return_value.write.side_effect = OSError
            self.assertEqual(avr.execute("CMD", avr.CONFIG), "ERROR")
            telnet_mock.return_value.close.assert_called()


if __name__ == '__main__':
    unittest.main()
