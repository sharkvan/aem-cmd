# coding: utf-8
import sys
import optparse

import requests

from acmd.tool import tool
from tool_utils import get_command

parser = optparse.OptionParser("acmd dispatcher [options] [clear]")
parser.add_option("-v", "--verbose",
                  action="store_const", const=True, dest="verbose",
                  help="report verbose data when supported")


@tool('dispatcher')
class DispatcherTool(object):
    def execute(self, server, argv):
        (options, args) = parser.parse_args(argv)
        action = get_command(args, 'clear')
        if action == 'clear':
            clear_cache(server, options)
        else:
            sys.stderr.write('error: Unknown {t} action {a}\n'.format(t=self.name, a=action))
            sys.exit(-1)


def clear_cache(server, options):
    headers = {
        'Host': server.host,
        'CQ-Action': 'DELETE',
        'CQ-Handle': '/',
        'CQ-Path': '/'
    }

    # Clear on port 80
    url = 'http://{host}{path}'.format(host=server.host, path='/dispatcher/invalidate.cache')

    response = requests.get(
        url,
        auth=(server.username, server.password),
        headers=headers)
    if response.status_code == 200:
        if "<H1>OK</H1>" not in response.content:
            sys.stderr.write("error: Failed to validate response {}".format(response.content))
    else:
        sys.stderr.write("error: " + str(response.status_code) + "\n")
    if options.verbose:
        sys.stderr.write(response.content + "\n")
