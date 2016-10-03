""" apt-repo suites {<uri> | <ppa>} """

import argparse
from   .common import get_archive

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    for suite in get_archive(args).scrape_suite_names():
         print(suite)

if __name__ == '__main__':
    main()
