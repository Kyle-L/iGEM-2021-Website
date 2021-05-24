import build
import wikisync

if __name__ == '__main__':
    answer = input("Are you sure you want to build and sync the wiki (Y/N): ").lower() 
    if answer == "yes" or answer == "y": 
        build.build()
        wikisync.sync()