/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/cluster/kmedians.hpp>

#include <algorithm>
#include <cmath>

#include <pyclustering/parallel/parallel.hpp>
#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::parallel;
using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


const double kmedians::THRESHOLD_CHANGE         = 0.000001;

const double kmedians::DEFAULT_TOLERANCE        = 0.001;
const std::size_t kmedians::DEFAULT_ITERMAX     = 50;


kmedians::kmedians(const dataset & p_initial_medians, const double p_tolerance, const std::size_t p_max_iter, const distance_metric<point> & p_metric) :
    m_tolerance(p_tolerance),
    m_max_iter(p_max_iter),
    m_initial_medians(p_initial_medians),
    m_ptr_result(nullptr),
    m_ptr_data(nullptr),
    m_metric(p_metric)
{ }


void kmedians::process(const dataset & p_data, kmedians_data & p_output_result) {
    m_ptr_data = &p_data;
    m_ptr_result = &p_output_result;

    if (p_data[0].size() != m_initial_medians[0].size()) {
        throw std::invalid_argument("kmedians: dimension of the input data and dimension of the initial medians must be equal.");
    }

    m_ptr_result->medians() = m_initial_medians;

    double changes = std::numeric_limits<double>::max();
    double prev_changes = 0.0;

    std::size_t counter_repeaters = 0;

    for (std::size_t iteration = 0; (iteration < m_max_iter) && (changes > m_tolerance) && (counter_repeaters < 10); iteration++)
    {
        update_clusters(m_ptr_result->medians(), m_ptr_result->clusters());
        changes = update_medians(m_ptr_result->clusters(), m_ptr_result->medians());

        double change_difference = std::abs(changes - prev_changes);
        if (change_difference < THRESHOLD_CHANGE) {
            counter_repeaters++;
        }
        else {
            counter_repeaters = 0;
        }

        prev_changes = changes;
    }

    m_ptr_data = nullptr;
    m_ptr_result = nullptr;
}


void kmedians::update_clusters(const dataset & p_medians, cluster_sequence & p_clusters) {
    const dataset & data = *m_ptr_data;

    p_clusters.clear();
    p_clusters.resize(p_medians.size());

    index_sequence labels(data.size(), 0);

    parallel_for(std::size_t(0), data.size(), [this, &p_medians, &labels](std::size_t index) {
        assign_point_to_cluster(index, p_medians, labels);
    });

    for (std::size_t index_point = 0; index_point < labels.size(); index_point++) {
        const std::size_t suitable_index_cluster = labels[index_point];
        p_clusters[suitable_index_cluster].push_back(index_point);
    }

    erase_empty_clusters(p_clusters);
}


void kmedians::assign_point_to_cluster(const std::size_t p_index_point, const dataset & p_medians, index_sequence & p_lables) {
    size_t index_cluster_optim = 0;
    double distance_optim = std::numeric_limits<double>::max();

    for (size_t index_cluster = 0; index_cluster < p_medians.size(); index_cluster++) {
        double distance = m_metric((*m_ptr_data)[p_index_point], p_medians[index_cluster]);
        if (distance < distance_optim) {
            index_cluster_optim = index_cluster;
            distance_optim = distance;
        }
    }

    p_lables[p_index_point] = index_cluster_optim;
}


void kmedians::erase_empty_clusters(cluster_sequence & p_clusters) {
    for (std::size_t index_cluster = p_clusters.size() - 1; index_cluster != (std::size_t) -1; index_cluster--) {
        if (p_clusters[index_cluster].empty()) {
            p_clusters.erase(p_clusters.begin() + index_cluster);
        }
    }
}


double kmedians::update_medians(cluster_sequence & clusters, dataset & medians) {
    const dataset & data = *m_ptr_data;
    const std::size_t dimension = data[0].size();

    std::vector<point> prev_medians(medians);

    medians.clear();
    medians.resize(clusters.size(), point(dimension, 0.0));

    std::vector<double> changes(clusters.size(), 0);

    parallel_for(std::size_t(0), clusters.size(), [this, &medians, &prev_medians, &clusters, &changes](std::size_t index_cluster) {
        calculate_median(clusters[index_cluster], medians[index_cluster]);
        changes[index_cluster] = m_metric(prev_medians[index_cluster], medians[index_cluster]);
    });

    return *std::max_element(changes.cbegin(), changes.cend());
}


void kmedians::calculate_median(cluster & current_cluster, point & median) {
    const dataset & data = *m_ptr_data;
    const std::size_t dimension = data[0].size();

    for (size_t index_dimension = 0; index_dimension < dimension; index_dimension++) {
        std::sort(current_cluster.begin(), current_cluster.end(), 
            [this](std::size_t index_object1, std::size_t index_object2) 
        {
            return (*m_ptr_data)[index_object1] > (*m_ptr_data)[index_object2];
        });

        std::size_t relative_index_median = (std::size_t) (current_cluster.size() - 1) / 2;
        std::size_t index_median = current_cluster[relative_index_median];

        if (current_cluster.size() % 2 == 0) {
            std::size_t index_median_second = current_cluster[relative_index_median + 1];
            median[index_dimension] = (data[index_median][index_dimension] + data[index_median_second][index_dimension]) / 2.0;
        }
        else {
            median[index_dimension] = data[index_median][index_dimension];
        }
    }
}


}

}
