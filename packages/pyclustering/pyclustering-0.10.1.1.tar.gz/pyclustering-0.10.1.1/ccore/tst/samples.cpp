/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include "samples.hpp"

#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <sstream>


#if defined _WIN32 || defined __CYGWIN__
    #define separator std::string("\\")
#else
    #define separator std::string("/")
#endif


const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_FOLDER =
    ".." + separator +
    ".." + separator +
    "pyclustering" + separator +
    "samples" + separator +
    "samples" + separator +
    "simple" + separator;


const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_01 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple01.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_02 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple02.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_03 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple03.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_04 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple04.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_05 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple05.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_06 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple06.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_07 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple07.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_08 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple08.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_09 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple09.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_10 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple10.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_11 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple11.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_12 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple12.data";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_13 = PATH_SAMPLE_SIMPLE_FOLDER + "Simple13.data";


const simple_sample_factory::map_sample simple_sample_factory::m_sample_table = {
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_01, simple_sample_factory::PATH_SAMPLE_SIMPLE_01 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_02, simple_sample_factory::PATH_SAMPLE_SIMPLE_02 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_03, simple_sample_factory::PATH_SAMPLE_SIMPLE_03 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_04, simple_sample_factory::PATH_SAMPLE_SIMPLE_04 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_05, simple_sample_factory::PATH_SAMPLE_SIMPLE_05 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_06, simple_sample_factory::PATH_SAMPLE_SIMPLE_06 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_07, simple_sample_factory::PATH_SAMPLE_SIMPLE_07 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_08, simple_sample_factory::PATH_SAMPLE_SIMPLE_08 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_09, simple_sample_factory::PATH_SAMPLE_SIMPLE_09 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_10, simple_sample_factory::PATH_SAMPLE_SIMPLE_10 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_11, simple_sample_factory::PATH_SAMPLE_SIMPLE_11 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_12, simple_sample_factory::PATH_SAMPLE_SIMPLE_12 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_13, simple_sample_factory::PATH_SAMPLE_SIMPLE_13 }
};



const std::string fcps_sample_factory::PATH_FCPS_SAMPLE_FOLDER = 
    ".." + separator +
    ".." + separator +
    "pyclustering" + separator +
    "samples" + separator +
    "samples" + separator +
    "fcps" + separator;


const std::string fcps_sample_factory::PATH_SAMPLE_ATOM         = PATH_FCPS_SAMPLE_FOLDER + "Atom.data";
const std::string fcps_sample_factory::PATH_SAMPLE_CHAINLINK    = PATH_FCPS_SAMPLE_FOLDER + "Chainlink.data";
const std::string fcps_sample_factory::PATH_SAMPLE_ENGY_TIME    = PATH_FCPS_SAMPLE_FOLDER + "EngyTime.data";
const std::string fcps_sample_factory::PATH_SAMPLE_GOLF_BALL    = PATH_FCPS_SAMPLE_FOLDER + "GolfBall.data";
const std::string fcps_sample_factory::PATH_SAMPLE_HEPTA        = PATH_FCPS_SAMPLE_FOLDER + "Hepta.data";
const std::string fcps_sample_factory::PATH_SAMPLE_LSUN         = PATH_FCPS_SAMPLE_FOLDER + "Lsun.data";
const std::string fcps_sample_factory::PATH_SAMPLE_TARGET       = PATH_FCPS_SAMPLE_FOLDER + "Target.data";
const std::string fcps_sample_factory::PATH_SAMPLE_TETRA        = PATH_FCPS_SAMPLE_FOLDER + "Tetra.data";
const std::string fcps_sample_factory::PATH_SAMPLE_TWO_DIAMONDS = PATH_FCPS_SAMPLE_FOLDER + "TwoDiamonds.data";
const std::string fcps_sample_factory::PATH_SAMPLE_WING_NUT     = PATH_FCPS_SAMPLE_FOLDER + "WingNut.data";


const fcps_sample_factory::map_sample fcps_sample_factory::m_sample_table = {
    { FCPS_SAMPLE::ATOM,            fcps_sample_factory::PATH_SAMPLE_ATOM           },
    { FCPS_SAMPLE::CHAINLINK,       fcps_sample_factory::PATH_SAMPLE_CHAINLINK      },
    { FCPS_SAMPLE::ENGY_TIME,       fcps_sample_factory::PATH_SAMPLE_ENGY_TIME      },
    { FCPS_SAMPLE::GOLF_BALL,       fcps_sample_factory::PATH_SAMPLE_GOLF_BALL      },
    { FCPS_SAMPLE::HEPTA,           fcps_sample_factory::PATH_SAMPLE_HEPTA          },
    { FCPS_SAMPLE::LSUN,            fcps_sample_factory::PATH_SAMPLE_LSUN           },
    { FCPS_SAMPLE::TARGET,          fcps_sample_factory::PATH_SAMPLE_TARGET         },
    { FCPS_SAMPLE::TETRA,           fcps_sample_factory::PATH_SAMPLE_TETRA          },
    { FCPS_SAMPLE::TWO_DIAMONDS,    fcps_sample_factory::PATH_SAMPLE_TWO_DIAMONDS   },
    { FCPS_SAMPLE::WING_NUT,        fcps_sample_factory::PATH_SAMPLE_WING_NUT       }
};



const std::string famous_sample_factory::PATH_FAMOUS_SAMPLE_FOLDER = 
    ".." + separator +
    ".." + separator +
    "pyclustering" + separator +
    "samples" + separator +
    "samples" + separator +
    "famous" + separator;


const std::string famous_sample_factory::PATH_OLD_FAITHFUL = PATH_FAMOUS_SAMPLE_FOLDER + "OldFaithful.data";
const std::string famous_sample_factory::PATH_IRIS         = PATH_FAMOUS_SAMPLE_FOLDER + "Iris.data";


const famous_sample_factory::map_sample famous_sample_factory::m_sample_table = {
    { FAMOUS_SAMPLE::OLD_FAITHFUL,    famous_sample_factory::PATH_OLD_FAITHFUL   },
    { FAMOUS_SAMPLE::SAMPLE_IRIS,     famous_sample_factory::PATH_IRIS           }
};



std::shared_ptr<dataset> generic_sample_factory::create_sample(const std::string & path_sample) {
    std::shared_ptr<dataset> sample_data(new dataset);
    size_t sample_dimension = 0;

    std::ifstream file_sample(path_sample);
    if (file_sample.is_open()) {
        std::string file_line;

        while(std::getline(file_sample, file_line)) {
            if (file_line.empty())
                continue;

            double value = 0.0;
            point sample_point;

            std::istringstream stream_value(file_line);

            while(stream_value >> value) {
                sample_point.push_back(value);
            }

            if (sample_dimension == 0) {
                sample_dimension = sample_point.size();
            }
            else {
                if (sample_dimension != sample_point.size()) {
                    throw std::runtime_error("Points from input data set should have the same dimension.");
                }
            }

            sample_data->push_back(sample_point);
        }
    }

    return sample_data;
}


std::shared_ptr<dataset> simple_sample_factory::create_sample(const SAMPLE_SIMPLE p_sample, const bool p_random_order) {
    const std::string path_sample = m_sample_table.at(p_sample);
    auto points = generic_sample_factory::create_sample(path_sample);

    if (p_random_order) {
        std::random_device device;
        std::mt19937 generator(device());

        std::shuffle(points->begin(), points->end(), generator);
    }

    return points;
}


std::shared_ptr<dataset> simple_sample_factory::create_random_sample(const std::size_t p_cluster_size, const std::size_t p_clusters) {
    std::shared_ptr<dataset> sample_data(new dataset);

    std::random_device device;
    std::mt19937 generator(device());

    for (std::size_t index_cluster = 0; index_cluster < p_clusters; index_cluster++) {
        for (std::size_t index_point = 0; index_point < p_cluster_size; index_point++) {
            sample_data->push_back({ 
                std::generate_canonical<double, 32>(generator) + index_point * 5, 
                std::generate_canonical<double, 32>(generator) + index_point * 5
            });
        }
    }

    return sample_data;
}



std::shared_ptr<dataset> fcps_sample_factory::create_sample(const FCPS_SAMPLE sample) {
    const std::string path_sample = m_sample_table.at(sample);
    return generic_sample_factory::create_sample(path_sample);
}


std::shared_ptr<dataset> famous_sample_factory::create_sample(const FAMOUS_SAMPLE sample) {
    const std::string path_sample = m_sample_table.at(sample);
    return generic_sample_factory::create_sample(path_sample);
}