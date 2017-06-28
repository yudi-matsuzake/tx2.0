#ifndef ACCOUNT_H
#define ACCOUNT_H
#include "client.h"
#include <QJsonObject>

/**
 * @brief Account model
 */

class Account
{
public:
	Account();
	Account(const int& id,
		const QString& client_cpf,
		const double& balance,
		const double& saving);

	/**
	 * @brief Function to atualize Account class based on a Json
	 * @param json Json object
	 * @return success or fail
	 */
	bool read(const QJsonObject& json);

	/**
	 * @brief Function to write into a Json the account class
	 * @param json Json object
	 * @return success or fail
	 */
	bool write(QJsonObject& json) const;
	
	int getId() const;
	void setId(int value);

	QString getClient_cpf() const;
	void setClient_cpf(const QString &value);

	double getBalance() const;

	double getSaving() const;
	void setSaving(double value);

private:
	static const QString JSON_TYPE;
	int id;
	QString client_cpf;
	double balance;   
	double saving;    
};

#endif // ACCOUNT_H
