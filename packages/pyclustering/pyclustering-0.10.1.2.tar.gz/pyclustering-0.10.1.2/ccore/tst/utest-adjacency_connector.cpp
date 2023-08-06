/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <cmath>
#include <algorithm>

#include <pyclustering/container/adjacency_connector.hpp>
#include <pyclustering/container/adjacency_bit_matrix.hpp>
#include <pyclustering/container/adjacency_list.hpp>
#include <pyclustering/container/adjacency_matrix.hpp>
#include <pyclustering/container/adjacency_weight_list.hpp>


using namespace pyclustering::container;


enum class grid_t { GRID_FOUR, GRID_EIGHT };


template <typename TypeCollection>
static void template_grid_connections(const grid_t p_connections, const size_t p_elements, const size_t p_width = 0, const size_t p_height = 0) {
    TypeCollection collection(p_elements);

    adjacency_connector<TypeCollection> connector;
    switch (p_connections) {
        case grid_t::GRID_FOUR:
            if ((p_width != 0U) && (p_height != 0U)) {
                connector.create_grid_four_connections(p_width, p_height, collection);
            }
            else {
                connector.create_grid_four_connections(collection);
            }

            break;

        case grid_t::GRID_EIGHT:
            if ((p_width != 0U) && (p_height != 0U)) {
                connector.create_grid_eight_connections(p_width, p_height, collection);
            }
            else {
                connector.create_grid_eight_connections(collection);
            }

            break;
    }

    int base = (int) p_width;
    if (base == 0) {
        base = (int) std::sqrt(p_elements);
    }

    for (int index = 0; index < (int) collection.size(); index++) {
        const int upper_index = index - base;
        const int upper_left_index = index - base - 1;
        const int upper_right_index = index - base + 1;

        const int lower_index = index + base;
        const int lower_left_index = index + base - 1;
        const int lower_right_index = index + base + 1;

        const int left_index = index - 1;
        const int right_index = index + 1;

        const int node_row_index = (int) std::ceil(index / base);
        const int upper_row_index = node_row_index - 1;
        const int lower_row_index = node_row_index + 1;

        std::vector<size_t> neighbors;
        collection.get_neighbors(index, neighbors);

        if (upper_index >= 0) {
            ASSERT_EQ(true, collection.has_connection(index, upper_index));
            ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) upper_index));
        }

        if (lower_index < (int) collection.size()) {
            ASSERT_EQ(true, collection.has_connection(index, lower_index));
            ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) lower_index));
        }

        if ((left_index >= 0) && (std::ceil(left_index / base) == node_row_index)) {
            ASSERT_TRUE(collection.has_connection(index, left_index));
            ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) left_index));
        }

        if ((right_index < (int) collection.size()) && (std::ceil(right_index / base) == node_row_index)) {
            ASSERT_TRUE(collection.has_connection(index, right_index));
            ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) right_index));
        }

        if (p_connections == grid_t::GRID_EIGHT) {
            if ((upper_left_index >= 0) && (std::floor(upper_left_index / base) == upper_row_index)) {
                ASSERT_TRUE(collection.has_connection(index, upper_left_index));
                ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) upper_left_index));
            }

            if ((upper_right_index >= 0) && (std::floor(upper_right_index / base) == upper_row_index)) {
                ASSERT_TRUE(collection.has_connection(index, upper_right_index));
                ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) upper_right_index));
            }

            if ((lower_left_index < (int) collection.size()) && (std::floor(lower_left_index / base) == lower_row_index)) {
                ASSERT_TRUE(collection.has_connection(index, lower_left_index));
                ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) lower_left_index));
            }

            if ((lower_right_index < (int) collection.size()) && (std::floor(lower_right_index / base) == lower_row_index)) {
                ASSERT_TRUE(collection.has_connection(index, lower_right_index));
                ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) lower_right_index));
            }

            for (int j = 0; j < (int) collection.size(); j++) {
                if ((j != index) &&
                    (j != upper_index) && (j != lower_index) && (j != left_index) && (j != right_index) &&
                    (j != upper_left_index) && (j != upper_right_index) && (j != lower_left_index) && (j != lower_right_index)) {

                    ASSERT_FALSE(collection.has_connection(index, j));
                    ASSERT_TRUE(neighbors.cend() == std::find(neighbors.cbegin(), neighbors.cend(), (size_t) j));
                }
            }
        }
        else {
            for (int j = 0; j < (int) collection.size(); j++) {
                if ((j != index) && (j != upper_index) && (j != lower_index) && (j != left_index) && (j != right_index)) {
                    ASSERT_FALSE(collection.has_connection(index, j));
                    ASSERT_TRUE(neighbors.cend() == std::find(neighbors.cbegin(), neighbors.cend(), (size_t) j));
                }
            }
        }
    }
}


TEST(utest_adjacency_connector, grid_four_bit_matrix_25) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_FOUR, 25);
}

TEST(utest_adjacency_connector, grid_four_list_25) {
    template_grid_connections<adjacency_list>(grid_t::GRID_FOUR, 25);
}

TEST(utest_adjacency_connector, grid_four_matrix_25) {
    template_grid_connections<adjacency_matrix>(grid_t::GRID_FOUR, 25);
}

TEST(utest_adjacency_connector, grid_four_list_weight_25) {
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_FOUR, 25);
}

TEST(utest_adjacency_connector, grid_four_36) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_FOUR, 36);
    template_grid_connections<adjacency_list>(grid_t::GRID_FOUR, 36);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_FOUR, 36);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_FOUR, 36);
}

TEST(utest_adjacency_connector, grid_four_49) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_FOUR, 49);
    template_grid_connections<adjacency_list>(grid_t::GRID_FOUR, 49);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_FOUR, 49);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_FOUR, 49);
}

TEST(utest_adjacency_connector, grid_eight_bit_matrix_16) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_EIGHT, 16);
}

TEST(utest_adjacency_connector, grid_eight_list_16) {
    template_grid_connections<adjacency_list>(grid_t::GRID_EIGHT, 16);
}

TEST(utest_adjacency_connector, grid_eight_matrix_16) {
    template_grid_connections<adjacency_matrix>(grid_t::GRID_EIGHT, 16);
}

TEST(utest_adjacency_connector, grid_eight_list_weight_16) {
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_EIGHT, 16);
}

TEST(utest_adjacency_connector, grid_eight_25) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_EIGHT, 25);
    template_grid_connections<adjacency_list>(grid_t::GRID_EIGHT, 25);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_EIGHT, 25);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_EIGHT, 25);
}

TEST(utest_adjacency_connector, grid_four_rectangle_10) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_FOUR, 10, 5, 2);
    template_grid_connections<adjacency_list>(grid_t::GRID_FOUR, 10, 5, 2);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_FOUR, 10, 5, 2);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_FOUR, 10, 5, 2);
}

TEST(utest_adjacency_connector, grid_eight_rectangle_10) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_EIGHT, 10, 5, 2);
    template_grid_connections<adjacency_list>(grid_t::GRID_EIGHT, 10, 5, 2);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_EIGHT, 10, 5, 2);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_EIGHT, 10, 5, 2);
}

TEST(utest_adjacency_connector, grid_four_rectangle_50) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_FOUR, 50, 5, 10);
    template_grid_connections<adjacency_list>(grid_t::GRID_FOUR, 50, 5, 10);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_FOUR, 50, 5, 10);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_FOUR, 50, 5, 10);
}

TEST(utest_adjacency_connector, grid_eight_rectangle_50) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_EIGHT, 50, 5, 10);
    template_grid_connections<adjacency_list>(grid_t::GRID_EIGHT, 50, 5, 10);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_EIGHT, 50, 5, 10);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_EIGHT, 50, 5, 10);
}

TEST(utest_adjacency_connector, grid_four_rectangle_as_list) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_FOUR, 15, 1, 15);
    template_grid_connections<adjacency_list>(grid_t::GRID_FOUR, 15, 1, 15);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_FOUR, 15, 1, 15);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_FOUR, 15, 1, 15);

    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_FOUR, 7, 7, 1);
    template_grid_connections<adjacency_list>(grid_t::GRID_FOUR, 7, 7, 1);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_FOUR, 7, 7, 1);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_FOUR, 7, 7, 1);
}

TEST(utest_adjacency_connector, grid_eight_rectangle_as_list) {
    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_EIGHT, 15, 1, 15);
    template_grid_connections<adjacency_list>(grid_t::GRID_EIGHT, 15, 1, 15);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_EIGHT, 15, 1, 15);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_EIGHT, 15, 1, 15);

    template_grid_connections<adjacency_bit_matrix>(grid_t::GRID_EIGHT, 7, 7, 1);
    template_grid_connections<adjacency_list>(grid_t::GRID_EIGHT, 7, 7, 1);
    template_grid_connections<adjacency_matrix>(grid_t::GRID_EIGHT, 7, 7, 1);
    template_grid_connections<adjacency_weight_list>(grid_t::GRID_EIGHT, 7, 7, 1);
}


template <typename TypeCollection>
static void template_list_connection(const size_t p_elements) {
    TypeCollection collection(p_elements);
    adjacency_connector<TypeCollection> connector;

    connector.create_list_bidir_connections(collection);

    for (size_t i = 0; i < p_elements; i++) {
        std::vector<size_t> neighbors;
        collection.get_neighbors(i, neighbors);

        if (i > 0) {
            ASSERT_TRUE(collection.has_connection(i, i - 1));
            ASSERT_TRUE(collection.has_connection(i - 1, i));

            ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) i - 1));
        }

        if (i < (p_elements - 1)) {
            ASSERT_TRUE(collection.has_connection(i, i + 1));
            ASSERT_TRUE(collection.has_connection(i + 1, i));

            ASSERT_TRUE(neighbors.cend() != std::find(neighbors.cbegin(), neighbors.cend(), (size_t) i + 1));
        }

        for (std::size_t j = 0; j < p_elements; j++) {
            if ((i != j) && (j != (i + 1)) && (j != (i - 1))) {
                ASSERT_FALSE(collection.has_connection(i, j));
                ASSERT_TRUE(neighbors.cend() == std::find(neighbors.cbegin(), neighbors.cend(), (size_t) j));
            }
        }
    }
}

TEST(utest_adjacency_connector, bidir_10) {
    template_list_connection<adjacency_bit_matrix>(10);
    template_list_connection<adjacency_list>(10);
    template_list_connection<adjacency_matrix>(10);
    template_list_connection<adjacency_weight_list>(10);
}

TEST(utest_adjacency_connector, bidir_15) {
    template_list_connection<adjacency_bit_matrix>(15);
    template_list_connection<adjacency_list>(15);
    template_list_connection<adjacency_matrix>(15);
    template_list_connection<adjacency_weight_list>(15);
}


template <typename TypeCollection>
static void template_all_to_all_connections(const size_t p_elements) {
    TypeCollection collection(p_elements);
    adjacency_connector<TypeCollection> connector;

    connector.create_all_to_all_connections(collection);

    for (size_t i = 0; i < collection.size(); i++) {
        ASSERT_FALSE(collection.has_connection(i, i));

        for (size_t j = i + 1; j < collection.size(); j++) {
            ASSERT_TRUE(collection.has_connection(i, j));
            ASSERT_TRUE(collection.has_connection(j, i));
        }
    }
}


TEST(utest_adjacency_connector, all_to_all_25) {
    template_all_to_all_connections<adjacency_bit_matrix>(25);
    template_all_to_all_connections<adjacency_list>(25);
    template_all_to_all_connections<adjacency_matrix>(25);
    template_all_to_all_connections<adjacency_weight_list>(25);
}


template <typename TypeCollection>
static void template_none_connections(const size_t p_elements) {
    TypeCollection collection(p_elements);
    adjacency_connector<TypeCollection> connector;

    /* create all-to-all connections and then set none */
    connector.create_all_to_all_connections(collection);
    connector.create_none_connections(collection);

    for (size_t i = 0; i < collection.size(); i++) {
        ASSERT_FALSE(collection.has_connection(i, i));

        for (size_t j = i; j < collection.size(); j++) {
            ASSERT_FALSE(collection.has_connection(i, j));
            ASSERT_FALSE(collection.has_connection(j, i));
        }
    }
}


TEST(utest_adjacency_connector, none_10) {
    template_none_connections<adjacency_bit_matrix>(10U);
    template_none_connections<adjacency_list>(10U);
    template_none_connections<adjacency_matrix>(10U);
    template_none_connections<adjacency_weight_list>(10U);
}
