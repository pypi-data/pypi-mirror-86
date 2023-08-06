/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/cluster/random_center_initializer.hpp>

#include <chrono>
#include <random>


namespace pyclustering {

namespace clst {


random_center_initializer::random_center_initializer(const std::size_t p_amount, const long long p_random_state) :
    m_amount(p_amount),
    m_random_state(p_random_state),
    m_generator(std::random_device()())
{ 
    initialize_random_generator();
}


void random_center_initializer::initialize(const dataset & p_data, dataset & p_centers) const {
    initialize(p_data, { }, p_centers);
}


void random_center_initializer::initialize_random_generator() {
    if (m_random_state == RANDOM_STATE_CURRENT_TIME) {
        m_generator.seed(static_cast<unsigned int>(std::chrono::system_clock::now().time_since_epoch().count()));
    }
    else {
        m_generator.seed(static_cast<unsigned int>(m_random_state));
    }
}


void random_center_initializer::initialize(const dataset & p_data, const index_sequence & p_indexes, dataset & p_centers) const {
    p_centers.clear();
    p_centers.reserve(m_amount);

    if ((m_amount > p_data.size()) || (m_amount == 0)) {
        return;
    }

    m_available_indexes.reserve(p_data.size());
    for (std::size_t i = 0; i < p_data.size(); i++) {
        m_available_indexes.insert(i);
    }

    if (m_amount == p_data.size()) {
        p_centers = p_data;
        return;
    }

    for (std::size_t i = 0; i < m_amount; i++) {
        create_center(p_data, p_centers);
    }
}


void random_center_initializer::create_center(const dataset & p_data, dataset & p_centers) const {
    std::uniform_int_distribution<std::size_t> distribution(0, p_data.size() - 1);
    std::size_t random_index_point = distribution(m_generator);

    index_storage::iterator available_index = m_available_indexes.find(random_index_point);
    if (available_index == m_available_indexes.end()) {
        random_index_point = *m_available_indexes.begin();
        available_index = m_available_indexes.begin();
    }

    p_centers.push_back(p_data.at(random_index_point));
    m_available_indexes.erase(available_index);
}


}

}