import os

if __name__ == "__main__":
    key = [162, 101, 186, 26, 45, 198, 127, 147, 70, 21, 132]

    encryptedFiles = ["png", "txt"]

    archiveName = input("Which .pac file to unpack?\n")
    folderName = archiveName[0:-4]

    try:
        os.mkdir(os.path.join(os.getcwd(), folderName))
    except FileExistsError:
        pass

    with open(archiveName, "rb") as f:
        fileHeader = f.read(4)
        if fileHeader != b'MGPK':
            raise TypeError("Invalid Filetype.")
        archiveVersion = int.from_bytes(f.read(4), "little")
        if archiveVersion != 1:
            raise TypeError("Invalid Archive Version.")
        numOfFiles = int.from_bytes(f.read(4), "little")

        for i in range(numOfFiles):
            print(f"Progress: {i}/{numOfFiles}", end="\r")

            f.seek(12 + 48 * i, 0)
            name = f.read(int.from_bytes(f.read(1), "little")).decode()

            f.seek(12 + 48 * i + 32, 0)
            offset = int.from_bytes(f.read(4), "little")
            size = int.from_bytes(f.read(4), "little")

            f.seek(offset)
            content = bytearray(f.read(size))

            fileEnding = name[-3:len(name)]
            if fileEnding in encryptedFiles:
                array = key[:]
                for j in range(len(content)):
                    content[j] = content[j] ^ array[j % len(key)]
                    array[j % len(array)] = (array[j % len(array)] + 27) % 256

            with open(f"{folderName}/{name}", "wb") as of:
                of.write(content)