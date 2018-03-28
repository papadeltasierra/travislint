"""
Utility to lint travis-ci.org .travis.yml files by requesting linting from
the travis-ci-org website.

This avoids having to install lots and lots of Ruby and other stuff just to
lint the file.
"""
from __future__ import print_function
import argparse
import json
import yaml
import requests

# Requests (urllib3) generates a lot of warnings which we don't care about so
# disable them.  Note also that the import structure that gets to urllib3
# confuses pylint so we have to disable the watning.
requests.packages.urllib3.disable_warnings()    # pylint: disable=no-member

URI_LINTER = 'https://api.travis-ci.org/lint'
LINT = 'lint'
KEY='key'
MESSAGE = 'message'


def argparser():
    """
    Build an arguments parser.

    :returns: An arguments parser.
    :rtype: Parser
    """
    parser = argparse.ArgumentParser(
        description="Lint a .travis.yml file")
    parser.add_argument(
        "-v", "--verbose", action="store_const", const=True, default=False,
        help="verbose output of progress")
    parser.add_argument(
        "filename", action="store", nargs="?", default=".travis.yml",
        help="name of the file to lint (default: .travis.yml)")

    return parser


def main():
    """
    Mainline script which does the following.
    - Parses arguments
    - Reads the .travis.yml file assuming YAML
    - Passes the file contents to travis-ci.org linter
    - Displays the results.
    """

    # Parse command line arguments.
    parser = argparser()
    args = parser.parse_args()

    try:
        with open(args.filename, 'r') as yaml_file:
            try:
                if args.verbose:
                    print("Request...")
                    print("----------")
                    print("Parsing %s..." % args.filename)

                # Parse the file as generic YAML.
                body = yaml.load(yaml_file)

                if args.verbose:
                    print("POSTing to the linter...")

                # Pass the YAML to the travis-ci.org linter.
                json_result = requests.post(
                    URI_LINTER, data={'content': yaml.dump(body)})

                # The results are returned as JSON.
                result = json.loads(json_result.text)

                if args.verbose:
                    print("")
                    print("Response...")
                    print("-----------")

                if not result[LINT]:
                    raise Exception('No lint result returned')

                for msg_type in result[LINT]:
                    for report in result[LINT][msg_type]:
                        print("[X] ", end='')
                        if report[KEY]:
                            print('in %s section: ' % '.'.join(report[KEY]), end='')

                        print("%s" % str(report[MESSAGE]))

            except yaml.YAMLError as exc:
                print("Generic YAML parse failed: %s" % str(exc))

    except Exception as exc:        # pylint: disable=broad-except
        print("Error opening file: %s: %s" % (args.filename, str(exc)))


if __name__ == '__main__':
    main()
