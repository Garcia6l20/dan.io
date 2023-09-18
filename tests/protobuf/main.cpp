#include <addressbook.pb.h>

int main() {
    example::AddressBook book{};
    example::Person *me = book.add_people();
    me->set_id(42);
    me->set_name("Sylvain Garcia");
    me->set_email("garcia.6l20@gmail.com");
    std::cout << book.SerializeAsString() << '\n';

    google::protobuf::ShutdownProtobufLibrary();

    return 0;
}
