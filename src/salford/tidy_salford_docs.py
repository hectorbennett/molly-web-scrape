import os

ROOT = os.path.join(os.getcwd(), "manchester_docs")

def delete_old_files():
    for pathname in os.listdir(ROOT):
        path = os.path.join(ROOT, pathname)
        for thing in os.listdir(path):
            p = os.path.join(path, thing)
            if os.path.isfile(p):
                print('delete')
                os.remove(p)


def check_completeness():
    done_count = 0
    failed_count = 0
    for root, dirs, files in os.walk(ROOT):
        path = root.split(os.sep)
        # print((len(path) - 1) * '---', os.path.basename(root))/
        for file in files:
            if file.endswith('crdownload'):
                failed_count += 1
            else:
                done_count += 1
    print('failed: {}'.format(failed_count))
    print('done: {}'.format(done_count))

if __name__ == '__main__':
    check_completeness()


