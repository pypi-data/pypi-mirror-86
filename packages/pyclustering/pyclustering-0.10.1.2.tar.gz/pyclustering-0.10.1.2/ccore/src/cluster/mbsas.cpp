/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/cluster/mbsas.hpp>


namespace pyclustering {

namespace clst {


mbsas::mbsas(const std::size_t p_amount,
             const double p_threshold,
             const distance_metric<point> & p_metric) :
    bsas(p_amount, p_threshold, p_metric)
{ }


void mbsas::process(const dataset & p_data, mbsas_data & p_result) {
    m_result_ptr = &p_result;

    cluster_sequence & clusters = m_result_ptr->clusters();
    representative_sequence & representative = m_result_ptr->representatives();

    clusters.push_back({ 0 });
    representative.push_back( p_data[0] );

    std::vector<std::size_t> skipped_objects = { };

    for (std::size_t i = 1; i < p_data.size(); i++) {
        auto nearest = find_nearest_cluster(p_data[i]);

        if ( (nearest.m_distance > m_threshold) && (clusters.size() < m_amount) ) {
            representative.push_back(p_data[i]);
            clusters.push_back({ i });
        }
        else {
            skipped_objects.push_back(i);
        }
    }

    for (auto index : skipped_objects) {
        auto nearest = find_nearest_cluster(p_data[index]);

        clusters.at(nearest.m_index).push_back(index);
        update_representative(nearest.m_index, p_data[index]);
    }
}


}

}