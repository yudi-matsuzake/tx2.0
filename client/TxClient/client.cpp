#include "client.h"
#include <QJsonArray>

const QString Client::JSON_TYPE = "clients";

Client::Client(){

}

Client::Client(const QString& cpf, const QString& name)
{
	this->cpf = cpf;
	this->name = name;
}

bool Client::read(const QJsonObject &json){

	if(json["type"] != Client::JSON_TYPE){
		return false;
	}

	this->cpf = json["cpf"].toString();
	this->name = json["name"].toString();

	QJsonArray JArray;
	QJsonObject JAccount;
	Account account(0, "", 0, 0);
	JArray = json["accounts"].toArray();

	for(int i = 0; i < JArray.size(); i++){
		JAccount = JArray[i].toObject();

		if(!account.read(JAccount)){
			return false;
		}

		this->accounts.append(account);
	}

	return true;
}

bool Client::write(QJsonObject &json) const{
	json["type"] = Client::JSON_TYPE;
	json["cpf"] = this->cpf;
	json["name"] = this->name;

	QJsonObject JAccount;
	QJsonArray JArray;
	foreach (Account a, accounts) {
		if (!a.write(JAccount)){
			return false;
		}

		JArray.append(JAccount);
	}

	json["accounts"] = JArray;
	return true;
}

QString Client::getCpf() const
{
    return cpf;
}

void Client::setCpf(const QString &value)
{
    cpf = value;
}

QString Client::getName() const
{
    return name;
}

void Client::setName(const QString &value)
{
    name = value;
}
