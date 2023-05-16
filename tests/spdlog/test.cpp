#include <spdlog/spdlog.h>

int main(int argc, char** argv) {
    std::string_view who = "world";
    if (argc > 1) {
        who = argv[1];
    }
    spdlog::info("Hello {}", who);
    return 0;
}