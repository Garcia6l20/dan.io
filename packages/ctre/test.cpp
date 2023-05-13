#include <ctre.hpp>
#include <iostream>

static inline constexpr auto pattern = ctll::fixed_string{R"(hello \w+)"};

int main(int argc, char **argv) {
    if (argc < 2) {
        return -1;
    }
    if (ctre::re<pattern>().match(argv[1])) {
        std::cout << "match\n";
        return 1;
    }
    std::cout << "no match\n";
    return 0;
}
