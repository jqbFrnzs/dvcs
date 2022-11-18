import sys
import os
import zlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    #print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[1]
    try:
        command1 = sys.argv[2]
    except:
        pass
    try:
        command2 = sys.argv[3]
    except:
        pass
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
     #   print("Initialized git directory")
    elif command == "cat-file":
        if command1 == "-p":
            sha1_of_blob = command2
            sub_dir = sha1_of_blob[0:2]
            blob_name = sha1_of_blob[2:]
            blob_path = ".git/objects/" + sub_dir +"/"+ blob_name
            decompressed_content = ""
            with open(blob_path, "rb") as f:
                decomp_w_header = zlib.decompress(f.read())
                content_str_w_header = decomp_w_header.decode("utf-8")
                decomp = content_str_w_header.split('\x00')[1]
            print(decomp, end="")
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
