#include "withdraw.h"

const QString Withdraw::JSON_TYPE = "withdraw";

Withdraw::Withdraw()
{

}

Withdraw::Withdraw(const int& account_id, const double& value, const QString& withdraw_method){
	this->account_id = account_id;
	this->value = value;
	this->withdraw_method = withdraw_method;
}

bool Withdraw::read(QJsonObject &json){
	if (json["type"] != Withdraw::JSON_TYPE)
		return false;

	this->account_id = json["account_id"].toInt();
	this->value = json["value"].toDouble();
	this->withdraw_method = json["withdraw_method"].toString();
	return true;
}

bool Withdraw::write(QJsonObject &json) const{

	json["type"] = Withdraw::JSON_TYPE;
	json["account_id"] = this->account_id;
	json["value"] = this->value;
	json["withdraw_method"] = this->withdraw_method;
	return true;
}
