/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/nnet/legion.hpp>


using namespace pyclustering::nnet;


static void template_create_delete(const unsigned int num_osc, const connection_t type) {
    legion_parameters parameters;
    legion_network * network = new legion_network(num_osc, type, parameters);

    ASSERT_EQ(num_osc, network->size());

    delete network;
}

TEST(utest_legion, create_10_oscillators_none_conn) {
    template_create_delete(10, connection_t::CONNECTION_NONE);
}

TEST(utest_legion, create_25_oscillators_grid_four_conn) {
    template_create_delete(25, connection_t::CONNECTION_GRID_FOUR);
}

TEST(utest_legion, create_25_oscillators_grid_eight_conn) {
    template_create_delete(25, connection_t::CONNECTION_GRID_EIGHT);
}

TEST(utest_legion, create_10_oscillators_bidir_conn) {
    template_create_delete(10, connection_t::CONNECTION_LIST_BIDIRECTIONAL);
}

TEST(utest_legion, create_10_oscillators_all_to_all_conn) {
    template_create_delete(10, connection_t::CONNECTION_ALL_TO_ALL);
}


static void template_simulation(const legion_stimulus & stimulus, const connection_t type, const solve_type solver, const unsigned int steps, const double time) {
    legion_parameters parameters;
    legion_network network(stimulus.size(), type, parameters);

    legion_dynamic output_legion_dynamic;
    network.simulate(steps, time, solver, true, stimulus, output_legion_dynamic);

    ASSERT_EQ(steps, output_legion_dynamic.size());
}

TEST(utest_legion, one_unstimulated_oscillator_rk4) {
    template_simulation({ 0 }, connection_t::CONNECTION_NONE, solve_type::RUNGE_KUTTA_4, 10, 100);
}

TEST(utest_legion, one_stimulated_oscillator_rk4) {
    template_simulation({ 1 }, connection_t::CONNECTION_GRID_FOUR, solve_type::RUNGE_KUTTA_4, 10, 100);
}


#ifndef VALGRIND_ANALYSIS_SHOCK

TEST(utest_legion, dynamic_simulation_grid_four_rk4) {
    template_simulation({ 1, 1, 1, 0, 0, 0, 1, 1, 1 }, connection_t::CONNECTION_GRID_FOUR, solve_type::RUNGE_KUTTA_4, 10, 100);
}

TEST(utest_legion, dynamic_simulation_grid_eight_rk4) {
    template_simulation({ 1, 1, 1, 0, 0, 0, 1, 1, 1 }, connection_t::CONNECTION_GRID_EIGHT, solve_type::RUNGE_KUTTA_4, 10, 100);
}

#endif
