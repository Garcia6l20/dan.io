#include <QApplication>
#include <QPushButton>

int main(int argc, char **argv) {
    QApplication app{argc, argv};
    QPushButton btn{"Click me !"};
    QApplication::connect(&btn, &QPushButton::clicked, [&] {
        app.quit();
    });
    btn.show();
    return app.exec();
}
