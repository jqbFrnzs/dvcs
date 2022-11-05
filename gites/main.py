from init import git_init
import sys
import zlib

def main():
    command1 = sys.argv[1]
    command2 = sys.argv[2]
    blob_hash = sys.argv[3]
    if command1 == 'init':
        git_init()
    elif command1 =='cat-file':
        print('s')
        if command2 =='-p':
            print('h')
            subfolder = blob_hash[:2]
            blob_name = blob_hash[2:]
            print(blob_hash)
            print(blob_name)
            print(subfolder)
            path_to_read = ".git\\objects\\" + subfolder + "\\" + blob_name
            print(path_to_read)
            compressed = zlib.compress('Hello There')
            print(type(compressed))
            with open(path_to_read, "wb") as f:
                f.write(compressed)
                # print(f.read())
            # with open(path_to_read, "rb") as f:
            #     print('d')
            #     decompressed = zlib.decompress(f.read())
            #     # print(f.read())
    else:
        print('Wrong argument: ' + command1)
        raise RuntimeError


if __name__ == "__main__":
    main()