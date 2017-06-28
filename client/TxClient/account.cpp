#include "account.h"

const QString Account::JSON_TYPE = "accounts";

Account::Account(){

}

Account::Account(const int &id,
		const QString &client_cpf,
		const double &balance,
		const double &saving)
{

		this->id = id;
		this->client_cpf = client_cpf;
		this->balance = balance;
		this->saving = saving;
}

bool Account::read(const QJsonObject &json){
	if (json["type"] != Account::JSON_TYPE)
		return false;

	this->balance = json["balance"].toDouble();
	this->client_cpf = json["client_cpf"].toString();
	this->id = json["id"].toInt();
	this->saving = json["saving"].toDouble();

	return true;
}

bool Account::write(QJsonObject &json) const{

	json["type"] = Account::JSON_TYPE;

	json["balance"] = this->balance;
	json["client_cpf"] = this->client_cpf;
	json["id"] = this->id;
	json["saving"] = this->saving;

	return true;
}

int Account::getId() const
{
    return id;
}

void Account::setId(int value)
{
    id = value;
}

QString Account::getClient_cpf() const
{
    return client_cpf;
}

void Account::setClient_cpf(const QString &value)
{
    client_cpf = value;
}

double Account::getBalance() const
{
    return balance;
}

double Account::getSaving() const
{
    return saving;
}

void Account::setSaving(double value)
{
    saving = value;
}
