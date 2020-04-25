from django.test import TestCase
import textintoimage

# Create your tests here.
class textIntoImageTests(TestCase):
    def testNoChecksum(self):
        encodeText = "testing 1234"
        # test 1 bit
        textintoimage.encodeText1Bit(encodeText)
        self.assertEqual(textintoimage.decodeText1Bit(), encodeText)
        # test 2 bit
        textintoimage.encodeText2Bit(encodeText)
        self.assertEqual(textintoimage.decodeText2Bit(), encodeText)
        # test 4 bit
        textintoimage.encodeText4Bit(encodeText)
        self.assertEqual(textintoimage.decodeText4Bit(), encodeText)
    
    def testChecksum(self):
        encodeText = "testing 1234"
        # test 1 bit
        textintoimage.encodeText1BitChecksum(encodeText)
        self.assertEqual(textintoimage.decodeText1BitChecksum(), encodeText)
        # test 2 bit
        textintoimage.encodeText2BitChecksum(encodeText)
        self.assertEqual(textintoimage.decodeText2BitChecksum(), encodeText)
        # test 4 bit
        textintoimage.encodeText4BitChecksum(encodeText)
        self.assertEqual(textintoimage.decodeText4BitChecksum(), encodeText)