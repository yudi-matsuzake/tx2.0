#include "transaction.h"

const QString Transaction::JSON_TYPE = "transaction";

Transaction::Transaction()
{

}

Transaction::Transaction(const int &sender_id,
			 const int &receiver_id,
			 const QString &sender_method,
			 const QString &receiver_method,
			 const double &value){

	this->sender_id = sender_id;
	this->receiver_id = receiver_id;
	this->sender_method = sender_method;
	this->receiver_method = receiver_method;
	this->value = value;
}

bool Transaction::read(const QJsonObject &json){
	if (json["type"] != Transaction::JSON_TYPE)
		return false;

	this->sender_id = json["sender_id"].toInt();
	this->receiver_id = json["receiver_id"].toInt();
	this->value = json["value"].toDouble();
	this->sender_method = json["sender_method"].toString();
	this->receiver_method = json["receiver_method"].toString();
	return true;
}

bool Transaction::write(QJsonObject &json) const{


	json["type"] = Transaction::JSON_TYPE;
	json["sender_id"] = this->sender_id;
	json["receiver_id"] = this->receiver_id;
	json["value"] = this->value;
	json["sender_method"] = this->sender_method;
	json["receiver_method"] = this->receiver_method;
	return true;
}
