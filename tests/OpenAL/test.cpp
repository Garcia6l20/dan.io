#include <string_view>
#include <ranges>

namespace al
{

#include <AL/al.h>
#include <AL/alc.h>

class string_list_view : public std::ranges::view_interface<string_list_view> {
public:
    string_list_view(ALCenum e, ALCdevice* device = nullptr) noexcept: begin_{al::alcGetString(device, ALC_CAPTURE_DEVICE_SPECIFIER)} {}

    struct sentinel {};

    class iterator {
        friend class string_list_view;
    public:
        auto operator *() const {
            return current_;
        }
        void operator ++() {
            current_ =  std::string_view{current_.data() + current_.size() + 1};
        }
        bool operator ==(sentinel const&) const {
            return current_[0] == '\0';
        }

    private:
        iterator(std::string_view c) noexcept: current_{c} {}
        std::string_view current_;
    };

    auto begin() {
        return iterator{std::string_view{begin_}};
    }
    auto end() {
        return sentinel{};
    }
    operator bool() const {
        return begin_ != nullptr and begin_[0] != '\0';
    }
private:
    ALchar const* begin_;
};

} // namespace al

#include <cassert>
#include <iostream>

int main(void) {
    assert(al::alcIsExtensionPresent(NULL, "ALC_enumeration_EXT"));
    assert(al::alcIsExtensionPresent(NULL, "ALC_enumerate_all_EXT"));
    al::string_list_view device_list{ALC_CAPTURE_DEVICE_SPECIFIER};
    if (device_list) {
        std::cout << "available input devices:\n";
        for (auto dev: device_list) {
            std::cout << " ⇒ " << dev << '\n';
        }
    } else {
        std::cout << "no input device available !\n";
    }
    return 0;
}
