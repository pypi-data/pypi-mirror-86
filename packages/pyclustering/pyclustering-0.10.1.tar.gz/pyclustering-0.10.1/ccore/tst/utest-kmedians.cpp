/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include "samples.hpp"

#include <pyclustering/cluster/kmedians.hpp>
#include "utenv_check.hpp"


using namespace pyclustering;
using namespace pyclustering::clst;


static void
template_kmedians_length_process_data(const dataset_ptr & p_data,
                                      const dataset & p_start_medians,
                                      const std::vector<size_t> & p_expected_cluster_length,
                                      const std::size_t p_itermax = kmedians::DEFAULT_ITERMAX,
                                      const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean_square())
{
    kmedians_data output_result;
    kmedians solver(p_start_medians, kmedians::DEFAULT_TOLERANCE, p_itermax, p_metric);
    solver.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = output_result.clusters();
    const dataset & medians = output_result.medians();

    if (p_itermax == 0) {
        ASSERT_TRUE(actual_clusters.empty());
        ASSERT_EQ(p_start_medians, medians);
        return;
    }

    ASSERT_EQ(actual_clusters.size(), medians.size());
    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


TEST(utest_kmedians, allocation_sample_simple_01) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length);
}

TEST(utest_kmedians, allocation_sample_simple_01_euclidean) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length, 
        kmedians::DEFAULT_ITERMAX, distance_metric_factory<point>::euclidean());
}

TEST(utest_kmedians, allocation_sample_simple_01_euclidean_square) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length, 
        kmedians::DEFAULT_ITERMAX, distance_metric_factory<point>::euclidean_square());
}

TEST(utest_kmedians, allocation_sample_simple_01_manhattan) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length, 
        kmedians::DEFAULT_ITERMAX, distance_metric_factory<point>::manhattan());
}

TEST(utest_kmedians, allocation_sample_simple_01_chebyshev) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length, 
        kmedians::DEFAULT_ITERMAX, distance_metric_factory<point>::chebyshev());
}

TEST(utest_kmedians, allocation_sample_simple_01_minkowski) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length, 
        kmedians::DEFAULT_ITERMAX, distance_metric_factory<point>::minkowski(2.0));
}

TEST(utest_kmedians, allocation_sample_simple_01_user_defined) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };

    auto user_metric = [](const point & p1, const point & p2) { return euclidean_distance(p1, p2); };

    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length, 
        kmedians::DEFAULT_ITERMAX, distance_metric_factory<point>::user_defined(user_metric));
}

TEST(utest_kmedians, allocation_sample_simple_02) {
    dataset start_medians = { { 3.5, 4.8 }, { 6.9, 7.0 }, { 7.5, 0.5 } };
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medians, expected_clusters_length);
}

TEST(utest_kmedians, allocation_sample_simple_03_hanging) {
    dataset start_medians = { { 1.80508 , 4.609467 }, { 0.926445, 0.126412 }, { 0.144706, 0.987019 } };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_medians, { });
}

TEST(utest_kmedians, allocation_sample_simple_03) {
    dataset start_medians = { { 0.2, 0.1 }, { 4.0, 1.0 }, { 2.0, 2.0 }, { 2.3, 3.9 } };
    std::vector<size_t> expected_clusters_length = { 10, 10, 10, 30 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_medians, expected_clusters_length);
}

TEST(utest_kmedians, large_number_medians_sample_simple_01) {
    dataset start_medians = { { 1.7, 2.6 }, { 3.7, 4.5 }, { 4.5, 1.6 }, { 6.4, 5.0 }, { 2.2, 2.2 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length);
}

TEST(utest_kmedians, large_number_medians_sample_simple_02) {
    dataset start_medians = { { -1.5, 0.8 }, { -4.9, 5.0 }, { 2.3, 3.2 }, { -1.2, -0.8 }, { 2.5, 2.9 }, { 6.8, 7.9 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medians, expected_clusters_length);
}


TEST(utest_kmedians, large_number_medians_sample_simple_03) {
    dataset start_medians = { { -8.1, 2.3 }, { -4.9, 5.5 }, { 1.3, 8.3 }, { -2.6, -1.7 }, { 5.3, 4.2 }, { 2.1, 0.0 }, { 1.7, 0.4 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_medians, expected_clusters_length);
}


TEST(utest_kmedians, one_dimension_sample_simple_07) {
    dataset start_medians = { { -2.0 }, { 4.0 } };
    std::vector<size_t> expected_clusters_length = { 10, 10 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), start_medians, expected_clusters_length);
}


TEST(utest_kmedians, one_dimension_sample_simple_08) {
    dataset start_medians = { { -4.0 }, { 3.0 }, { 6.0 }, { 10.0 } };
    std::vector<size_t> expected_clusters_length = { 15, 30, 20, 80 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), start_medians, expected_clusters_length);
}


TEST(utest_kmedians, rough_medians_sample_simple_10) {
    dataset start_medians = { { 0.0772944481804071, 0.05224990900863469 }, { 1.6021689021213712, 1.0347579135245601 }, { 2.3341008076636096, 1.280022869739064 } };
    std::vector<size_t> expected_clusters_length;   /* pass empty */
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), start_medians, expected_clusters_length);
}


TEST(utest_kmedians, itermax_0) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length, 0);
}

TEST(utest_kmedians, itermax_1) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length, 1);
}

TEST(utest_kmedians, itermax_10_simple01) {
    dataset start_medians = { { 3.7, 5.5 }, { 6.7, 7.5 } };
    std::vector<size_t> expected_clusters_length = { 5, 5 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_medians, expected_clusters_length, 10);
}

TEST(utest_kmedians, itermax_10_simple02) {
    dataset start_medians = { { 3.5, 4.8 }, { 6.9, 7.0 }, { 7.5, 0.5 } };
    std::vector<size_t> expected_clusters_length = { 10, 5, 8 };
    template_kmedians_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_medians, expected_clusters_length, 20);
}