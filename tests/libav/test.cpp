extern "C" {
    #include <libavdevice/avdevice.h>
}

int main(void) {
    avdevice_register_all();
    return 0;
}
