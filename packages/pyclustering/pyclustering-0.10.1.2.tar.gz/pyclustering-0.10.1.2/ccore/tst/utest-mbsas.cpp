/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <gtest/gtest.h>

#include <pyclustering/cluster/mbsas.hpp>

#include <pyclustering/utils/metric.hpp>

#include "samples.hpp"

#include "utenv_check.hpp"


using namespace pyclustering;
using namespace pyclustering::clst;


static void
template_mbsas_length_process_data(const dataset_ptr p_data,
        const std::size_t & p_amount,
        const double & p_threshold,
        const std::vector<size_t> & p_expected_cluster_length,
        const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean()) {

    mbsas_data output_result;
    mbsas solver(p_amount, p_threshold, p_metric);
    solver.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = output_result.clusters();
    const representative_sequence & actual_repr = output_result.representatives();

    for (auto & repr : actual_repr)
        ASSERT_EQ(data[0].size(), repr.size());

    ASSERT_EQ(actual_repr.size(), actual_clusters.size());
    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


TEST(utest_mbsas, allocation_sample_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1.0, expected_clusters_length);
}


TEST(utest_mbsas, allocation_sample_simple_01_euclidean) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1.0, expected_clusters_length, distance_metric_factory<point>::euclidean());
}


TEST(utest_mbsas, allocation_sample_simple_01_euclidean_square) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1.0, expected_clusters_length, distance_metric_factory<point>::euclidean_square());
}


TEST(utest_mbsas, allocation_sample_simple_01_manhattan) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1.0, expected_clusters_length, distance_metric_factory<point>::manhattan());
}


TEST(utest_mbsas, allocation_sample_simple_01_chebyshev) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1.0, expected_clusters_length, distance_metric_factory<point>::chebyshev());
}


TEST(utest_mbsas, allocation_sample_simple_01_minkowski) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1.0, expected_clusters_length, distance_metric_factory<point>::minkowski(2.0));
}


TEST(utest_mbsas, allocation_sample_simple_01_user_defined) {
    const std::vector<size_t> expected_clusters_length = { 5, 5 };

    auto user_metric = [](const point & p1, const point & p2) { return euclidean_distance(p1, p2); };

    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1.0, expected_clusters_length, distance_metric_factory<point>::user_defined(user_metric));
}


TEST(utest_mbsas, allocation_one_allocation_sample_simple_01) {
    const std::vector<size_t> expected_clusters_length = { 10 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 10.0, expected_clusters_length);
}


TEST(utest_mbsas, allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 5, 8, 10 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, 1.0, expected_clusters_length);
}


TEST(utest_mbsas, allocation_one_allocation_sample_simple_02) {
    const std::vector<size_t> expected_clusters_length = { 23 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, 10.0, expected_clusters_length);
}


TEST(utest_mbsas, allocation_one_dimension_points_1) {
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 3, 1.0, expected_clusters_length);
}


TEST(utest_mbsas, allocation_one_allocation_one_dimension_points_1) {
    const std::vector<size_t> expected_clusters_length = { 20 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 3, 10.0, expected_clusters_length);
}


TEST(utest_mbsas, allocation_one_dimension_points_2) {
    const std::vector<size_t> expected_clusters_length = { 10, 20 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 3, 1.0, expected_clusters_length);
}


TEST(utest_mbsas, allocation_one_allocation_one_dimension_points_2) {
    const std::vector<size_t> expected_clusters_length = { 30 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 3, 10.0, expected_clusters_length);
}


TEST(utest_mbsas, allocation_three_dimension_points_2) {
    const std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 2, 1.0, expected_clusters_length);
}


TEST(utest_mbsas, allocation_three_allocation_one_dimension_points_2) {
    const std::vector<size_t> expected_clusters_length = { 20 };
    template_mbsas_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 2, 10.0, expected_clusters_length);
}