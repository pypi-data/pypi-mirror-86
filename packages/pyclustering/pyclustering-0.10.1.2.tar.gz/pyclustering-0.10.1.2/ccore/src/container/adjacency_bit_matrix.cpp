/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/container/adjacency_bit_matrix.hpp>

#include <string>
#include <stdexcept>


namespace pyclustering {

namespace container {


const size_t adjacency_bit_matrix::DEFAULT_EXISTANCE_CONNECTION_VALUE = 0x01;
const size_t adjacency_bit_matrix::DEFAULT_NON_EXISTANCE_CONNECTION_VALUE = 0x00;


adjacency_bit_matrix::adjacency_bit_matrix(const size_t node_amount) :
    m_adjacency(node_amount, std::vector<size_t>(node_amount, 0)),
    m_size(node_amount)
{ }


adjacency_bit_matrix::~adjacency_bit_matrix() { }


size_t adjacency_bit_matrix::size() const { return m_size; }


void adjacency_bit_matrix::set_connection(const size_t node_index1, const size_t node_index2) {
    update_connection(node_index1, node_index2, DEFAULT_EXISTANCE_CONNECTION_VALUE);
}


void adjacency_bit_matrix::erase_connection(const size_t node_index1, const size_t node_index2) {
    update_connection(node_index1, node_index2, DEFAULT_NON_EXISTANCE_CONNECTION_VALUE);
}


bool adjacency_bit_matrix::has_connection(const size_t node_index1, const size_t node_index2) const {
    const size_t index_element = node_index2 / (sizeof(size_t) << 3);
    const size_t bit_number = node_index2 - (index_element * (sizeof(size_t) << 3));

    const size_t bit_value = (m_adjacency[node_index1][index_element] >> bit_number) & (size_t) DEFAULT_EXISTANCE_CONNECTION_VALUE;

    return (bit_value > 0);
}


void adjacency_bit_matrix::get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const {
    node_neighbors.clear();
    
    for (size_t neighbor_index = 0; neighbor_index != m_adjacency.size(); neighbor_index++) {
        if (has_connection(node_index, neighbor_index)) {
            node_neighbors.push_back(neighbor_index);
        }
    }
}


void adjacency_bit_matrix::clear() {
    m_adjacency.clear();
    m_size = 0;
}


void adjacency_bit_matrix::update_connection(const size_t node_index1, const size_t node_index2, const size_t state_connection) {
    size_t element_byte_length = (sizeof(size_t) << 3);
    size_t index_element = node_index2 / element_byte_length;
    size_t bit_number = node_index2 % element_byte_length;

    if ( (node_index1 > m_adjacency.size()) || (index_element > m_adjacency.size()) ) {
        std::string message("adjacency bit matrix size: " + std::to_string(m_adjacency.size()) + ", index1: " + std::to_string(node_index1) + ", index2: " + std::to_string(node_index2));
        throw std::out_of_range(message);
    }

    if (state_connection > 0) {
        m_adjacency[node_index1][index_element] |= ((size_t) 0x01 << bit_number);
    }
    else {
        m_adjacency[node_index1][index_element] &= ~((size_t) 0x01 << bit_number);
    }
}


adjacency_bit_matrix & adjacency_bit_matrix::operator=(adjacency_bit_matrix && another_matrix) {
    if (this != &another_matrix) {
        m_adjacency = std::move(another_matrix.m_adjacency);
        m_size = std::move(another_matrix.m_size);

        another_matrix.m_size = 0;
    }

    return *this;
}


}

}