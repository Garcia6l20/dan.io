#include <udev++.hpp>

#include <iostream>

int main(void)
{
    auto ctx = udev::udev::instance();

    udev::enumerate enumerate{ctx};
    enumerate.match_subsystem("sound");
    enumerate.match_sysname("control*");

    auto devices = enumerate.get();
    for (auto const &device : devices)
    {
        using namespace std;

        cout << "Found sound device" << endl
             << "   Path: " << device.syspath() << endl
             << "   Node: " << device.devnode() << endl
             << "   Name: " << device.sysname() << endl
             << "      #: " << device.sysnum() << endl;
        cout << endl;

        if (auto parent = device.parent("usb", "usb_device"); parent.is_valid())
        {
            cout << ">> " << parent.subsystem() << " sound card" << endl
                 << "     Path: " << parent.syspath() << endl
                 << "     Node: " << parent.devnode() << endl
                 << "   Vendor: " << parent.sysattr("idVendor") << endl
                 << "  Product: " << parent.sysattr("idProduct") << endl
                 << "     Name: " << parent.sysname() << endl
                 << "        #: " << parent.sysnum() << endl;
            cout << endl;
        }
        if (auto parent = device.parent("pci"); parent.is_valid())
        {
            cout << ">> " << parent.subsystem() << " sound card" << endl
                 << "     Path: " << parent.syspath() << endl
                 << "   Vendor: " << parent.sysattr("vendor") << endl
                 << "  Product: " << parent.sysattr("device") << endl
                 << "     Name: " << parent.sysname() << endl
                 << "        #: " << parent.sysnum() << endl;
            cout << endl;
        }
    }

    return 0;
}