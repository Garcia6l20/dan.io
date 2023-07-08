#include <webview.h>

int main() {
    webview::webview wv{};
    wv.navigate("https://google.com");
    wv.run();
    return 0;
}

