#ifndef CLIENT_H
#define CLIENT_H
#include "account.h"
#include <QString>
#include <QList>

class Account;

class Client
{
public:
	Client();
	Client(const QString& cpf, const QString& name);

	/**
	 * @brief Function to atualize Client class based on a Json
	 * @param json Json object
	 * @return success or fail
	 */
	bool read(const QJsonObject& json);

	/**
	 * @brief Function to write into a Json the client class
	 * @param json Json object
	 * @return success or fail
	 */
	bool write(QJsonObject& json) const;
	QList<Account> accounts;

	QString getCpf() const;
	void setCpf(const QString &value);

	QString getName() const;
	void setName(const QString &value);

private:
	static const QString JSON_TYPE;
	QString cpf;
	QString name;
};

#endif // CLIENT_H
