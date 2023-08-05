/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/cluster/silhouette_ksearch.hpp>

#include <pyclustering/cluster/kmeans_plus_plus.hpp>

#include <pyclustering/cluster/kmeans.hpp>
#include <pyclustering/cluster/kmedians.hpp>
#include <pyclustering/cluster/kmedoids.hpp>

#include <numeric>


namespace pyclustering {

namespace clst {


void kmeans_allocator::allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) {
    allocate(p_amount, p_data, RANDOM_STATE_CURRENT_TIME, p_clusters);
}


void kmeans_allocator::allocate(const std::size_t p_amount, const dataset & p_data, const long long p_random_state, cluster_sequence & p_clusters) {
    dataset initial_centers;
    kmeans_plus_plus(p_amount, 1, p_random_state).initialize(p_data, initial_centers);

    kmeans_data result;
    kmeans(initial_centers).process(p_data, result);

    p_clusters = std::move(result.clusters());
}


void kmedians_allocator::allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) {
    allocate(p_amount, p_data, RANDOM_STATE_CURRENT_TIME, p_clusters);
}


void kmedians_allocator::allocate(const std::size_t p_amount, const dataset & p_data, const long long p_random_state, cluster_sequence & p_clusters) {
    dataset initial_medians;
    kmeans_plus_plus(p_amount, 1, p_random_state).initialize(p_data, initial_medians);

    kmedians_data result;
    kmedians(initial_medians).process(p_data, result);

    p_clusters = std::move(result.clusters());
}


void kmedoids_allocator::allocate(const std::size_t p_amount, const dataset & p_data, cluster_sequence & p_clusters) {
    allocate(p_amount, p_data, RANDOM_STATE_CURRENT_TIME, p_clusters);
}


void kmedoids_allocator::allocate(const std::size_t p_amount, const dataset & p_data, const long long p_random_state, cluster_sequence & p_clusters) {
    medoid_sequence initial_medoids;
    kmeans_plus_plus(p_amount, 1, p_random_state).initialize(p_data, initial_medoids);

    kmedoids_data result;
    kmedoids(initial_medoids).process(p_data, result);

    p_clusters = std::move(result.clusters());
}



silhouette_ksearch::silhouette_ksearch(const std::size_t p_kmin, const std::size_t p_kmax, const silhouette_ksearch_allocator::ptr & p_allocator, const long long p_random_state) :
    m_kmin(p_kmin),
    m_kmax(p_kmax),
    m_allocator(p_allocator),
    m_random_state(p_random_state)
{
    if (m_kmin <= 1) {
        throw std::invalid_argument("K min value '" + std::to_string(m_kmin) + 
            "' should be greater than 1 (impossible to provide silhouette score for only one cluster).");
    }
}


void silhouette_ksearch::process(const dataset & p_data, silhouette_ksearch_data & p_result) {
    if (m_kmax > p_data.size()) {
        throw std::invalid_argument("K max value '" + std::to_string(m_kmax) + 
            "' should be bigger than amount of objects '" + std::to_string(p_data.size()) + "' in input data.");
    }

    p_result.scores().reserve(m_kmax - m_kmin);

    for (std::size_t k = m_kmin; k < m_kmax; k++) {
        cluster_sequence clusters;
        m_allocator->allocate(k, p_data, m_random_state, clusters);

        if (clusters.size() != k) {
            p_result.scores().push_back(std::nan("1"));
            continue;
        }
        
        silhouette_data result;
        silhouette().process(p_data, clusters, result);

        const auto & scores = result.get_score();
        const double score = std::accumulate(scores.begin(), scores.end(), 0.0) / scores.size();
        p_result.scores().push_back(score);

        if (score > p_result.get_score()) {
            p_result.set_amount(k);
            p_result.set_score(score);
        }
    }
}


}

}