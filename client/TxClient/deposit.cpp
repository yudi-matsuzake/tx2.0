#include "deposit.h"

const QString Deposit::JSON_TYPE = "deposit";

Deposit::Deposit()
{
}

Deposit::Deposit(
	const int& account_id,
	const double& value,
	const QString& deposit_method){

	this->account_id = account_id;
	this->value = value;
	this->deposit_method = deposit_method;
}

bool Deposit::write(QJsonObject& json) const{
	json["type"] = Deposit::JSON_TYPE;
	json["account_id"] = this->account_id;
	json["deposit_method"] = this->deposit_method;
	json["value"] = this->value;

	return true;
}

bool Deposit::read(QJsonObject& json){
	if (json["type"] != Deposit::JSON_TYPE)
		return false;

	this->account_id = json["account_id"].toInt();
	this->deposit_method = json["deposit_method"].toString();
	this->value = json["value"].toDouble();

	return true;
}

