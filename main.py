import build
import wikisync

if __name__ == '__main__':
    build.build('temp\\build', 'site')
    wikisync.sync('temp\\build', 'temp\\sync', 'MiamiU_OH')
