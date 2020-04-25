from django.conf import settings
from PIL import Image


def encodeImage1Bit():
    innerImg = Image.open(f"{settings.MEDIA_ROOT}/upload_inner.png")
    outerImg = Image.open(f"{settings.MEDIA_ROOT}/upload_outer.png")
    innerPixelData = getPixelData(innerImg)
    outerPixelData = getPixelData(outerImg)
    innerWidth = innerPixelData[0]
    innerHeight = innerPixelData[1]
    validImgSize = True
    # Each pixel from inner needs 9 pixels in outer to be stored
    # 12 pixels are needed for the width and height of the inner image
    if (outerPixelData[0] * outerPixelData[1] * 9) - 12 < (innerWidth * innerHeight):
        validImgSize = False

    binaryCols = format(innerWidth, "016b")
    binaryRows = format(innerHeight, "016b")

    pixPart = 0
    pixelCount = 0
    innerCol = 0
    innerRow = 0
    if validImgSize:
        for col in range(outerPixelData[0]):
            for row in range(outerPixelData[1]):
                pixel = outerImg.getpixel((col, row))

                # RGB values
                red = format(pixel[0], "08b")
                green = format(pixel[1], "08b")
                blue = format(pixel[2], "08b")

                currentInnerPixel = innerImg.getpixel((innerCol, innerRow))
                innerRed = format(currentInnerPixel[0], "08b")
                innerGreen = format(currentInnerPixel[1], "08b")
                innerBlue = format(currentInnerPixel[2], "08b")
                if col == 0 and row <= 11:
                    if row == 0:
                        # metadata pixel 1
                        red = red[:7] + binaryCols[0]
                        green = green[:7] + binaryCols[1]
                        blue = blue[:7] + binaryCols[2]
                    elif row == 1:
                        # metadata pixel 2
                        red = red[:7] + binaryCols[3]
                        green = green[:7] + binaryCols[4]
                        blue = blue[:7] + binaryCols[5]
                    elif row == 2:
                        # metadata pixel 3
                        red = red[:7] + binaryCols[6]
                        green = green[:7] + binaryCols[7]
                        blue = blue[:7] + binaryCols[8]
                    elif row == 3:
                        # metadata pixel 4
                        red = red[:7] + binaryCols[9]
                        green = green[:7] + binaryCols[10]
                        blue = blue[:7] + binaryCols[11]
                    elif row == 4:
                        # metadata pixel 5
                        red = red[:7] + binaryCols[12]
                        green = green[:7] + binaryCols[13]
                    elif row == 5:
                        # metadata pixel 6
                        red = red[:7] + binaryCols[14]
                        green = green[:7] + binaryCols[15]
                    elif row == 6:
                        # metadata pixel 7
                        red = red[:7] + binaryRows[0]
                        green = green[:7] + binaryRows[1]
                        blue = blue[:7] + binaryRows[2]
                    elif row == 7:
                        # metadata pixel 8
                        red = red[:7] + binaryRows[3]
                        green = green[:7] + binaryRows[4]
                        blue = blue[:7] + binaryRows[5]
                    elif row == 8:
                        # metadata pixel 9
                        red = red[:7] + binaryRows[6]
                        green = green[:7] + binaryRows[7]
                        blue = blue[:7] + binaryRows[8]
                    elif row == 9:
                        # metadata pixel 10
                        red = red[:7] + binaryRows[9]
                        green = green[:7] + binaryRows[10]
                        blue = blue[:7] + binaryRows[11]
                    elif row == 10:
                        # metadata pixel 11
                        red = red[:7] + binaryRows[12]
                        green = green[:7] + binaryRows[13]
                    elif row == 11:
                        # metadata pixel 12
                        red = red[:7] + binaryRows[14]
                        green = green[:7] + binaryRows[15]
                elif pixPart == 0:
                    red = red[:7] + innerRed[0]
                    green = green[:7] + innerRed[1]
                    blue = blue[:7] + innerRed[2]
                    pixPart = 1
                elif pixPart == 1:
                    red = red[:7] + innerRed[3]
                    green = green[:7] + innerRed[4]
                    blue = blue[:7] + innerRed[5]
                    pixPart = 2
                elif pixPart == 2:
                    red = red[:7] + innerRed[6]
                    green = green[:7] + innerRed[7]
                    pixPart = 3
                elif pixPart == 3:
                    red = red[:7] + innerGreen[0]
                    green = green[:7] + innerGreen[1]
                    blue = blue[:7] + innerGreen[2]
                    pixPart = 4
                elif pixPart == 4:
                    red = red[:7] + innerGreen[3]
                    green = green[:7] + innerGreen[4]
                    blue = blue[:7] + innerGreen[5]
                    pixPart = 5
                elif pixPart == 5:
                    red = red[:7] + innerGreen[6]
                    green = green[:7] + innerGreen[7]
                    pixPart = 6
                elif pixPart == 6:
                    red = red[:7] + innerBlue[0]
                    green = green[:7] + innerBlue[1]
                    blue = blue[:7] + innerBlue[2]
                    pixPart = 7
                elif pixPart == 7:
                    red = red[:7] + innerBlue[3]
                    green = green[:7] + innerBlue[4]
                    blue = blue[:7] + innerBlue[5]
                    pixPart = 8
                elif pixPart == 8:
                    red = red[:7] + innerBlue[6]
                    green = green[:7] + innerBlue[7]
                    pixPart = 0
                    pixelCount += 1
                    innerRow = (innerRow + 1) % innerHeight
                    if innerRow == 0:
                        innerCol = innerCol + 1

                outerPixelData[2][col, row] = (int(red, 2), int(green, 2), int(blue, 2))

                if pixelCount >= innerPixelData[0] * innerPixelData[1]:
                    outerImg.save(f"{settings.MEDIA_ROOT}/encoded.png")
                    return
    else:
        raise ValueError("Inner Image too Large for Outer Image")


def decodeImage1Bit():
    encodedImg = Image.open(f"{settings.MEDIA_ROOT}/encoded.png")
    pixelData = getPixelData(encodedImg)

    width = ""
    height = ""
    # get metadata pixels
    for row in range(6):
        # width metadata pixels
        widthPixel = encodedImg.getpixel((0, row))
        if row < 4:
            width += (
                format(widthPixel[0], "08b")[7]
                + format(widthPixel[1], "08b")[7]
                + format(widthPixel[2], "08b")[7]
            )
        else:
            width += format(widthPixel[0], "08b")[7] + format(widthPixel[1], "08b")[7]
    for row in range(6, 12):
        # height metadata pixels
        heightPixel = encodedImg.getpixel((0, row))
        if row < 10:
            height += (
                format(heightPixel[0], "08b")[7]
                + format(heightPixel[1], "08b")[7]
                + format(heightPixel[2], "08b")[7]
            )
        else:
            height += (
                format(heightPixel[0], "08b")[7] + format(heightPixel[1], "08b")[7]
            )

    width = int(width, 2)
    height = int(height, 2)
    remainingPixels = width * height

    # create new image
    hiddenImg = Image.new("RGB", (width, height))
    hiddenPixels = hiddenImg.load()

    pixPart = 0
    innerCol = 0
    innerRow = 0
    for col in range(pixelData[0]):
        for row in range(pixelData[1]):
            if col == 0 and row < 12:
                # metadata pixel, skip
                continue

            pixel = encodedImg.getpixel((col, row))
            if remainingPixels > 0:
                if pixPart == 0:
                    # red 1/3
                    red = (
                        format(pixel[0], "08b")[7]
                        + format(pixel[1], "08b")[7]
                        + format(pixel[2], "08b")[7]
                    )
                    pixPart = 1
                elif pixPart == 1:
                    # red 2/3
                    red += (
                        format(pixel[0], "08b")[7]
                        + format(pixel[1], "08b")[7]
                        + format(pixel[2], "08b")[7]
                    )
                    pixPart = 2
                elif pixPart == 2:
                    # red 3/3
                    red += format(pixel[0], "08b")[7] + format(pixel[1], "08b")[7]
                    pixPart = 3
                elif pixPart == 3:
                    # green 1/3
                    green = (
                        format(pixel[0], "08b")[7]
                        + format(pixel[1], "08b")[7]
                        + format(pixel[2], "08b")[7]
                    )
                    pixPart = 4
                elif pixPart == 4:
                    # green 2/3
                    green += (
                        format(pixel[0], "08b")[7]
                        + format(pixel[1], "08b")[7]
                        + format(pixel[2], "08b")[7]
                    )
                    pixPart = 5
                elif pixPart == 5:
                    # green 3/3
                    green += format(pixel[0], "08b")[7] + format(pixel[1], "08b")[7]
                    pixPart = 6
                elif pixPart == 6:
                    # blue 1/3
                    blue = (
                        format(pixel[0], "08b")[7]
                        + format(pixel[1], "08b")[7]
                        + format(pixel[2], "08b")[7]
                    )
                    pixPart = 7
                elif pixPart == 7:
                    # blue 2/3
                    blue += (
                        format(pixel[0], "08b")[7]
                        + format(pixel[1], "08b")[7]
                        + format(pixel[2], "08b")[7]
                    )
                    pixPart = 8
                elif pixPart == 8:
                    # blue 3/3
                    blue += format(pixel[0], "08b")[7] + format(pixel[1], "08b")[7]
                    pixPart = 0
                    remainingPixels -= 1
                    hiddenPixels[innerCol, innerRow] = (
                        int(red, 2),
                        int(green, 2),
                        int(blue, 2),
                    )
                    innerRow = (innerRow + 1) % height
                    if innerRow == 0:
                        innerCol = innerCol + 1
            else:
                hiddenImg.save(f"{settings.MEDIA_ROOT}/decoded.png")
                return


def encodeImage2Bit():
    innerImg = Image.open(f"{settings.MEDIA_ROOT}/upload_inner.png")
    outerImg = Image.open(f"{settings.MEDIA_ROOT}/upload_outer.png")
    innerPixelData = getPixelData(innerImg)
    outerPixelData = getPixelData(outerImg)
    innerWidth = innerPixelData[0]
    innerHeight = innerPixelData[1]
    validImgSize = True
    # Each pixel of inner needs 6 pixels from outer to encode
    # 6 pixels are used for metadata
    if (outerPixelData[0] * outerPixelData[1] * 6) - 6 < innerWidth * innerHeight:
        validImgSize = False

    binaryCols = format(innerWidth, "016b")
    binaryRows = format(innerHeight, "016b")

    pixPart = 0
    pixelCount = 0
    innerCol = 0
    innerRow = 0
    if validImgSize:
        for col in range(outerPixelData[0]):
            for row in range(outerPixelData[1]):
                pixel = outerImg.getpixel((col, row))

                # RGB values
                red = format(pixel[0], "08b")
                green = format(pixel[1], "08b")
                blue = format(pixel[2], "08b")

                currentInnerPixel = innerImg.getpixel((innerCol, innerRow))
                innerRed = format(currentInnerPixel[0], "08b")
                innerGreen = format(currentInnerPixel[1], "08b")
                innerBlue = format(currentInnerPixel[2], "08b")
                if col == 0 and row <= 5:
                    if row == 0:
                        # metadata pixel 1
                        red = red[:6] + binaryCols[:2]
                        green = green[:6] + binaryCols[2:4]
                        blue = blue[:6] + binaryCols[4:6]
                    elif row == 1:
                        # metadata pixel 2
                        red = red[:6] + binaryCols[6:8]
                        green = green[:6] + binaryCols[8:10]
                        blue = blue[:6] + binaryCols[10:12]
                    elif row == 2:
                        # metadata pixel 3
                        red = red[:6] + binaryCols[12:14]
                        green = green[:6] + binaryCols[14:]
                    elif row == 3:
                        # metadata pixel 4
                        red = red[:6] + binaryRows[:2]
                        green = green[:6] + binaryRows[2:4]
                        blue = blue[:6] + binaryRows[4:6]
                    elif row == 4:
                        # metadata pixel 5
                        red = red[:6] + binaryRows[6:8]
                        green = green[:6] + binaryRows[8:10]
                        blue = blue[:6] + binaryRows[10:12]
                    elif row == 5:
                        # metadata pixel 6
                        red = red[:6] + binaryRows[12:14]
                        green = green[:6] + binaryRows[14:]
                elif pixPart == 0:
                    red = red[:6] + innerRed[:2]
                    green = green[:6] + innerRed[2:4]
                    pixPart = 1
                elif pixPart == 1:
                    red = red[:6] + innerRed[4:6]
                    green = green[:6] + innerRed[6:]
                    pixPart = 2
                elif pixPart == 2:
                    red = red[:6] + innerGreen[:2]
                    green = green[:6] + innerGreen[2:4]
                    pixPart = 3
                elif pixPart == 3:
                    red = red[:6] + innerGreen[4:6]
                    green = green[:6] + innerGreen[6:8]
                    pixPart = 4
                elif pixPart == 4:
                    red = red[:6] + innerBlue[:2]
                    green = green[:6] + innerBlue[2:4]
                    pixPart = 5
                elif pixPart == 5:
                    red = red[:6] + innerBlue[4:6]
                    green = green[:6] + innerBlue[6:]
                    pixPart = 0
                    pixelCount += 1
                    innerRow = (innerRow + 1) % innerHeight
                    if innerRow == 0:
                        innerCol = innerCol + 1

                outerPixelData[2][col, row] = (int(red, 2), int(green, 2), int(blue, 2))

                if pixelCount >= innerWidth * innerHeight:
                    outerImg.save(f"{settings.MEDIA_ROOT}/encoded.png")
                    return
    else:
        raise ValueError("Inner Image too Large for Outer Image")


def decodeImage2Bit():
    encodedImg = Image.open(f"{settings.MEDIA_ROOT}/encoded.png")
    pixelData = getPixelData(encodedImg)

    # get metadata pixels
    for row in range(3):
        # width metadata pixels
        widthPixel = encodedImg.getpixel((0, row))
        if row == 0:
            width = (
                format(widthPixel[0], "08b")[6:]
                + format(widthPixel[1], "08b")[6:]
                + format(widthPixel[2], "08b")[6:]
            )
        elif row == 1:
            width += (
                format(widthPixel[0], "08b")[6:]
                + format(widthPixel[1], "08b")[6:]
                + format(widthPixel[2], "08b")[6:]
            )
        elif row == 2:
            width += format(widthPixel[0], "08b")[6:] + format(widthPixel[1], "08b")[6:]
    for row in range(3, 6):
        # height metadata pixels
        heightPixel = encodedImg.getpixel((0, row))
        if row == 3:
            height = (
                format(heightPixel[0], "08b")[6:]
                + format(heightPixel[1], "08b")[6:]
                + format(heightPixel[2], "08b")[6:]
            )
        elif row == 4:
            height += (
                format(heightPixel[0], "08b")[6:]
                + format(heightPixel[1], "08b")[6:]
                + format(heightPixel[2], "08b")[6:]
            )
        elif row == 5:
            height += (
                format(heightPixel[0], "08b")[6:] + format(heightPixel[1], "08b")[6:]
            )
    width = int(width, 2)
    height = int(height, 2)

    remainingPixels = width * height

    # create new image
    hiddenImg = Image.new("RGB", (width, height))
    hiddenPixels = hiddenImg.load()

    pixPart = 0
    innerCol = 0
    innerRow = 0
    for col in range(pixelData[0]):
        for row in range(pixelData[1]):
            if col == 0 and row < 12:
                # metadata pixel, skip
                continue

            pixel = encodedImg.getpixel((col, row))
            if remainingPixels > 0:
                if pixPart == 0:
                    # red 1/2
                    red = format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                    pixPart = 1
                elif pixPart == 1:
                    # red 2/2
                    red += format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                    pixPart = 2
                elif pixPart == 2:
                    # green 1/2
                    green = format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                    pixPart = 3
                elif pixPart == 3:
                    # green 2/2
                    green += format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                    pixPart = 4
                elif pixPart == 4:
                    # blue 1/2
                    blue = format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                    pixPart = 5
                elif pixPart == 5:
                    # blue 2/2
                    blue += format(pixel[0], "08b")[6:] + format(pixel[1], "08b")[6:]
                    pixPart = 0
                    remainingPixels -= 1
                    hiddenPixels[innerCol, innerRow] = (
                        int(red, 2),
                        int(green, 2),
                        int(blue, 2),
                    )
                    innerRow = (innerRow + 1) % height
                    if innerRow == 0:
                        innerCol = innerCol + 1
            else:
                hiddenImg.save(f"{settings.MEDIA_ROOT}/decoded.png")
                return


def encodeImage4Bit():
    innerImg = Image.open(f"{settings.MEDIA_ROOT}/upload_inner.png")
    outerImg = Image.open(f"{settings.MEDIA_ROOT}/upload_outer.png")
    innerPixelData = getPixelData(innerImg)
    outerPixelData = getPixelData(outerImg)
    innerWidth = innerPixelData[0]
    innerHeight = innerPixelData[1]
    validImgSize = True
    # Each pixel of inner needs 3 pixels from outer to be encoded
    # 4 metadata pixels are used, 2 for # cols and 2 for # rows
    if (outerPixelData[0] * outerPixelData[1] * 3) - 4 < (innerWidth * innerHeight):
        validImgSize = False

    binaryCols = format(innerWidth, "016b")
    binaryRows = format(innerHeight, "016b")

    pixPart = 0
    pixelCount = 0
    innerCol = 0
    innerRow = 0
    if validImgSize:
        for col in range(outerPixelData[0]):
            for row in range(outerPixelData[1]):
                pixel = outerImg.getpixel((col, row))

                # RGB values
                red = format(pixel[0], "08b")
                green = format(pixel[1], "08b")
                blue = format(pixel[2], "08b")

                currentInnerPixel = innerImg.getpixel((innerCol, innerRow))
                innerRed = format(currentInnerPixel[0], "08b")
                innerGreen = format(currentInnerPixel[1], "08b")
                innerBlue = format(currentInnerPixel[2], "08b")
                if col == 0 and row <= 3:
                    if row == 0:
                        # metadata pixel 1
                        red = red[:4] + binaryCols[:4]
                        green = green[:4] + binaryCols[4:8]
                    elif row == 1:
                        # metadata pixel 2
                        red = red[:4] + binaryCols[8:12]
                        green = green[:4] + binaryCols[12:]
                    elif row == 2:
                        # metadata pixel 3
                        red = red[:4] + binaryRows[:4]
                        green = green[:4] + binaryRows[4:8]
                    elif row == 3:
                        # metadata pixel 4
                        red = red[:4] + binaryRows[8:12]
                        green = green[:4] + binaryRows[12:]
                elif pixPart == 0:
                    red = red[:4] + innerRed[:4]
                    green = green[:4] + innerRed[4:]
                    pixPart = 1
                elif pixPart == 1:
                    red = red[:4] + innerGreen[:4]
                    green = green[:4] + innerGreen[4:]
                    pixPart = 2
                elif pixPart == 2:
                    red = red[:4] + innerBlue[:4]
                    green = green[:4] + innerBlue[4:]
                    pixPart = 0
                    pixelCount += 1
                    innerRow = (innerRow + 1) % innerHeight
                    if innerRow == 0:
                        innerCol = innerCol + 1

                outerPixelData[2][col, row] = (int(red, 2), int(green, 2), int(blue, 2))

                if pixelCount >= innerWidth * innerHeight:
                    outerImg.save(f"{settings.MEDIA_ROOT}/encoded.png")
                    return
    else:
        raise ValueError("Inner Image too Large for Outer Image")


def decodeImage4Bit():
    encodedImg = Image.open(f"{settings.MEDIA_ROOT}/encoded.png")
    pixelData = getPixelData(encodedImg)

    # get metadata pixels
    for row in range(2):
        # width metadata pixels
        widthPixel = encodedImg.getpixel((0, row))
        if row == 0:
            width = format(widthPixel[0], "08b")[4:] + format(widthPixel[1], "08b")[4:]
        elif row == 1:
            width += format(widthPixel[0], "08b")[4:] + format(widthPixel[1], "08b")[4:]
    for row in range(2, 4):
        # height metadata pixels
        heightPixel = encodedImg.getpixel((0, row))
        if row == 2:
            height = (
                format(heightPixel[0], "08b")[4:] + format(heightPixel[1], "08b")[4:]
            )
        elif row == 3:
            height += (
                format(heightPixel[0], "08b")[4:] + format(heightPixel[1], "08b")[4:]
            )
    width = int(width, 2)
    height = int(height, 2)

    remainingPixels = width * height

    # create new image
    hiddenImg = Image.new("RGB", (width, height))
    hiddenPixels = hiddenImg.load()

    pixPart = 0
    innerCol = 0
    innerRow = 0
    for col in range(pixelData[0]):
        for row in range(pixelData[1]):
            if col == 0 and row < 4:
                # metadata pixel, skip
                continue

            pixel = encodedImg.getpixel((col, row))
            if remainingPixels > 0:
                if pixPart == 0:
                    # red
                    red = format(pixel[0], "08b")[4:] + format(pixel[1], "08b")[4:]
                    pixPart = 1
                elif pixPart == 1:
                    # green
                    green = format(pixel[0], "08b")[4:] + format(pixel[1], "08b")[4:]
                    pixPart = 2
                elif pixPart == 2:
                    # blue
                    blue = format(pixel[0], "08b")[4:] + format(pixel[1], "08b")[4:]
                    pixPart = 0
                    remainingPixels -= 1
                    hiddenPixels[innerCol, innerRow] = (
                        int(red, 2),
                        int(green, 2),
                        int(blue, 2),
                    )
                    innerRow = (innerRow + 1) % height
                    if innerRow == 0:
                        innerCol = innerCol + 1
            else:
                hiddenImg.save(f"{settings.MEDIA_ROOT}/decoded.png")
                return


def getPixelData(image):
    width, height = image.size
    pixels = image.load()
    pixelData = [width, height, pixels]
    return pixelData


def main():
    encodeImage4Bit()
    decodeImage4Bit()


if __name__ == "__main__":
    main()
