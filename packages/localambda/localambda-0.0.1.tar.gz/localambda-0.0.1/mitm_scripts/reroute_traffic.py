"""
This file routes traffic from a man in the middle either to AWS servers or to
the locally deployed service based off on pre-defined configuration rules.

These
"""
import json
import time


from mitmproxy import http
import redis
import yaml


from localambda.decorators import threadify
from localambda import LOLA_REDIS_LIST_NAME

# The Butler always checks if Redis is available before this script runs
r = redis.Redis('127.0.0.1')


class MatchedFlow(object):
    def __init__(self, from_route, to_route):
        self.from_route = from_route
        self.to_route = to_route

    def matches(self, route_url: str) -> bool:
        """Checks to see if a given URL is matched for the from route provided for this MatchedFlow

        :param route_url: A string representing the full URL of the request
        :return: Boolean, True if the MatchFlow route matches, otherwise False
        """

        if self.from_route in route_url:
            return True
        return False

    def replace_url_for_env(self, flow: http.HTTPFlow) -> None:
        """Safely replaces a flow object's URL and removes the environment specific key from
        the lambda to enable safely routing to localhost

        :param flow: A flow object that contains the URL
        :return: None
        """
        env_url = flow.request.url.replace(self.from_route, '')
        replacement_route = self.to_route + env_url[env_url.index('/'):]
        flow.request.url = replacement_route


class FlowMatcher(object):
    """Matches specific flows (URLs) that are being sent to AWS and routes them to internally
    running services
    """
    def __init__(self):
        self.route_confs = None
        self.match_flows = []
        self.load_route_configs()

    @threadify
    def load_route_configs(self) -> None:
        """Continuously polls redis to check if there are more route configurations that
        should be loaded to map traffic intended for AWS traffic to localhost.
        """
        while True:
            self.get_all_routes()
            time.sleep(1)

    def get_all_routes(self) -> None:
        """Reads the routes provided to Redis and creates MatchedFlows for each"""
        has_next = True
        while has_next:
            route_flow_bytes = r.lpop(LOLA_REDIS_LIST_NAME)
            if route_flow_bytes:
                route_flow_json = json.loads(route_flow_bytes)
                for route in route_flow_json:
                    mf = MatchedFlow(
                        from_route=route['from_route'],
                        to_route=route['to_route']
                    )
                    self.match_flows.append(mf)
            else:
                has_next = False

    def match_update_url(self, flow: http.HTTPFlow) -> None:
        """Matches a request against the set of configuraitons provided to see if the request
        should be rerouted.

        :param flow: A mitmproxy http flow object containing the full request details
        :return: None
        """
        for match_flow in self.match_flows:
            if match_flow.matches(flow.request.pretty_url):
                match_flow.replace_url_for_env(flow)
                break


FM = FlowMatcher()


def request(flow: http.HTTPFlow) -> None:
    FM.match_update_url(flow)
