/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/interface/elbow_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include "samples.hpp"

#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;


TEST(utest_interface_elbow, elbow_method) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1.0, 1.0 }, { 1.1, 1.0 }, { 1.2, 1.4 }, { 10.0, 10.3 }, { 10.1, 10.2 }, { 10.2, 10.4 } }));

    pyclustering_package * result = elbow_method_ikpp(sample.get(), 1, sample->size, 1, RANDOM_STATE_CURRENT_TIME);
    ASSERT_EQ((std::size_t) ELBOW_PACKAGE_SIZE, result->size);

    delete result;

    result = elbow_method_irnd(sample.get(), 1, sample->size, 1, RANDOM_STATE_CURRENT_TIME);
    ASSERT_EQ((std::size_t) ELBOW_PACKAGE_SIZE, result->size);

    delete result;
}


TEST(utest_interface_elbow, elbow_method_simple3_ikpp) {
    auto sample_ptr = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    std::shared_ptr<pyclustering_package> sample = pack(*sample_ptr);

    pyclustering_package * result = elbow_method_ikpp(sample.get(), 1, 10, 1, RANDOM_STATE_CURRENT_TIME);
    ASSERT_EQ((std::size_t) ELBOW_PACKAGE_SIZE, result->size);

    delete result;
}


TEST(utest_interface_elbow, elbow_method_simple3_irnd) {
    auto sample_ptr = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    std::shared_ptr<pyclustering_package> sample = pack(*sample_ptr);

    pyclustering_package * result = elbow_method_irnd(sample.get(), 1, 10, 1, RANDOM_STATE_CURRENT_TIME);
    ASSERT_EQ((std::size_t) ELBOW_PACKAGE_SIZE, result->size);

    delete result;
}
