#ifndef USER_H
#define USER_H

#include <string>

// Clase abstracta User
class User {
protected:
    std::string username;
    std::string email;
public:
    User(const std::string& uname, const std::string& mail) : username(uname), email(mail) {}
    virtual std::string getRole() const = 0;  // Método abstracto
};

#endif
