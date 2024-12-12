#ifndef ADMIN_H
#define ADMIN_H

#include "user.hpp"

// Clase concreta Admin hereda de User
class Admin : public User {
    int admin_level;
public:
    Admin(const std::string& uname, const std::string& mail, int level) 
        : User(uname, mail), admin_level(level) {}

    std::string getRole() const override {
        return "Admin";
    }
};

#endif // ADMIN_H
