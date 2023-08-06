import requests
import json
import logging

log = logging.getLogger(__name__)


def request(url, hostcert=None, hostkey=None, verify=False):
    log.debug('Retrieving {}'.format(url))
    if hostcert and hostkey:
        req = requests.get(url, verify=verify, timeout=120, cert=(hostcert, hostkey))
    else:
        req = requests.get(url, timeout=120, verify=verify)
    req.raise_for_status()
    return req.content


class PSCException(Exception):
    pass


class PSC(object):
    def __init__(self, url, hostcert=None, hostkey=None, verify=False):
        self.config = list()
        req = request(url, hostcert=hostcert, hostkey=hostkey, verify=verify)
        config_st = json.loads(req)
        # auto-url, mesh-config or list of mesh-configs
        if isinstance(config_st, dict):
            # mesh config or auto-url
            self.config = [config_st, ]
        else:
            # list of mesh configs
            for e in config_st:
                mesh_url = e['include'][0]
                mesh_r = request(mesh_url, hostcert=hostcert, hostkey=hostkey, verify=verify)
                mesh_config = json.loads(mesh_r)
                self.config.append(mesh_config)

    def get_all_hosts(self):
        hosts = set()
        for mc in self.config:
            for h in mc['hosts'].keys():
                hosts.add(h)
        return hosts

    def _group_hosts(self):
        groups_hosts = dict()
        for mc in self.config:
            for k, v in mc['groups'].items():
                if 'addresses' in v.keys():
                    hosts = [h['name'] for h in v['addresses']]
                elif 'a-addresses' in v.keys():
                    hosts = [h['name'] for h in v['a-addresses']]
                elif 'b-addresses' in v.keys():
                    hosts = [h['name'] for h in v['b-addresses']]
                else:
                    raise PSCException('Unexpected key in groups ({})'.format(v))
                groups_hosts[k] = hosts
        return groups_hosts

    def get_hosts_by_group(self, *groups, exclude=None):
        if isinstance(exclude, str):
            exclude = [exclude, ]

        groups_hosts = self._group_hosts()
        hosts_set = set()
        for group, hosts in groups_hosts.items():
            if exclude and any(ex in group for ex in exclude):
                continue
            if groups and any(g not in group for g in groups):
                continue
            for h in hosts:
                hosts_set.add(h)
        return hosts_set

    def get_test_types(self, host):
        groups_hosts = self._group_hosts()
        groups_tests = dict()
        for mc in self.config:
            if 'tests' not in mc.keys():
                raise PSCException('Failed to find tests ({})'.format(mc.keys()))
            for k, v in mc['tests'].items():
                groups_tests[k] = v['type']

        types_per_host = set()
        for g, h in groups_hosts.items():
            if host in h:
                for g2, t in groups_tests.items():
                    if g2 == g:
                        types_per_host.add(t)
        return types_per_host

    def get_site(self, host):
        host_site = dict()
        for mc in self.config:
            if 'addresses' not in mc.keys():
                raise PSCException('Failed to find addresses ({})'.format(mc.keys()))
            for k, v in mc['addresses'].items():
                host_site[k] = v['_meta']['display-name']

        if host in host_site.keys():
            return host_site[host]
