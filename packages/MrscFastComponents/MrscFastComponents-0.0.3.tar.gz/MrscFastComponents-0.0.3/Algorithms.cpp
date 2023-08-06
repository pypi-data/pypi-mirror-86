#include "Algorithms.h"
#include <queue>
#include <unordered_map>

typedef int VertexId;

PathInfo extract_path(const PathNodeNaive& path_node)
{
	auto path_node_ptr = &path_node;
	PathInfo pinfo;
	pinfo.cost = path_node.total_cost;

	while (path_node_ptr->prev_node->prev_node != nullptr) {
		pinfo.path.push_back(Edge(path_node_ptr->edge));
		path_node_ptr = path_node_ptr->prev_node;
	}

	reverse(pinfo.path.begin(), pinfo.path.end());
	return pinfo;
}

bool PathNodeNaive::operator<(const PathNodeNaive& p)
{

	return this->total_cost < p.total_cost;
}

bool CmpPathNodeNaivePtr::operator()(const PathNodeNaive* lhs, const PathNodeNaive* rhs) const
{
	return lhs->total_cost > rhs->total_cost;
}

vector<PathNodeNaive> PathNodes(5625 * 4);
int path_node_pointer = 0;

void inline reset_node(PathNodeNaive* n, const Vertex& v, PathNodeNaive* prev_node, double&& total_cost) {
	n->prev_node = prev_node;
	n->total_cost = std::move(total_cost);
	n->edge.endPointY = v;

	if (prev_node != nullptr) {
		n->edge.endPointX = prev_node->edge.endPointY;
	}
}

struct VertexPtrHash
{
	std::size_t operator()(const Vertex* k) const {
		return k->id;
	};
};


// Termination Criteria: Vertex
PathInfo get_path_gbrs(
	Workspace& z, Vector2d& direction, Vertex& vs, set<Vertex>& vends,
	unordered_map<Edge, double, Edge::HashFunction>& w, double penalty_factor)

{
	Vertex v_root;
	priority_queue<PathNodeNaive*, vector<PathNodeNaive*>, CmpPathNodeNaivePtr> Open;

	if (z.graph.edges.size() > PathNodes.size()) {
		PathNodes.resize(z.graph.edges.size());
	}

	path_node_pointer = 0;

	z.set_mapping(v_root, z[vs] - direction);
	auto root_node = &(PathNodes[path_node_pointer++]);
	reset_node(root_node, v_root, nullptr, 0);
	auto first_node = &(PathNodes[path_node_pointer++]);
	reset_node(first_node, vs, root_node, 0);

	Open.push(first_node);

	PathNodeNaive* n;
	PathNodeNaive* n_next;
	const Edge* e_next;

	unordered_set<const Edge*> edge_used(z.graph.edges.size());
	unordered_map<int, double> best_cost(z.graph.edges.size());

	double penalty;
	set<Edge>* succ;
	std::set<Edge>::iterator it;

	while (!Open.empty()) {

		n = Open.top();
		Open.pop();

		if (vends.find(n->edge.endPointY) != vends.end()) {
			return extract_path(*n);
		}

		succ = &(z.graph.left_vertex_incident_edges.find(n->edge.endPointY)->second);
		for (it = succ->begin(); it != succ->end(); it++) {

			e_next = &(*it);

			if (edge_used.find(e_next) != edge_used.end()) continue;
			else edge_used.insert(e_next);

			penalty = penalty_factor *
				GetAngleDf(z.z.find(n->edge.endPointY)->second - z.z.find(n->edge.endPointX)->second,
					z.z.find(e_next->endPointY)->second - z.z.find(e_next->endPointX)->second);

			n_next = &(PathNodes[path_node_pointer++]);
			reset_node(n_next, (*it).endPointY, n, penalty + n->total_cost + w.find(*e_next)->second);
			Open.push(n_next);
		}
	}
	return PathInfo();
}


// Termination Criteria: Edge 
PathInfo get_path_gbrs(
	Workspace& z, Vector2d& direction, Vertex& vs, set<Edge>& vends,
	unordered_map<Edge, double, Edge::HashFunction>& w, double penalty_factor)

{
	Vertex v_root;
	priority_queue<PathNodeNaive*, vector<PathNodeNaive*>, CmpPathNodeNaivePtr> Open;

	if (z.graph.edges.size() > PathNodes.size()) {
		PathNodes.resize(z.graph.edges.size());
	}

	path_node_pointer = 0;

	z.set_mapping(v_root, z[vs] - direction);
	auto root_node = &(PathNodes[path_node_pointer++]);
	reset_node(root_node, v_root, nullptr, 0);
	auto first_node = &(PathNodes[path_node_pointer++]);
	reset_node(first_node, vs, root_node, 0);

	Open.push(first_node);

	PathNodeNaive* n;
	PathNodeNaive* n_next;
	const Edge* e_next;

	unordered_set<const Edge*> edge_used(z.graph.edges.size());
	unordered_map<int, double> best_cost(z.graph.edges.size());

	double penalty;
	set<Edge>* succ;
	std::set<Edge>::iterator it;

	while (!Open.empty()) {

		n = Open.top();
		Open.pop();

		if (vends.find(n->edge) != vends.end()) {
			return extract_path(*n);
		}

		succ = &(z.graph.left_vertex_incident_edges.find(n->edge.endPointY)->second);
		for (it = succ->begin(); it != succ->end(); it++) {

			e_next = &(*it);

			if (edge_used.find(e_next) != edge_used.end()) continue;
			else edge_used.insert(e_next);

			penalty = penalty_factor *
				GetAngleDf(z.z.find(n->edge.endPointY)->second - z.z.find(n->edge.endPointX)->second,
					z.z.find(e_next->endPointY)->second - z.z.find(e_next->endPointX)->second);

			n_next = &(PathNodes[path_node_pointer++]);
			reset_node(n_next, (*it).endPointY, n, penalty + n->total_cost + w.find(*e_next)->second);
			Open.push(n_next);
		}
	}
	return PathInfo();
}