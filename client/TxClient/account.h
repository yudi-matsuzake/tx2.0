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
		const int& branch_id,
		const int& bank_id,
		const QString& bank_name,
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

	int getBranch_id() const;
	void setBranch_id(int value);

	int getBank_id() const;
	void setBank_id(int value);

	QString getBank_name() const;
	void setBank_name(const QString &value);

	double getBalance() const;

	double getSaving() const;
	void setSaving(double value);

private:
	static const QString JSON_TYPE;
	int id;
	QString client_cpf;
	int branch_id; 
	int bank_id;   
	QString bank_name; 
	double balance;   
	double saving;    
};

#endif // ACCOUNT_H
