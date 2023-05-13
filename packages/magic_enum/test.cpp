#include <magic_enum.hpp>

#include <iostream>

enum TestEnum {
    ONE,
    TWO
};

int main(void) {
    std::cout << magic_enum::enum_name(TestEnum::ONE) << '\n';
    return 0;
}
