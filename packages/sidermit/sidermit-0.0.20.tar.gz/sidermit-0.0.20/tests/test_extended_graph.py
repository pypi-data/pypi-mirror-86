import unittest
from collections import defaultdict

from sidermit.city import graph
from sidermit.optimization.preoptimization import ExtendedGraph, ExtendedEdgesType
from sidermit.publictransportsystem import *


class test_extended_graph(unittest.TestCase):

    def test_build_tree_graph(self):
        """
        test methods get_tree_graph
        :return:
        """
        graph_obj = graph.Graph.build_from_parameters(n=5, l=1000, g=0.5, p=2)
        network = TransportNetwork(graph_obj)

        mode_manager = TransportModeManager()
        bus_obj = mode_manager.get_mode("bus")
        metro_obj = mode_manager.get_mode("metro")
        # train_obj = TransportMode("train", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

        feeder_routes = network.get_feeder_routes(bus_obj)
        radial_routes = network.get_radial_routes(metro_obj)
        circular_routes = network.get_circular_routes(bus_obj)

        for route in feeder_routes:
            network.add_route(route)

        for route in radial_routes:
            network.add_route(route)

        for route in circular_routes:
            network.add_route(route)

        city_nodes = ExtendedGraph.build_city_nodes(graph_obj)
        tree_graph = ExtendedGraph.build_tree_graph(network.get_routes(), city_nodes)

        one_stop = []
        two_stop = []
        three_stop = []

        four_route_city = 0
        six_route_city = 0
        ten_route_city = 0

        one_route_stop = 0
        two_route_stop = 0
        ten_route_stop = 0

        for city_node in tree_graph:
            if len(tree_graph[city_node]) == 1:
                one_stop.append(city_node)
            if len(tree_graph[city_node]) == 2:
                two_stop.append(city_node)
            if len(tree_graph[city_node]) == 3:
                three_stop.append(city_node)

            n_routes_city = 0
            for stop in tree_graph[city_node]:
                n_routes_stop = 0
                for _ in tree_graph[city_node][stop]:
                    n_routes_stop = n_routes_stop + 1
                    n_routes_city = n_routes_city + 1

                if n_routes_stop == 1:
                    one_route_stop = one_route_stop + 1
                if n_routes_stop == 2:
                    two_route_stop = two_route_stop + 1
                if n_routes_stop == 10:
                    ten_route_stop = ten_route_stop + 1

            if n_routes_city == 4:
                four_route_city = four_route_city + 1
            if n_routes_city == 6:
                six_route_city = six_route_city + 1
            if n_routes_city == 10:
                ten_route_city = ten_route_city + 1

        self.assertEqual(len(one_stop), 1)
        self.assertEqual(len(two_stop), 10)
        self.assertEqual(len(three_stop), 0)

        self.assertEqual(four_route_city, 5)
        self.assertEqual(six_route_city, 5)
        self.assertEqual(ten_route_city, 1)

        self.assertEqual(one_route_stop, 0)
        self.assertEqual(two_route_stop, 15)
        self.assertEqual(ten_route_stop, 1)

    def test_build_nodes(self):

        graph_obj = graph.Graph.build_from_parameters(n=5, l=1000, g=0.5, p=2)
        network = TransportNetwork(graph_obj)

        mode_manager = TransportModeManager()
        bus_obj = mode_manager.get_mode("bus")
        metro_obj = mode_manager.get_mode("metro")
        # train_obj = TransportMode("train", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

        feeder_routes = network.get_feeder_routes(bus_obj)
        radial_routes = network.get_radial_routes(metro_obj)
        circular_routes = network.get_circular_routes(bus_obj)

        for route in feeder_routes:
            network.add_route(route)

        for route in radial_routes:
            network.add_route(route)

        for route in circular_routes:
            network.add_route(route)

        city_nodes = ExtendedGraph.build_city_nodes(graph_obj)
        tree_graph = ExtendedGraph.build_tree_graph(network.get_routes(), city_nodes)
        stop_nodes = ExtendedGraph.build_stop_nodes(tree_graph)
        route_nodes = ExtendedGraph.build_route_nodes(network.get_routes(), stop_nodes)

        self.assertEqual(len(city_nodes), 11)
        self.assertEqual(len(stop_nodes), 21)
        self.assertEqual(len(route_nodes), 60)

    def test_extended_graph_nodes(self):

        graph_obj = graph.Graph.build_from_parameters(n=5, l=1000, g=0.5, p=2)
        network = TransportNetwork(graph_obj)

        passenger_obj = Passenger(2, 2, 2, 2, 2, 2, 2, 2, 2)

        mode_manager = TransportModeManager()
        bus_obj = mode_manager.get_mode("bus")
        metro_obj = mode_manager.get_mode("metro")
        # train_obj = TransportMode("train", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

        feeder_routes = network.get_feeder_routes(bus_obj)
        radial_routes = network.get_radial_routes(metro_obj)
        circular_routes = network.get_circular_routes(bus_obj)

        for route in feeder_routes:
            network.add_route(route)

        for route in radial_routes:
            network.add_route(route)

        for route in circular_routes:
            network.add_route(route)

        extended_graph = ExtendedGraph(graph_obj, network.get_routes(), passenger_obj.spt)
        extended_graph_nodes = extended_graph.get_extended_graph_nodes()

        n_city = 0
        n_stop = 0
        n_route = 0
        for city_node in extended_graph_nodes:
            n_city = n_city + 1
            for stop_node in extended_graph_nodes[city_node]:
                n_stop = n_stop + 1
                for _ in extended_graph_nodes[city_node][stop_node]:
                    n_route = n_route + 1

        self.assertEqual(n_city, 11)
        self.assertEqual(n_stop, 21)
        self.assertEqual(n_route, 60)

    def test_build_edges(self):

        graph_obj = graph.Graph.build_from_parameters(n=5, l=1000, g=0.5, p=2)
        network = TransportNetwork(graph_obj)

        passenger_obj = Passenger(4, 2, 2, 2, 2, 2, 2, 2, 2)

        mode_manager = TransportModeManager()
        bus_obj = mode_manager.get_mode("bus")
        metro_obj = mode_manager.get_mode("metro")
        # train_obj = TransportMode("train", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

        feeder_routes = network.get_feeder_routes(bus_obj)
        radial_routes = network.get_radial_routes(metro_obj)
        circular_routes = network.get_circular_routes(bus_obj)

        for route in feeder_routes:
            network.add_route(route)

        for route in radial_routes:
            network.add_route(route)

        for route in circular_routes:
            network.add_route(route)

        city_nodes = ExtendedGraph.build_city_nodes(graph_obj)
        tree_graph = ExtendedGraph.build_tree_graph(network.get_routes(), city_nodes)
        stop_nodes = ExtendedGraph.build_stop_nodes(tree_graph)
        route_nodes = ExtendedGraph.build_route_nodes(network.get_routes(), stop_nodes)

        extended_graph_nodes = ExtendedGraph.build_extended_graph_nodes(route_nodes)

        initial_frequency = defaultdict(float)

        for route in network.get_routes():
            initial_frequency[route.id] = 28

        access_edges = ExtendedGraph.build_access_edges(extended_graph_nodes)
        boarding_edges = ExtendedGraph.build_boarding_edges(extended_graph_nodes, initial_frequency)
        alighting_edges = ExtendedGraph.build_alighting_edges(extended_graph_nodes, passenger_obj.spt)
        route_edges = ExtendedGraph.build_route_edges(extended_graph_nodes)

        self.assertEqual(len(access_edges), 42)
        self.assertEqual(len(boarding_edges), 40)
        self.assertEqual(len(alighting_edges), 40)
        self.assertEqual(len(route_edges), 40)

    def test_get_extended_edges(self):

        graph_obj = graph.Graph.build_from_parameters(n=5, l=1000, g=0.5, p=2)
        network = TransportNetwork(graph_obj)

        passenger_obj = Passenger(4, 2, 2, 2, 2, 2, 2, 2, 2)

        mode_manager = TransportModeManager()
        bus_obj = mode_manager.get_mode("bus")
        metro_obj = mode_manager.get_mode("metro")
        # train_obj = TransportMode("train", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

        feeder_routes = network.get_feeder_routes(bus_obj)
        radial_routes = network.get_radial_routes(metro_obj, express=True)
        circular_routes = network.get_circular_routes(bus_obj)

        for route in feeder_routes:
            network.add_route(route)

        for route in radial_routes:
            network.add_route(route)

        for route in circular_routes:
            network.add_route(route)

        extended_graph = ExtendedGraph(graph_obj, network.get_routes(), passenger_obj.spt)
        extended_graph_edges = extended_graph.get_extended_graph_edges()

        n_access = 0
        n_boarding = 0
        n_alighting = 0
        n_route = 0

        for edge in extended_graph_edges:
            if edge.type == ExtendedEdgesType.ACCESS:
                n_access = n_access + 1
            if edge.type == ExtendedEdgesType.BOARDING:
                n_boarding = n_boarding + 1
            if edge.type == ExtendedEdgesType.ALIGHTING:
                n_alighting = n_alighting + 1
            if edge.type == ExtendedEdgesType.ROUTE:
                n_route = n_route + 1

        self.assertEqual(n_access, 32)
        self.assertEqual(n_boarding, 30)
        self.assertEqual(n_alighting, 30)
        self.assertEqual(n_route, 30)
