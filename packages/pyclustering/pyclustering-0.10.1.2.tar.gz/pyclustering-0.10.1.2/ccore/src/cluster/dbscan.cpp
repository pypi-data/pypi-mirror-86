/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/cluster/dbscan.hpp>

#include <string>
#include <unordered_set>

#include <pyclustering/container/kdtree_searcher.hpp>


namespace pyclustering {

namespace clst {


dbscan::dbscan(const double p_radius_connectivity, const size_t p_minimum_neighbors) :
        m_data_ptr(nullptr),
        m_result_ptr(nullptr),
        m_visited(std::vector<bool>()),
        m_belong(std::vector<bool>()),
        m_initial_radius(p_radius_connectivity),
        m_neighbors(p_minimum_neighbors)
{ }


void dbscan::process(const dataset & p_data, dbscan_data & p_result) {
    process(p_data, dbscan_data_t::POINTS, p_result);
}


void dbscan::process(const dataset & p_data, const dbscan_data_t p_type, dbscan_data & p_result) {
    m_data_ptr  = &p_data;
    m_type      = p_type;

    if (m_type == dbscan_data_t::POINTS) {
        create_kdtree(*m_data_ptr);
    }

    m_visited = std::vector<bool>(m_data_ptr->size(), false);
    m_belong = m_visited;

    m_result_ptr = &p_result;

    for (size_t i = 0; i < m_data_ptr->size(); i++) {
        if (m_visited[i]) {
            continue;
        }

        m_visited[i] = true;

        /* expand cluster */
        cluster allocated_cluster;
        expand_cluster(i, allocated_cluster);

        if (!allocated_cluster.empty()) {
            m_result_ptr->clusters().emplace_back(std::move(allocated_cluster));
        }
    }

    for (size_t i = 0; i < m_data_ptr->size(); i++) {
        if (!m_belong[i]) {
            m_result_ptr->noise().emplace_back(i);
        }
    }

    m_data_ptr = nullptr;
    m_result_ptr = nullptr;
}


void dbscan::expand_cluster(const std::size_t p_index, cluster & allocated_cluster) {
    std::vector<size_t> index_matrix_neighbors;
    get_neighbors(p_index, index_matrix_neighbors);

    if (index_matrix_neighbors.size() >= m_neighbors) {
        allocated_cluster.push_back(p_index);
        m_belong[p_index] = true;

        for (std::size_t k = 0; k < index_matrix_neighbors.size(); k++) {
            std::size_t index_neighbor = index_matrix_neighbors[k];

            if (!m_visited[index_neighbor]) {
                m_visited[index_neighbor] = true;

                /* check for neighbors of the current neighbor - maybe it's noise */
                std::vector<size_t> neighbor_neighbor_indexes;
                get_neighbors(index_neighbor, neighbor_neighbor_indexes);
                if (neighbor_neighbor_indexes.size() >= m_neighbors) {

                    /* Add neighbors of the neighbor for checking */
                    for (auto neighbor_index : neighbor_neighbor_indexes) {
                        /* Check if some of neighbors already in check list */
                        std::vector<std::size_t>::const_iterator position = std::find(index_matrix_neighbors.begin(), index_matrix_neighbors.end(), neighbor_index);
                        if (position == index_matrix_neighbors.end()) {
                            /* Add neighbor if it does not exist in the list */
                            index_matrix_neighbors.push_back(neighbor_index);
                        }
                    }
                }
            }

            if (!m_belong[index_neighbor]) {
                allocated_cluster.push_back(index_neighbor);
                m_belong[index_neighbor] = true;
            }
        }

        index_matrix_neighbors.clear();
    }
}


void dbscan::get_neighbors(const size_t p_index, std::vector<size_t> & p_neighbors) {
    switch(m_type) {
    case dbscan_data_t::POINTS:
        get_neighbors_from_points(p_index, p_neighbors);
        break;

    case dbscan_data_t::DISTANCE_MATRIX:
        get_neighbors_from_distance_matrix(p_index, p_neighbors);
        break;

    default:
        throw std::invalid_argument("Incorrect input data type is specified '" + std::to_string((unsigned) m_type) + "'");
    }
}


void dbscan::get_neighbors_from_points(const size_t p_index, std::vector<size_t> & p_neighbors) {
    container::kdtree_searcher searcher((*m_data_ptr)[p_index], m_kdtree.get_root(), m_initial_radius);
    searcher.find_nearest([&p_index, &p_neighbors](const container::kdnode::ptr & node, const double distance) {
            if (p_index != (std::size_t) node->get_payload()) {
                p_neighbors.push_back((std::size_t) node->get_payload());
            }
        });
}


void dbscan::get_neighbors_from_distance_matrix(const size_t p_index, std::vector<size_t> & p_neighbors) {
    const auto & distances = m_data_ptr->at(p_index);
    for (std::size_t index_neighbor = 0; index_neighbor < distances.size(); index_neighbor++) {
        const double candidate_distance = distances[index_neighbor];
        if ( (candidate_distance <= m_initial_radius) && (index_neighbor != p_index) ) {
            p_neighbors.push_back(index_neighbor);
        }
    }
}


void dbscan::create_kdtree(const dataset & p_data) {
    std::vector<void *> payload(p_data.size());
    for (std::size_t index = 0; index < p_data.size(); index++) {
        payload[index] = (void *)index;
    }

    m_kdtree = container::kdtree_balanced(p_data, payload);
}


}

}