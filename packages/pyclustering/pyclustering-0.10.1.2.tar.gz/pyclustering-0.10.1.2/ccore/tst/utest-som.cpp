/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include "samples.hpp"

#include <pyclustering/nnet/som.hpp>

#include <algorithm>
#include <numeric>


using namespace pyclustering;
using namespace pyclustering::nnet;


static void template_create_delete(const unsigned int rows, const unsigned int cols, const som_conn_type conn_type, const som_init_type init_type) {
    som_parameters params;
    params.init_type = init_type;

    som * som_map = new som(rows, cols, conn_type, params);
    ASSERT_EQ(rows * cols, som_map->get_size());

    delete som_map;
}


TEST(utest_som, create_delete_conn_func_neighbor) {
    template_create_delete(10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_conn_grid_eight) {
    template_create_delete(10, 10, som_conn_type::SOM_GRID_EIGHT, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_conn_grid_four) {
    template_create_delete(10, 10, som_conn_type::SOM_GRID_FOUR, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_conn_honeycomb) {
  template_create_delete(10, 10, som_conn_type::SOM_HONEYCOMB, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_init_centroid) {
    template_create_delete(10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_RANDOM_CENTROID);
}

TEST(utest_som, create_delete_init_surface) {
    template_create_delete(10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_RANDOM_SURFACE);
}

TEST(utest_som, create_delete_init_uniform_grid) {
    template_create_delete(10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_UNIFORM_GRID);
}


static void template_award_neurons(const std::shared_ptr<dataset> & data,
                                   const unsigned int epouchs, 
                                   const bool autostop, 
                                   const unsigned int rows, 
                                   const unsigned int cols, 
                                   const som_conn_type conn_type, 
                                   const std::vector<unsigned int> & expected_result) {

    som_parameters params;
    som som_map(rows, cols, conn_type, params);
    som_map.train(*data.get(), epouchs, autostop);

    size_t winners = som_map.get_winner_number();
    ASSERT_EQ(expected_result.size(), winners);

    som_award_sequence & awards = som_map.get_awards();

    std::sort(awards.begin(), awards.end());

    ASSERT_EQ(expected_result.size(), awards.size());

    for (size_t i = 0; i < awards.size(); i++) {
        ASSERT_EQ(expected_result[i], awards[i]);
    }

    som_gain_sequence captured_objects = som_map.get_capture_objects();

    size_t total_capture_points = 0;
    for (size_t i = 0; i < captured_objects.size(); i++) {
        total_capture_points += captured_objects[i].size();
    }

    size_t expected_capture_points = std::accumulate(expected_result.begin(), expected_result.end(), (std::size_t) 0);
    ASSERT_EQ(expected_capture_points, total_capture_points);
}

TEST(utest_som, awards_two_clusters_func_neighbor) {
    std::vector<unsigned int> expected_awards = {5, 5};
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, false, 1, 2, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
    template_award_neurons(sample_simple_01, 100, false, 2, 1, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
}

TEST(utest_som, awards_two_clusters_func_neighbor_autostop) {
    std::vector<unsigned int> expected_awards = { 5, 5 };
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, true, 1, 2, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
    template_award_neurons(sample_simple_01, 100, true, 2, 1, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_eight) {
    std::vector<unsigned int> expected_awards = {5, 5};
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, false, 1, 2, som_conn_type::SOM_GRID_EIGHT, expected_awards);
    template_award_neurons(sample_simple_01, 100, false, 2, 1, som_conn_type::SOM_GRID_EIGHT, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_eight_autostop) {
    std::vector<unsigned int> expected_awards = { 5, 5 };
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, true, 1, 2, som_conn_type::SOM_GRID_EIGHT, expected_awards);
    template_award_neurons(sample_simple_01, 100, true, 2, 1, som_conn_type::SOM_GRID_EIGHT, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_four) {
    std::vector<unsigned int> expected_awards = {5, 5};
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, false, 1, 2, som_conn_type::SOM_GRID_FOUR, expected_awards);
    template_award_neurons(sample_simple_01, 100, false, 2, 1, som_conn_type::SOM_GRID_FOUR, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_four_autostop) {
    std::vector<unsigned int> expected_awards = { 5, 5 };
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, true, 1, 2, som_conn_type::SOM_GRID_FOUR, expected_awards);
    template_award_neurons(sample_simple_01, 100, true, 2, 1, som_conn_type::SOM_GRID_FOUR, expected_awards);
}

TEST(utest_som, awards_two_clusters_honeycomb) {
    std::vector<unsigned int> expected_awards = {5, 5};
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, false, 1, 2, som_conn_type::SOM_HONEYCOMB, expected_awards);
    template_award_neurons(sample_simple_01, 100, false, 2, 1, som_conn_type::SOM_HONEYCOMB, expected_awards);
}

TEST(utest_som, awards_two_clusters_honeycomb_autostop) {
    std::vector<unsigned int> expected_awards = { 5, 5 };
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, true, 1, 2, som_conn_type::SOM_HONEYCOMB, expected_awards);
    template_award_neurons(sample_simple_01, 100, true, 2, 1, som_conn_type::SOM_HONEYCOMB, expected_awards);
}

TEST(utest_som, awards_clusters_func_neighbor_simple_sample_02) {
    std::vector<unsigned int> expected_awards = { 5, 8, 10 };
    std::shared_ptr<dataset> sample_simple_02 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_award_neurons(sample_simple_02, 100, false, 1, 3, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
    template_award_neurons(sample_simple_02, 100, false, 3, 1, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
}

TEST(utest_som, awards_clusters_grid_eight_simple_sample_02) {
    std::vector<unsigned int> expected_awards = { 5, 8, 10 };
    std::shared_ptr<dataset> sample_simple_02 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_award_neurons(sample_simple_02, 100, false, 1, 3, som_conn_type::SOM_GRID_EIGHT, expected_awards);
    template_award_neurons(sample_simple_02, 100, false, 3, 1, som_conn_type::SOM_GRID_EIGHT, expected_awards);
}

TEST(utest_som, awards_clusters_func_grid_four_simple_sample_02) {
    std::vector<unsigned int> expected_awards = { 5, 8, 10 };
    std::shared_ptr<dataset> sample_simple_02 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_award_neurons(sample_simple_02, 100, false, 1, 3, som_conn_type::SOM_GRID_FOUR, expected_awards);
    template_award_neurons(sample_simple_02, 100, false, 3, 1, som_conn_type::SOM_GRID_FOUR, expected_awards);
}

TEST(utest_som, awards_clusters_honeycomb_simple_sample_02) {
    std::vector<unsigned int> expected_awards = { 5, 8, 10 };
    std::shared_ptr<dataset> sample_simple_02 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_award_neurons(sample_simple_02, 100, false, 1, 3, som_conn_type::SOM_HONEYCOMB, expected_awards);
    template_award_neurons(sample_simple_02, 100, false, 3, 1, som_conn_type::SOM_HONEYCOMB, expected_awards);
}

TEST(utest_som, awards_clusters_func_neighbor_simple_sample_03) {
    std::vector<unsigned int> expected_awards = { 10, 10, 10, 30 };
    std::shared_ptr<dataset> sample_simple_03 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_award_neurons(sample_simple_03, 100, false, 1, 4, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
    template_award_neurons(sample_simple_03, 100, false, 2, 2, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
}

TEST(utest_som, awards_clusters_grid_eight_simple_sample_03) {
    std::vector<unsigned int> expected_awards = { 10, 10, 10, 30 };
    std::shared_ptr<dataset> sample_simple_03 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_award_neurons(sample_simple_03, 100, false, 1, 4, som_conn_type::SOM_GRID_EIGHT, expected_awards);
    template_award_neurons(sample_simple_03, 100, false, 2, 2, som_conn_type::SOM_GRID_EIGHT, expected_awards);
}

TEST(utest_som, awards_clusters_func_grid_four_simple_sample_03) {
    std::vector<unsigned int> expected_awards = { 10, 10, 10, 30 };
    std::shared_ptr<dataset> sample_simple_03 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_award_neurons(sample_simple_03, 100, false, 1, 4, som_conn_type::SOM_GRID_FOUR, expected_awards);
    template_award_neurons(sample_simple_03, 100, false, 2, 2, som_conn_type::SOM_GRID_FOUR, expected_awards);
}

TEST(utest_som, awards_clusters_honeycomb_simple_sample_03) {
    std::vector<unsigned int> expected_awards = { 10, 10, 10, 30 };
    std::shared_ptr<dataset> sample_simple_03 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_award_neurons(sample_simple_03, 100, false, 1, 4, som_conn_type::SOM_HONEYCOMB, expected_awards);
    template_award_neurons(sample_simple_03, 100, false, 2, 2, som_conn_type::SOM_HONEYCOMB, expected_awards);
}

TEST(utest_som, double_training) {
    som_parameters params;
    som som_map(2, 2, som_conn_type::SOM_GRID_EIGHT, params);

    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);

    som_map.train(*sample_simple_01.get(), 100, false);
    som_map.train(*sample_simple_01.get(), 100, false);

    const som_gain_sequence & captured_objects = som_map.get_capture_objects();

    size_t total_capture_points = 0;
    for (size_t i = 0; i < captured_objects.size(); i++) {
        total_capture_points += captured_objects[i].size();
    }

    ASSERT_EQ(sample_simple_01->size(), total_capture_points);

    const som_award_sequence & awards = som_map.get_awards();

    size_t number_awards = std::accumulate(awards.cbegin(), awards.cend(), (std::size_t) 0);

    ASSERT_EQ(sample_simple_01->size(), number_awards);
}


static void template_simulate_check_winners(const som_conn_type conn_type, const bool autostop, const bool p_reload = false) {
    som_parameters params;
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);

    som som_map(1, 2, conn_type, params);
    som_map.train(*sample_simple_01.get(), 100, autostop);

    if (p_reload) {
        auto weights = som_map.get_weights();
        auto captured_objects = som_map.get_capture_objects();
        auto awards = som_map.get_awards();

        som_map = som(1, 2, conn_type, params);
        som_map.load(weights, awards, captured_objects);
    }

    std::vector<std::size_t> expected_winners = { 0, 1 };
    for (std::size_t i = 0; i < sample_simple_01->size(); i++) {
        std::size_t index_winner = som_map.simulate(sample_simple_01->at(i));
        if ( (i == 0) && (index_winner != 0) ) {
            expected_winners = { 1, 0 };
        }

        if (i < 5)
            EXPECT_EQ(expected_winners[0], index_winner);
        else
            EXPECT_EQ(expected_winners[1], index_winner);
    }
}


TEST(utest_som, simulate_func_neighbors_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_FUNC_NEIGHBOR, true);
}

TEST(utest_som, simulate_func_neighbors_autostop_reload) {
    template_simulate_check_winners(som_conn_type::SOM_FUNC_NEIGHBOR, true, true);
}

TEST(utest_som, simulate_grid_four_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_FOUR, true);
}

TEST(utest_som, simulate_grid_four_autostop_reload) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_FOUR, true, true);
}

TEST(utest_som, simulate_grid_eight_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_EIGHT, true);
}

TEST(utest_som, simulate_grid_eight_autostop_reload) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_EIGHT, true, true);
}

TEST(utest_som, simulate_honeycomb_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_HONEYCOMB, true);
}

TEST(utest_som, simulate_honeycomb_autostop_reload) {
    template_simulate_check_winners(som_conn_type::SOM_HONEYCOMB, true, true);
}

TEST(utest_som, simulate_func_neighbors_without_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_FUNC_NEIGHBOR, false);
}

TEST(utest_som, simulate_func_neighbors_without_autostop_reload) {
    template_simulate_check_winners(som_conn_type::SOM_FUNC_NEIGHBOR, false, true);
}

TEST(utest_som, simulate_grid_four_without_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_FOUR, false);
}

TEST(utest_som, simulate_grid_four_without_autostop_reload) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_FOUR, false, true);
}

TEST(utest_som, simulate_grid_eight_without_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_EIGHT, false);
}

TEST(utest_som, simulate_grid_eight_without_autostop_reload) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_EIGHT, false, true);
}

TEST(utest_som, simulate_honeycomb_without_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_HONEYCOMB, false);
}

TEST(utest_som, simulate_honeycomb_without_autostop_reload) {
    template_simulate_check_winners(som_conn_type::SOM_HONEYCOMB, false, true);
}


static void template_random_state(const std::size_t rows, const std::size_t cols, const som_conn_type conn_type, const std::size_t random_state, const bool autostop) {
    som_parameters params;
    params.random_state = random_state;

    dataset_ptr sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);

    som som_1(rows, cols, conn_type, params);
    std::size_t steps_1 = som_1.train(*sample_simple_01.get(), 100, autostop);

    som som_2(rows, cols, conn_type, params);
    std::size_t steps_2 = som_2.train(*sample_simple_01.get(), 100, autostop);

    ASSERT_EQ(steps_1, steps_2);
    ASSERT_EQ(som_1.get_awards(), som_2.get_awards());
    ASSERT_EQ(som_1.get_weights(), som_2.get_weights());
    ASSERT_EQ(som_1.get_capture_objects(), som_2.get_capture_objects());
    ASSERT_EQ(som_1.get_winner_number(), som_2.get_winner_number());
}

TEST(utest_som, random_state_neighbor_2x2_rnd_1) {
    template_random_state(2, 2, som_conn_type::SOM_FUNC_NEIGHBOR, 1, false);
}

TEST(utest_som, random_state_neighbor_2x2_rnd_2) {
    template_random_state(2, 2, som_conn_type::SOM_FUNC_NEIGHBOR, 2, false);
}

TEST(utest_som, random_state_neighbor_2x2_rnd_3) {
    template_random_state(2, 2, som_conn_type::SOM_FUNC_NEIGHBOR, 3, false);
}

TEST(utest_som, random_state_neighbor_2x4_rnd_2) {
    template_random_state(2, 4, som_conn_type::SOM_FUNC_NEIGHBOR, 2, false);
}

TEST(utest_som, random_state_four_grid) {
    template_random_state(2, 4, som_conn_type::SOM_GRID_FOUR, 2, false);
}

TEST(utest_som, random_state_eight_grid) {
    template_random_state(2, 4, som_conn_type::SOM_GRID_EIGHT, 2, false);
}

TEST(utest_som, random_state_honeycomb_grid) {
    template_random_state(2, 4, som_conn_type::SOM_HONEYCOMB, 2, false);
}

TEST(utest_som, random_state_autostop_rnd_1) {
    template_random_state(2, 2, som_conn_type::SOM_FUNC_NEIGHBOR, 1, true);
}

TEST(utest_som, random_state_autostop_rnd_2) {
    template_random_state(2, 2, som_conn_type::SOM_FUNC_NEIGHBOR, 2, true);
}

TEST(utest_som, random_state_autostop_rnd_5) {
    template_random_state(2, 2, som_conn_type::SOM_FUNC_NEIGHBOR, 5, true);
}
