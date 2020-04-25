from django.conf import settings
from PIL import Image


def encodeText1Bit(encodeStr):
    encodeImg = Image.open(f"{settings.MEDIA_ROOT}/upload.png")
    pixelData = getPixelData(encodeImg)
    validStrLen = True
    # each char needs 3 pixels to store data
    # need 6 pixels to store up to 16 bits of string length
    if len(encodeStr) > (((pixelData[0] * pixelData[1]) // 3) - 6):
        validStrLen = False

    if validStrLen:
        binaryChars = []
        for i, char in enumerate(encodeStr):
            binaryChar = format(ord(char), "08b")
            binaryChars.append(binaryChar)

        binaryCount = format(len(encodeStr), "016b")

        charIndex = 0
        # charPart goes from 0-2 to determine
        # which part of the char is to be written
        charPart = 0
        for col in range(pixelData[0]):
            for row in range(pixelData[1]):
                pixel = encodeImg.getpixel((col, row))
                # get RGB values in binary
                red = format(pixel[0], "08b")
                green = format(pixel[1], "08b")
                blue = format(pixel[2], "08b")

                if col == 0 and row <= 5:
                    if row == 0:
                        # metadata pixel 1
                        red = red[:7] + binaryCount[0]
                        green = green[:7] + binaryCount[1]
                        blue = blue[:7] + binaryCount[2]
                    elif row == 1:
                        # metadata pixel 2
                        red = red[:7] + binaryCount[3]
                        green = green[:7] + binaryCount[4]
                        blue = blue[:7] + binaryCount[5]
                    elif row == 2:
                        # metadata pixel 3
                        red = red[:7] + binaryCount[6]
                        green = green[:7] + binaryCount[7]
                        blue = blue[:7] + binaryCount[8]
                    elif row == 3:
                        # metadata pixel 4
                        red = red[:7] + binaryCount[9]
                        green = green[:7] + binaryCount[10]
                        blue = blue[:7] + binaryCount[11]
                    elif row == 4:
                        # metadata pixel 5
                        red = red[:7] + binaryCount[12]
                        green = green[:7] + binaryCount[13]
                    elif row == 5:
                        # metadata pixel 6
                        red = red[:7] + binaryCount[14]
                        green = green[:7] + binaryCount[15]

                elif charPart == 0:
                    red = red[:7] + binaryChars[charIndex][0]
                    green = green[:7] + binaryChars[charIndex][1]
                    blue = blue[:7] + binaryChars[charIndex][2]
                    charPart = 1
                elif charPart == 1:
                    red = red[:7] + binaryChars[charIndex][3]
                    green = green[:7] + binaryChars[charIndex][4]
                    blue = blue[:7] + binaryChars[charIndex][5]
                    charPart = 2
                elif charPart == 2:
                    red = red[:7] + binaryChars[charIndex][6]
                    green = green[:7] + binaryChars[charIndex][7]
                    charPart = 0
                    charIndex += 1

                pixelData[2][col, row] = (int(red, 2), int(green, 2), int(blue, 2))

                if charIndex >= len(binaryChars):
                    # all text written, save image and exit
                    encodeImg.save(f"{settings.MEDIA_ROOT}/encoded.png")
                    return
    else:
        raise ValueError("Invalid Text Length")


def decodeText1Bit():
    encodedImg = Image.open(f"{settings.MEDIA_ROOT}/encoded.png")
    pixelData = getPixelData(encodedImg)
    decodedString = ""

    # get metadata pixels
    textlen = ""
    for row in range(6):
        textLenPixel = encodedImg.getpixel((0, row))
        if row < 4:
            textlen += (
                format(textLenPixel[0], "08b")[7]
                + format(textLenPixel[1], "08b")[7]
                + format(textLenPixel[2], "08b")[7]
            )
        else:
            textlen += (
                format(textLenPixel[0], "08b")[7] + format(textLenPixel[1], "08b")[7]
            )

    textlen = int(textlen, 2)

    # loop through image and extract text
    charPart = 0
    for col in range(pixelData[0]):
        for row in range(pixelData[1]):
            if col == 0 and row <= 5:
                # metadata pixel, skip
                continue

            pixel = encodedImg.getpixel((col, row))
            if textlen > 0:
                if charPart == 0:
                    binaryChar = (
                        format(pixel[0], "08b")[7]
                        + format(pixel[1], "08b")[7]
                        + format(pixel[2], "08b")[7]
                    )
                    charPart = 1
                elif charPart == 1:
                    binaryChar += (
                        format(pixel[0], "08b")[7]
                        + format(pixel[1], "08b")[7]
                        + format(pixel[2], "08b")[7]
                    )
                    charPart = 2
                elif charPart == 2:
                    binaryChar += (
                        format(pixel[0], "08b")[7] + format(pixel[1], "08b")[7]
                    )
                    decodedString += chr(int(binaryChar, 2))
                    charPart = 0
                    textlen -= 1
            else:
                return decodedString


def encodeText2Bit(encodeStr):
    encodeImg = Image.open(f"{settings.MEDIA_ROOT}/upload.png")
    pixelData = getPixelData(encodeImg)
    validStrLen = True
    if len(encodeStr) > (((pixelData[0] * pixelData[1]) // 2) - 4):
        validStrLen = False

    if validStrLen:
        binaryChars = []
        for i, char in enumerate(encodeStr):
            binaryChar = format(ord(char), "08b")
            binaryChars.append(binaryChar)

        binaryCount = format(len(encodeStr), "016b")

        charIndex = 0
        # firstHalf indicates if the first half needs to be written
        # or if the second half needs to be written
        firstHalf = True
        for col in range(pixelData[0]):
            for row in range(pixelData[1]):
                pixel = encodeImg.getpixel((col, row))
                # get RGB values in binary
                red = format(pixel[0], "08b")
                green = format(pixel[1], "08b")
                blue = pixel[2]

                if col == 0 and row <= 3:
                    if row == 0:
                        # metadata pixel 1
                        red = red[:6] + binaryCount[:2]
                        green = green[:6] + binaryCount[2:4]
                    elif row == 1:
                        # metadata pixel 2
                        red = red[:6] + binaryCount[4:6]
                        green = green[:6] + binaryCount[6:8]
                    elif row == 2:
                        # metadata pixel 3
                        red = red[:6] + binaryCount[8:10]
                        green = green[:6] + binaryCount[10:12]
                    elif row == 3:
                        # metadata pixel 4
                        red = red[:6] + binaryCount[12:14]
                        green = green[:6] + binaryCount[14:]

                elif firstHalf:
                    red = red[:6] + binaryChars[charIndex][:2]
                    green = green[:6] + binaryChars[charIndex][2:4]
                    firstHalf = False
                elif not firstHalf:
                    red = red[:6] + binaryChars[charIndex][4:6]
                    green = green[:6] + binaryChars[charIndex][6:]
                    charIndex += 1
                    firstHalf = True

                pixelData[2][col, row] = (int(red, 2), int(green, 2), blue)

                if charIndex >= len(binaryChars):
                    # all text written, save image and exit
                    encodeImg.save(f"{settings.MEDIA_ROOT}/encoded.png")
                    return
    else:
        raise ValueError("Invalid Text Length")


def decodeText2Bit():
    encodedImg = Image.open(f"{settings.MEDIA_ROOT}/encoded.png")
    pixelData = getPixelData(encodedImg)
    decodedString = ""

    # get metadata pixels
    textlen = ""
    for row in range(4):
        textLenPixel = encodedImg.getpixel((0, row))
        textlen += (
            format(textLenPixel[0], "08b")[6:] + format(textLenPixel[1], "08b")[6:]
        )

    textlen = int(textlen, 2)

    # loop through image and extract text
    firstHalf = True
    for col in range(pixelData[0]):
        for row in range(pixelData[1]):
            if col == 0 and row <= 3:
                # metadata pixel, skip
                continue

            pixel = encodedImg.getpixel((col, row))
            if textlen > 0:
                if firstHalf:
                    binaryChar = (
                        format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                    )
                    firstHalf = False
                elif not firstHalf:
                    binaryChar += (
                        format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                    )
                    decodedString += chr(int(binaryChar, 2))
                    textlen -= 1
                    firstHalf = True
            else:
                return decodedString


def encodeText4Bit(encodeStr):
    encodeImg = Image.open(f"{settings.MEDIA_ROOT}/upload.png")
    pixelData = getPixelData(encodeImg)
    validStrLen = True
    if len(encodeStr) > ((pixelData[0] * pixelData[1]) - 2):
        validStrLen = False

    if validStrLen:
        binaryChars = []
        for i, char in enumerate(encodeStr):
            binaryChar = format(ord(char), "08b")
            binaryChars.append(binaryChar)

        binaryCount = format(len(encodeStr), "016b")

        charIndex = 0
        # for column in width
        for col in range(pixelData[0]):
            # for row in height
            for row in range(pixelData[1]):
                pixel = encodeImg.getpixel((col, row))

                # get RGB values in binary
                red = format(pixel[0], "08b")
                green = format(pixel[1], "08b")
                blue = pixel[2]

                if col == 0 and row <= 1:
                    if row == 0:
                        # metadata pixel 1
                        red = red[:4] + binaryCount[:4]
                        green = green[:4] + binaryCount[4:8]
                    elif row == 1:
                        # metadata pixel 2
                        red = red[:4] + binaryCount[8:12]
                        green = green[:4] + binaryCount[12:]
                else:
                    # pixel holds text data
                    red = red[:4] + binaryChars[charIndex][:4]
                    green = green[:4] + binaryChars[charIndex][4:]
                    charIndex += 1

                pixelData[2][col, row] = (int(red, 2), int(green, 2), blue)

                if charIndex >= len(binaryChars):
                    # all text written, save image and exit
                    encodeImg.save(f"{settings.MEDIA_ROOT}/encoded.png")
                    return
    else:
        raise ValueError("Invalid Text Length")


def decodeText4Bit():
    encodedImg = Image.open(f"{settings.MEDIA_ROOT}/encoded.png")
    pixelData = getPixelData(encodedImg)
    decodedString = ""

    # get metadata pixels
    textlen = ""
    for row in range(2):
        textLenPixel = encodedImg.getpixel((0, row))
        textlen += (
            format(textLenPixel[0], "08b")[4:] + format(textLenPixel[1], "08b")[4:]
        )

    textlen = int(textlen, 2)

    # loop through image and extract text
    for col in range(pixelData[0]):
        for row in range(pixelData[1]):
            if col == 0 and row <= 1:
                # metadata pixel, skip
                continue

            pixel = encodedImg.getpixel((col, row))
            if textlen > 0:
                binaryChar = format(pixel[0], "08b")[4:] + format(pixel[1], "08b")[4:]
                decodedString += chr(int(binaryChar, 2))
                textlen -= 1
            else:
                return decodedString


def encodeText2BitChecksum(encodeStr):
    encodeImg = Image.open(f"{settings.MEDIA_ROOT}/upload.png")
    pixelData = getPixelData(encodeImg)
    validStrLen = True
    # 3 pixels for each character, 2 for the character and 1 for checksum
    # 6 pixels for length of string, 4 for length and 2 for checksum
    if len(encodeStr) > (((pixelData[0] * pixelData[1]) // 3) - 6):
        validStrLen = False

    if validStrLen:
        binaryChars = []
        pixel0Checksum = []
        pixel1Checksum = []
        comboChecksum = []
        for i, char in enumerate(encodeStr):
            binaryChar = format(ord(char), "08b")
            binaryChars.append(binaryChar)
            pixel0Checksum.append(
                format(int(binaryChars[i][:2], 2) ^ int(binaryChars[i][2:4], 2), "02b")
            )
            pixel1Checksum.append(
                format(int(binaryChars[i][4:6], 2) ^ int(binaryChars[i][6:], 2), "02b")
            )
            comboChecksum.append(
                format(int(binaryChars[i][2:4], 2) ^ int(binaryChars[i][6:], 2), "02b")
            )

        binaryCount = format(len(encodeStr), "016b")
        binaryCountChecksums0 = []
        binaryCountChecksums1 = []
        binaryCountChecksums0.append(
            format(int(binaryCount[:2], 2) ^ int(binaryCount[2:4], 2), "02b")
        )
        binaryCountChecksums0.append(
            format(int(binaryCount[4:6], 2) ^ int(binaryCount[6:8], 2), "02b")
        )
        binaryCountChecksums0.append(
            format(int(binaryCount[2:4], 2) ^ int(binaryCount[6:8], 2), "02b")
        )
        binaryCountChecksums1.append(
            format(int(binaryCount[8:10], 2) ^ int(binaryCount[10:12], 2), "02b")
        )
        binaryCountChecksums1.append(
            format(int(binaryCount[12:14], 2) ^ int(binaryCount[14:], 2), "02b")
        )
        binaryCountChecksums1.append(
            format(int(binaryCount[10:12], 2) ^ int(binaryCount[14:], 2), "02b")
        )

        charIndex = 0
        # text indicates if the char needs to be written or the checksum
        text = True
        # firstHalf indicates if the first half needs to be written
        # or if the second half needs to be written
        firstHalf = True
        for col in range(pixelData[0]):
            for row in range(pixelData[1]):
                pixel = encodeImg.getpixel((col, row))
                # get RGB values in binary
                red = format(pixel[0], "08b")
                green = format(pixel[1], "08b")
                blue = format(pixel[2], "08b")

                if col == 0 and row <= 5:
                    if row == 0:
                        # metadata pixel 1
                        red = red[:6] + binaryCount[:2]
                        green = green[:6] + binaryCount[2:4]
                    elif row == 1:
                        # metadata pixel 2
                        red = red[:6] + binaryCount[4:6]
                        green = green[:6] + binaryCount[6:8]
                    elif row == 2:
                        # metadata pixel 3
                        red = red[:6] + binaryCount[8:10]
                        green = green[:6] + binaryCount[10:12]
                    elif row == 3:
                        # metadata pixel 4
                        red = red[:6] + binaryCount[12:14]
                        green = green[:6] + binaryCount[14:]
                    elif row == 4:
                        # metadata checksum pixel 1
                        red = red[:6] + binaryCountChecksums0[0]
                        green = green[:6] + binaryCountChecksums0[1]
                        blue = blue[:6] + binaryCountChecksums0[2]
                    elif row == 5:
                        # metadata checksum pixel 2
                        red = red[:6] + binaryCountChecksums1[0]
                        green = green[:6] + binaryCountChecksums1[1]
                        blue = blue[:6] + binaryCountChecksums1[2]
                elif text:
                    if firstHalf:
                        red = red[:6] + binaryChars[charIndex][:2]
                        green = green[:6] + binaryChars[charIndex][2:4]
                        firstHalf = False
                    elif not firstHalf:
                        red = red[:6] + binaryChars[charIndex][4:6]
                        green = green[:6] + binaryChars[charIndex][6:]
                        firstHalf = True
                        text = False
                elif not text:
                    # write checksum pixel
                    red = red[:6] + pixel0Checksum[charIndex]
                    green = green[:6] + pixel1Checksum[charIndex]
                    blue = blue[:6] + comboChecksum[charIndex]
                    charIndex += 1
                    text = True

                pixelData[2][col, row] = (int(red, 2), int(green, 2), int(blue, 2))

                if charIndex >= len(binaryChars):
                    # all text written, save image and exit
                    encodeImg.save(f"{settings.MEDIA_ROOT}/encoded.png")
                    return
    else:
        raise ValueError("Invalid Text Length")


def decodeText2BitChecksum():
    encodedImg = Image.open(f"{settings.MEDIA_ROOT}/encoded.png")
    pixelData = getPixelData(encodedImg)
    decodedString = ""

    # get metadata pixels
    textlen = ""
    for row in range(4):
        textLenPixel = encodedImg.getpixel((0, row))
        textlen += (
            format(textLenPixel[0], "08b")[6:] + format(textLenPixel[1], "08b")[6:]
        )
    # get metadata checksum pixels
    textlenChecksums = []
    for row in range(4, 6):
        checksumPixel = encodedImg.getpixel((0, row))
        textlenChecksums.append(format(checksumPixel[0], "08b")[6:])
        textlenChecksums.append(format(checksumPixel[1], "08b")[6:])
        textlenChecksums.append(format(checksumPixel[2], "08b")[6:])

    textlen0 = validateChar2Bit(textlen[:8], textlenChecksums[:3])
    textlen1 = validateChar2Bit(textlen[8:], textlenChecksums[3:])
    textlen = int(textlen0 + textlen1, 2)

    # loop through image and extract text
    text = True
    firstHalf = True
    for col in range(pixelData[0]):
        for row in range(pixelData[1]):
            if col == 0 and row <= 5:
                # metadata pixel, skip
                continue

            pixel = encodedImg.getpixel((col, row))
            if textlen > 0:
                if text:
                    if firstHalf:
                        binaryChar = (
                            format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                        )
                        firstHalf = False
                    elif not firstHalf:
                        binaryChar += (
                            format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                        )
                        firstHalf = True
                        text = False
                elif not text:
                    checksums = []
                    checksums.append(format(pixel[0], "08b")[6:])
                    checksums.append(format(pixel[1], "08b")[6:])
                    checksums.append(format(pixel[2], "08b")[6:])
                    validated = validateChar2Bit(binaryChar, checksums)
                    decodedString += chr(int(validated, 2))
                    textlen -= 1
                    text = True
            else:
                return decodedString


def validateChar2Bit(binaryChar, checksums):
    validChecks = [True, True, True]
    testChecksums = []
    testChecksums.append(
        format(int(binaryChar[:2], 2) ^ int(binaryChar[2:4], 2), "02b")
    )
    testChecksums.append(
        format(int(binaryChar[4:6], 2) ^ int(binaryChar[6:], 2), "02b")
    )
    testChecksums.append(
        format(int(binaryChar[2:4], 2) ^ int(binaryChar[6:], 2), "02b")
    )
    for i, checksum in enumerate(checksums):
        if testChecksums[i] != checksum:
            validChecks[i] = False

    if False in validChecks:
        if not validChecks[2]:
            # [2:4] or [6:] are wrong
            if not validChecks[0]:
                # [2:4] wrong
                correction = format(
                    int(checksums[2], 2) ^ int(binaryChar[6:], 2), "02b"
                )
                binaryChar = binaryChar[:2] + correction + binaryChar[4:]
            elif not validChecks[1]:
                # [6:] wrong
                correction = format(
                    int(checksums[2], 2) ^ int(binaryChar[2:4], 2), "02b"
                )
                binaryChar = binaryChar[:6] + correction
        elif validChecks[2]:
            # [:2] or [4:6] are wrong
            if not validChecks[0]:
                # [:2] wrong
                correction = format(
                    int(checksums[0], 2) ^ int(binaryChar[2:4], 2), "02b"
                )
                binaryChar = correction + binaryChar[2:]
            elif not validChecks[1]:
                # [4:6] wrong
                correction = format(
                    int(checksums[1], 2) ^ int(binaryChar[6:], 2), "02b"
                )
                binaryChar = binaryChar[:4] + correction + binaryChar[6:]
    return binaryChar


def encodeText4BitChecksum(encodeStr):
    encodeImg = Image.open(f"{settings.MEDIA_ROOT}/upload.png")
    pixelData = getPixelData(encodeImg)
    validStrLen = True
    if len(encodeStr) > ((pixelData[0] * pixelData[1]) // 2) - 2:
        validStrLen = False

    if validStrLen:
        binaryChars = []
        row0Checksum = []
        row1Checksum = []
        columnarChecksum = []
        for i, char in enumerate(encodeStr):
            binaryChar = format(ord(char), "08b")
            binaryChars.append(binaryChar)
            row0Checksum.append(format(binaryChar.count("1", 0, 4), "04b"))
            row1Checksum.append(format(binaryChar.count("1", 4, 8), "04b"))
            bitwiseColumns = ""
            for j in range(4):
                bitwiseColumns += str(int(binaryChar[j], 2) ^ int(binaryChar[j + 4], 2))
            columnarChecksum.append(bitwiseColumns)

        binaryCount = format(len(encodeStr), "016b")
        countRow0Checksum = format(binaryCount.count("1", 0, 4), "04b")
        countRow1Checksum = format(binaryCount.count("1", 4, 8), "04b")
        countRow2Checksum = format(binaryCount.count("1", 8, 12), "04b")
        countRow3Checksum = format(binaryCount.count("1", 12, 16), "04b")
        countColumnarChecksum0 = ""
        countColumnarChecksum1 = ""
        for i in range(4):
            countColumnarChecksum0 += str(
                int(binaryCount[i], 2) ^ int(binaryCount[i + 4], 2)
            )
            countColumnarChecksum1 += str(
                int(binaryCount[i + 8], 2) ^ int(binaryCount[i + 12], 2)
            )

        charIndex = 0
        # text is true if the pixel holds text
        # false if the pixel holds checksums
        text = True
        for col in range(pixelData[0]):
            for row in range(pixelData[1]):
                pixel = encodeImg.getpixel((col, row))

                # get RGB values in binary
                red = format(pixel[0], "08b")
                green = format(pixel[1], "08b")
                blue = format(pixel[2], "08b")

                if col == 0 and row <= 3:
                    if row == 0:
                        # metadata pixel 1
                        red = red[:4] + binaryCount[:4]
                        green = green[:4] + binaryCount[4:8]
                    elif row == 1:
                        # metadata pixel 1 checksums
                        red = red[:4] + countRow0Checksum
                        green = green[:4] + countRow1Checksum
                        blue = blue[:4] + countColumnarChecksum0
                    elif row == 2:
                        # metadata pixel 2
                        red = red[:4] + binaryCount[8:12]
                        green = green[:4] + binaryCount[12:]
                    elif row == 3:
                        # metadata pixel 2 checksums
                        red = red[:4] + countRow2Checksum
                        green = green[:4] + countRow3Checksum
                        blue = blue[:4] + countColumnarChecksum1
                elif text:
                    # pixel holds text data
                    red = red[:4] + binaryChars[charIndex][:4]
                    green = green[:4] + binaryChars[charIndex][4:]
                    text = False
                elif not text:
                    # pixel holds checksums for prev pixel
                    red = red[:4] + row0Checksum[charIndex]
                    green = green[:4] + row1Checksum[charIndex]
                    blue = blue[:4] + columnarChecksum[charIndex]
                    charIndex += 1
                    text = True

                pixelData[2][col, row] = (int(red, 2), int(green, 2), int(blue, 2))

                if charIndex >= len(binaryChars):
                    # all text written, save image and exit
                    encodeImg.save(f"{settings.MEDIA_ROOT}/encoded.png")
                    return
    else:
        raise ValueError("Invalid Text Length")


def decodeText4BitChecksum():
    encodedImg = Image.open(f"{settings.MEDIA_ROOT}/encoded.png")
    pixelData = getPixelData(encodedImg)
    decodedString = ""

    # get metadata pixels
    textLenPixel0 = encodedImg.getpixel((0, 0))
    textLenChecksumsPixel0 = encodedImg.getpixel((0, 1))
    textLenPixel1 = encodedImg.getpixel((0, 2))
    textLenChecksumsPixel1 = encodedImg.getpixel((0, 3))

    textLen0 = format(textLenPixel0[0], "08b")[4:] + format(textLenPixel0[1], "08b")[4:]
    textLenChecksums0 = [
        format(textLenChecksumsPixel0[0], "08b")[4:],
        format(textLenChecksumsPixel0[1], "08b")[4:],
        format(textLenChecksumsPixel0[2], "08b")[4:],
    ]

    textLen1 = format(textLenPixel1[0], "08b")[4:] + format(textLenPixel1[1], "08b")[4:]
    textLenChecksums1 = [
        format(textLenChecksumsPixel1[0], "08b")[4:],
        format(textLenChecksumsPixel1[1], "08b")[4:],
        format(textLenChecksumsPixel1[2], "08b")[4:],
    ]

    textLen0 = validateChar4Bit(textLen0, textLenChecksums0)
    textLen1 = validateChar4Bit(textLen1, textLenChecksums1)
    textlen = int(textLen0 + textLen1, 2)

    # text is true if the pixel holds text
    # false if the pixel holds checksums
    text = True
    # loop through image and extract text
    for col in range(pixelData[0]):
        for row in range(pixelData[1]):
            if col == 0 and row <= 3:
                # metadata pixel, skip
                continue

            pixel = encodedImg.getpixel((col, row))
            if textlen > 0:
                if text:
                    binaryChar = (
                        format(pixel[0], "08b")[4:] + format(pixel[1], "08b")[4:]
                    )
                    text = False
                elif not text:
                    checksums = [
                        format(pixel[0], "08b")[4:],
                        format(pixel[1], "08b")[4:],
                        format(pixel[2], "08b")[4:],
                    ]
                    binaryChar = int(validateChar4Bit(binaryChar, checksums), 2)
                    decodedString += chr(binaryChar)
                    textlen -= 1
                    text = True
            else:
                return decodedString


def validateChar4Bit(binaryChar, checksums):
    row0Valid = row1Valid = True
    # calculate columnar check sum for binaryChar
    for i in range(4):
        colsCheckSum = str(int(binaryChar[i], 2) ^ int(binaryChar[i + 4], 2))

    # check row validity
    if format(int(binaryChar[:4].count("1")), "04b") != checksums[0]:
        row0Valid = False
    if format(int(binaryChar[4:].count("1")), "04b") != checksums[1]:
        row1Valid = False

    # if a row is invalid, determine invalid column(s)
    if not row0Valid or not row1Valid:
        for i, val in enumerate(colsCheckSum):
            if val != checksums[2][i]:
                # column i is invalid, check rows and swap value if necessary
                if not row0Valid:
                    if binaryChar[i] == 0:
                        binaryChar = binaryChar[:i] + "1" + binaryChar[i + 1 :]
                    else:
                        binaryChar = binaryChar[:i] + "0" + binaryChar[i + 1 :]
                if not row1Valid:
                    if binaryChar[i + 4] == 0:
                        binaryChar = binaryChar[: i + 4] + "1" + binaryChar[i + 5 :]
                    else:
                        binaryChar = binaryChar[: i + 4] + "0" + binaryChar[i + 5 :]
    return binaryChar


def getPixelData(image):
    width, height = image.size
    pixels = image.load()
    pixelData = [width, height, pixels]
    return pixelData


def main():
    encodeText = "testing 1234"
    # encodeText4BitChecksum(encodeText)
    # print()
    # print("4 bit checksum decode:")
    # print(decodeText4BitChecksum())
    # print()
    # encodeText2BitChecksum(encodeText)
    # print("2 bit checksum decode:")
    # print(decodeText2BitChecksum())
    # print()
    # encodeText1BitChecksum(encodeText)
    # print("1 bit checksum decode:")
    # print(decodeText1BitChecksum())
    # print()
    # encodeText4Bit(encodeText)
    # print("4 bit decode:")
    # print(decodeText4Bit())
    # print()
    # encodeText2Bit(encodeText)
    # print("2 bit decode:")
    # print(decodeText2Bit())
    # print()
    # encodeText1Bit(encodeText)
    # print("1 bit decode:")
    # print(decodeText1Bit())
    # print()


if __name__ == "__main__":
    main()
