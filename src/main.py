import sys

from fileutils import prepare_target_folder, sync_content

def main():
    args = sys.argv[1:]
    if len(args) == 0: basepath = '/'
    else: basepath = args[0]

    prepare_target_folder()
    sync_content(basepath)

if __name__ == "__main__":
    main()