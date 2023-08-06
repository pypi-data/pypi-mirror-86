/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/container/adjacency_bit_matrix.hpp>

#include "utest-adjacency.hpp"

#include <cmath>
#include <utility>


using namespace pyclustering::container;


TEST(utest_adjacency_bit_matrix, create_delete) {
    adjacency_bit_matrix * matrix = new adjacency_bit_matrix(10);
    ASSERT_EQ(10U, matrix->size());

    for (size_t i = 0; i < matrix->size(); i++) {
        for (size_t j = i + 1; j < matrix->size(); j++) {
            ASSERT_FALSE(matrix->has_connection(i, j));
        }
    }

    delete matrix;
}


TEST(utest_adjacency_bit_matrix, null_size) {
    adjacency_bit_matrix matrix(0);
    ASSERT_EQ(0U, matrix.size());
}


TEST(utest_adjacency_bit_matrix, create_clear) {
    adjacency_bit_matrix matrix(10);
    ASSERT_EQ(10U, matrix.size());

    matrix.clear();
    ASSERT_EQ(0U, matrix.size());
}


TEST(utest_adjacency_bit_matrix, copy_matrix) {
    adjacency_bit_matrix matrix_first(20);
    adjacency_bit_matrix matrix_second(10);

    ASSERT_EQ(20U, matrix_first.size());
    ASSERT_EQ(10U, matrix_second.size());

    matrix_first.set_connection(1, 2);
    matrix_first.set_connection(2, 3);

    matrix_second.set_connection(2, 1);
    matrix_second.set_connection(4, 7);

    matrix_first = matrix_second;

    ASSERT_EQ(10U, matrix_first.size());
    ASSERT_EQ(10U, matrix_second.size());
    ASSERT_FALSE(matrix_first.has_connection(1, 2));
    ASSERT_FALSE(matrix_first.has_connection(2, 3));
    ASSERT_TRUE(matrix_first.has_connection(2, 1));
    ASSERT_TRUE(matrix_first.has_connection(4, 7));
}


TEST(utest_adjacency_bit_matrix, move_matrix) {
    adjacency_bit_matrix matrix_first(40);
    adjacency_bit_matrix matrix_second(40);

    ASSERT_TRUE(matrix_first.size() == matrix_second.size());
    ASSERT_EQ(40U, matrix_first.size());
    ASSERT_EQ(40U, matrix_second.size());

    for (size_t i = 0; i < matrix_first.size(); i++) {
        for (size_t j = i + 1; j < matrix_first.size(); j++) {
            if ((i % 2) == 0) {
                matrix_first.set_connection(i, j);
                ASSERT_TRUE(matrix_first.has_connection(i, j));
                ASSERT_FALSE(matrix_second.has_connection(i, j));
            }
            else {
                matrix_second.set_connection(i, j);
                ASSERT_FALSE(matrix_first.has_connection(i, j));
                ASSERT_TRUE(matrix_second.has_connection(i, j));
            }
        }
    }

    matrix_first = std::move(matrix_second);

    ASSERT_EQ(40U, matrix_first.size());
    ASSERT_EQ(0U, matrix_second.size());

    for (size_t i = 0; i < matrix_first.size(); i++) {
        for (size_t j = i + 1; j < matrix_first.size(); j++) {
            if ((i % 2) != 0) {
                ASSERT_TRUE(matrix_first.has_connection(i, j));
            }
        }
    }
}


TEST(utest_adjacency_bit_matrix, has_no_connection) {
    adjacency_bit_matrix matrix(30);
    template_has_no_connection(matrix);
}


TEST(utest_adjacency_bit_matrix, has_all_connection) {
    adjacency_bit_matrix matrix(25);
    template_has_all_connection(matrix);
}


TEST(utest_adjacency_bit_matrix, set_get_connection) {
    adjacency_bit_matrix matrix(100);
    template_set_connection(matrix);
}


TEST(utest_adjacency_bit_matrix, erase_get_connection) {
    adjacency_bit_matrix matrix(20);
    template_erase_connection(matrix);
}


TEST(utest_adjacency_bit_matrix, get_neighbors_sizes) {
    adjacency_bit_matrix matrix(20);
    template_get_neighbors_sizes(matrix);
}


TEST(utest_adjacency_bit_matrix, get_neighbors_indexes) {
    adjacency_bit_matrix matrix(20);
    template_get_neighbors_indexes(matrix);
}


TEST(utest_adjacency_bit_matrix, no_get_neighbors) {
    adjacency_bit_matrix matrix(41);
    template_no_get_neighbors(matrix);
}


TEST(utest_adjacency_bit_matrix, all_get_neighbors) {
    adjacency_bit_matrix matrix(9);
    template_all_get_neighbors(matrix);
}


TEST(utest_adjacency_bit_matrix, get_neighbors_after_erase) {
    adjacency_bit_matrix matrix(18);
    template_get_neighbors_after_erase(matrix);
}
