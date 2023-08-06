/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include <pyclustering/interface/pyclustering_package.hpp>

#include <cstring>
#include <memory>
#include <vector>


template <class TypeContainer>
static void template_pyclustering_package(const TypeContainer & container) {
    using container_data_t = typename TypeContainer::value_type;
    pyclustering_package * package = create_package(&container);

    ASSERT_EQ(container.size(), package->size);

    if (package->type != PYCLUSTERING_TYPE_LIST) {
        for (std::size_t index = 0; index < container.size(); index++) {
            ASSERT_EQ(container[index], package->at<container_data_t>(index));
        }
    }

    delete package;
}


TEST(utest_pyclustering, package_integer) {
    std::vector<int> container = { 1, 2, 3, 4, 5 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_double) {
    std::vector<double> container = { 1.0, 1.5, 2.0, 2.5, 3.0 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_unsigned) {
    std::vector<unsigned int> container = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_float) {
    std::vector<float> container = { -1.0, -0.5, 0.0, 0.5, 1.0 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_size_t) {
    std::vector<std::size_t> container = { 1, 2, 3, 4, 5, 6, 7 };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_empty) {
    std::vector<int> container = { };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_list) {
    std::vector<std::vector<int>> container = { { 1, 2 }, { 1, 2, 3, 4 } };
    template_pyclustering_package(container);
}


TEST(utest_pyclustering, package_pointer_list) {
    std::vector<std::vector<int> *> container;
    container.push_back(new std::vector<int>({ 1, 2, 3, 4, 5}));
    template_pyclustering_package(container);
    delete container[0];
}


TEST(utest_pyclustering, package_char_message) {
    const char * message = "message char";
    std::shared_ptr<pyclustering_package> package = std::shared_ptr<pyclustering_package>(create_package(message));

    ASSERT_NE(nullptr, package);
    ASSERT_EQ(std::strlen(message) + 1, package->size);
    ASSERT_EQ(PYCLUSTERING_TYPE_CHAR, package->type);
    ASSERT_STREQ(message, (const char *)package->data);
}


TEST(utest_pyclustering, package_empty_char_message) {
    const char * message = "";
    std::shared_ptr<pyclustering_package> package = std::shared_ptr<pyclustering_package>(create_package(message));

    ASSERT_NE(nullptr, package);
    ASSERT_EQ(std::strlen(message) + 1, package->size);
    ASSERT_EQ(PYCLUSTERING_TYPE_CHAR, package->type);
    ASSERT_STREQ(message, (const char *)package->data);
}


TEST(utest_pyclustering, package_wchar_message) {
    const wchar_t * message = L"message wchar_t";
    std::shared_ptr<pyclustering_package> package = std::shared_ptr<pyclustering_package>(create_package(message));

    ASSERT_NE(nullptr, package);
    ASSERT_EQ(std::wcslen(message) + 1, package->size);
    ASSERT_EQ(PYCLUSTERING_TYPE_WCHAR_T, package->type);
    ASSERT_EQ(0, std::wcscmp(message, (const wchar_t *)package->data));
}


TEST(utest_pyclustering, package_empty_wchar_message) {
    const wchar_t * message = L"";
    std::shared_ptr<pyclustering_package> package = std::shared_ptr<pyclustering_package>(create_package(message));

    ASSERT_NE(nullptr, package);
    ASSERT_EQ(std::wcslen(message) + 1, package->size);
    ASSERT_EQ(PYCLUSTERING_TYPE_WCHAR_T, package->type);
    ASSERT_EQ(0, std::wcscmp(message, (const wchar_t *)package->data));
}


TEST(utest_pyclustering, package_string_message) {
    std::string message = "message string";
    std::shared_ptr<pyclustering_package> package = std::shared_ptr<pyclustering_package>(create_package(message));

    ASSERT_NE(nullptr, package);
    ASSERT_EQ(message.size() + 1, package->size);
    ASSERT_EQ(PYCLUSTERING_TYPE_CHAR, package->type);
    ASSERT_STREQ(message.c_str(), (const char *)package->data);
}


TEST(utest_pyclustering, package_empty_string_message) {
    std::string message = "";
    std::shared_ptr<pyclustering_package> package = std::shared_ptr<pyclustering_package>(create_package(message));

    ASSERT_NE(nullptr, package);
    ASSERT_EQ(message.size() + 1, package->size);
    ASSERT_EQ(PYCLUSTERING_TYPE_CHAR, package->type);
    ASSERT_STREQ(message.c_str(), (const char *)package->data);
}


TEST(utest_pyclustering, package_wstring_message) {
    std::wstring message = L"message wstring";
    std::shared_ptr<pyclustering_package> package = std::shared_ptr<pyclustering_package>(create_package(message));

    ASSERT_NE(nullptr, package);
    ASSERT_EQ(message.size() + 1, package->size);
    ASSERT_EQ(PYCLUSTERING_TYPE_WCHAR_T, package->type);
    ASSERT_EQ(0, std::wcscmp(message.c_str(), (const wchar_t *)package->data));
}


TEST(utest_pyclustering, package_empty_wstring_message) {
    std::wstring message = L"";
    std::shared_ptr<pyclustering_package> package = std::shared_ptr<pyclustering_package>(create_package(message));

    ASSERT_NE(nullptr, package);
    ASSERT_EQ(message.size() + 1, package->size);
    ASSERT_EQ(PYCLUSTERING_TYPE_WCHAR_T, package->type);
    ASSERT_EQ(0, std::wcscmp(message.c_str(), (const wchar_t *)package->data));
}


template <class TypeContainer>
static void template_two_dimension_pyclustering_package(const TypeContainer & container) {
    using sub_container_t   = typename TypeContainer::value_type;
    using container_data_t  = typename sub_container_t::value_type;

    pyclustering_package * package = create_package(&container);

    ASSERT_EQ(container.size(), package->size);

    for (std::size_t i = 0; i < container.size(); i++) {
        pyclustering_package * sub_package = package->at<pyclustering_package *>(i);
        ASSERT_EQ(container[i].size(), sub_package->size);

        for (std::size_t j = 0; j < container[i].size(); j++) {
            ASSERT_EQ(container[i][j], package->at<container_data_t>(i, j));
        }
    }

    delete package;
}


TEST(utest_pyclustering, package_two_dimension_integer) {
    std::vector<std::vector<int>> container = { { 1, 2, 3 }, { 4, 5 }, { 6, 7, 8, 9 } };
    template_two_dimension_pyclustering_package(container);
}


TEST(utest_pyclustering, package_two_dimension_double) {
    std::vector<std::vector<double>> container = { { 1.0, 2.5, 3.0 }, { 4.5, 5.5 }, { 6.1, 7.2, 8.3, 9.4 } };
    template_two_dimension_pyclustering_package(container);
}


TEST(utest_pyclustering, package_two_dimension_empty) {
    std::vector<std::vector<long>> container = { { }, { 4, 5 }, { }, { 6 } };
    template_two_dimension_pyclustering_package(container);
}


template <class Container>
static void template_pack_unpack(const Container & container) {
    pyclustering_package * package = create_package(&container);

    Container unpack_container;
    package->extract(unpack_container);

    ASSERT_EQ(container, unpack_container);

    delete package;
}


TEST(utest_pyclustering, package_unpack_int) {
    template_pack_unpack(std::vector<int>({ 1, 2, 3, 4 }));
}


TEST(utest_pyclustering, package_unpack_long) {
    template_pack_unpack(std::vector<long>({ 1, 2, 3, 4, 5, 6 }));
}


TEST(utest_pyclustering, package_unpack_empty) {
    template_pack_unpack(std::vector<float>({ }));
}


TEST(utest_pyclustering, package_unpack_two_dimension) {
    template_pack_unpack(std::vector<std::vector<double>>({ { 1.2, 2.4 }, { 3.6, 4.8, 5.0 }, { 6.0 } }));
}