#include "account.h"

const QString Account::JSON_TYPE = "accounts";

Account::Account(){

}

Account::Account(const int &id,
		const QString &client_cpf,
		const int &branch_id,
		const int &bank_id,
		const QString &bank_name,
		const double &balance,
		const double &saving)
{

		this->id = id;
		this->client_cpf = client_cpf;
		this->branch_id = branch_id;
		this->bank_name = bank_name;
		this->bank_id = bank_id;
		this->balance = balance;
		this->saving = saving;
}

bool Account::read(const QJsonObject &json){
	if (json["type"] != Account::JSON_TYPE)
		return false;

	this->balance = json["balance"].toDouble();
	this->bank_id = json["bank_id"].toInt();
	this->bank_name = json["bank_name"].toString();
	this->branch_id = json["branch_id"].toInt();
	this->client_cpf = json["client_cpf"].toString();
	this->id = json["id"].toInt();
	this->saving = json["saving"].toDouble();

	return true;
}

bool Account::write(QJsonObject &json) const{

	json["type"] = Account::JSON_TYPE;

	json["balance"] = this->balance;
	json["bank_id"] = this->bank_id;
	json["bank_name"] = this->bank_name;
	json["branch_id"] = this->branch_id;
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

int Account::getBranch_id() const
{
    return branch_id;
}

void Account::setBranch_id(int value)
{
    branch_id = value;
}

int Account::getBank_id() const
{
    return bank_id;
}

void Account::setBank_id(int value)
{
    bank_id = value;
}

QString Account::getBank_name() const
{
    return bank_name;
}

void Account::setBank_name(const QString &value)
{
    bank_name = value;
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
