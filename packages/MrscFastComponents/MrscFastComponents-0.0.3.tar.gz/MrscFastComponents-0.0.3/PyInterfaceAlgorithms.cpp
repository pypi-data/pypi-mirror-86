#include "PyInterfaceAlgorithms.h"

void bindAlgorithms(py::module& m) {

    py::class_<PathInfo>(m, "PathInfo", R"delimiter(

        A class with two attributes: path, cost. 
        This class is used to return the result of path planning algorithms.

        :var path: A list of edges. 
        :type path: List[Edge]
        :var cost: The total cost of the path.
        :type cost: double 

    )delimiter")
        .def(py::init<>())
        .def_readonly("path", &PathInfo::path)
        .def_readonly("cost", &PathInfo::cost);

    m.def("get_path_gbrs", py::overload_cast<Workspace&, Vector2d&, Vertex&, set<Vertex>&,
        unordered_map<Edge, double, Edge::HashFunction>&, double>(&get_path_gbrs), py::return_value_policy::move,
        R"delimiter(

            This function returns the shortest cost path, which also considers the rotation penalty.
            
            :param workspace: An abstract Graph-based layout.
            :type workspace: Workspace
            :param init_direction: Initial heading direction of a robot.
            :type init_direction: Vector2d
            :param vs: Initiate vertex.
            :type vs: Vertex
            :param ends: A set of available goal vertices or edges.
            :type ends: Set[Vertex, Edge]
            :param cost: Cost function for each edges.
            :type cost: Dict[Edge]
            :param rotation_penalty: Rotation penalty.
            :type rotation_penalty: float
            :rtype: PathInfo

            :Example:
            
            >>> from mrscfastcom.workspace import *
            >>> from mrscfastcom.algorithms import *

            >>> w = Workspace(75, 75, 0.6)
            >>> init_direction = Vector2d(0, 1)
            >>> vs = w[0, 0]
            >>> ends = {Edge(w[11, 12], w[12, 12])}
            >>> cost = {e: 1 for e in w.graph.edges}
            >>> p = get_path_gbrs(w, init_direction, vs, ends, cost, 1)

            >>> p.cost
            25.5707963267949
            
            >>> (w[p.path[0].endPointX], w[p.path[0].endPointY])
            (<Vector2d: 0.000000, 0.000000>, <Vector2d: 0.000000, 1.000000>)

            >>> (w[p.path[-1].endPointX], w[p.path[-1].endPointY])
            (<Vector2d: 11.000000, 12.000000>, <Vector2d: 12.000000, 12.000000>)

            >>> len(p.path)
            24

        )delimiter", "workspace"_a, "init_direction"_a, "vs"_a, "ends"_a, "cost"_a, "rotation_penalty"_a);

    m.def("get_path_gbrs", py::overload_cast<Workspace&, Vector2d&, Vertex&, set<Edge>&,
        unordered_map<Edge, double, Edge::HashFunction>&, double>(&get_path_gbrs), py::return_value_policy::move,
        "workspace"_a, "init_direction"_a, "vs"_a, "ends"_a, "cost"_a, "rotation_penalty"_a);
}