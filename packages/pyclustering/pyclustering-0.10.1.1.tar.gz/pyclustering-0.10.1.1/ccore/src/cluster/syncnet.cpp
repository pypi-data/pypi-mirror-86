/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/cluster/syncnet.hpp>

#include <limits>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;
using namespace pyclustering::nnet;

using namespace std::placeholders;


namespace pyclustering {

namespace clst {


void syncnet_analyser::allocate_clusters(const double eps, syncnet_cluster_data & data) {
    allocate_sync_ensembles(eps, data);
}



syncnet::syncnet(std::vector<std::vector<double> > * input_data, const double connectivity_radius, const bool enable_conn_weight, const initial_type initial_phases) :
sync_network(input_data->size(), 1, 0, connection_t::CONNECTION_NONE, initial_type::RANDOM_GAUSSIAN)
{
    equation<double> oscillator_equation = std::bind(&syncnet::phase_kuramoto_equation, this, _1, _2, _3, _4);
    set_equation(oscillator_equation);

    oscillator_locations = new std::vector<std::vector<double> >(*input_data);
    create_connections(connectivity_radius, enable_conn_weight);
}


syncnet::~syncnet() {
    if (oscillator_locations != nullptr) {
        delete oscillator_locations;
        oscillator_locations = nullptr;
    }

    if (distance_conn_weights != nullptr) {
        delete distance_conn_weights;
        distance_conn_weights = nullptr;
    }
}


void syncnet::create_connections(const double connectivity_radius, const bool enable_conn_weight) {
    double sqrt_connectivity_radius = connectivity_radius * connectivity_radius;

    if (enable_conn_weight == true) {
        std::vector<double> instance(size(), 0);
        distance_conn_weights = new std::vector<std::vector<double> >(size(), instance);
    }
    else {
        distance_conn_weights = nullptr;
    }

    double maximum_distance = 0;
    double minimum_distance = std::numeric_limits<double>::max();

    for (std::size_t i = 0; i < size(); i++) {
        for (std::size_t j = i + 1; j < size(); j++) {
            double distance = euclidean_distance_square( (*oscillator_locations)[i], (*oscillator_locations)[j] );

            if (distance <= sqrt_connectivity_radius) {
                m_connections->set_connection(j, i);
                m_connections->set_connection(i, j);
            }

            if (enable_conn_weight == true) {
                (*distance_conn_weights)[i][j] = distance;
                (*distance_conn_weights)[j][i] = distance;

                if (distance > maximum_distance) {
                    maximum_distance = distance;
                }

                if (distance < maximum_distance) {
                    maximum_distance = distance;
                }
            }
        }
    }

    if (enable_conn_weight == true) {
        double multiplier = 1;
        double subtractor = 0;

        if (maximum_distance != minimum_distance) {
            multiplier = maximum_distance - minimum_distance;
            subtractor = minimum_distance;
        }

        for (std::size_t i = 0; i < size(); i++) {
            for (std::size_t j = i + 1; j < size(); j++) {
                double value_weight = ((*distance_conn_weights)[i][j] - subtractor) / multiplier;

                (*distance_conn_weights)[i][j] = value_weight;
                (*distance_conn_weights)[j][i] = value_weight;
            }
        }
    }
}


double syncnet::phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) const {
    std::size_t index = *(unsigned int *) argv[0];
    std::size_t num_neighbors = 0;
    double phase = 0;

    /* Avoid a lot of checking of this condition in the loop */
    if (distance_conn_weights != nullptr) {
        for (std::size_t k = 0; k < size(); k++) {
            if (m_connections->has_connection(index, k)) {
                phase += (*distance_conn_weights)[index][k] * std::sin( m_oscillators[k].phase - teta );
                num_neighbors++;
            }
        }
    }
    else {
        for (std::size_t k = 0; k < size(); k++) {
            if (m_connections->has_connection(index, k)) {
                phase += std::sin( m_oscillators[k].phase - teta );
                num_neighbors++;
            }
        }
    }

    if (num_neighbors == 0) {
        num_neighbors = 1;
    }

    phase = phase * weight / num_neighbors;
    return phase;
}


void syncnet::phase_kuramoto_equation(const double t, const differ_state<double> & inputs,  const differ_extra<void *> & argv, differ_state<double> & outputs) const {
    outputs.resize(1);
    outputs[0] = phase_kuramoto(t, inputs[0], argv);
}


void syncnet::process(const double order, const solve_type solver, const bool collect_dynamic, syncnet_analyser & analyser) {
    simulate_dynamic(order, 0.1, solver, collect_dynamic, analyser);
}


}

}
