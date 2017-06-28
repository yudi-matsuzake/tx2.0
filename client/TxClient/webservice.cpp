#include "webservice.hpp"

const QString WebServiceError::JSON_TYPE = "error";

WebServiceError::WebServiceError()
{}

WebServiceError::WebServiceError(const QString& msg, int code)
{
	this->msg = msg;
	this->code = code;
}

bool WebServiceError::read(const QJsonObject &json)
{
	if(json["type"] != WebServiceError::JSON_TYPE)
		return false;

	this->msg = json["msg"].toString();

	return true;
}

WebService::WebService(const std::string& ip, short port)
{
	this->ip = ip;
	this->port = port;
}

Account WebService::getAccount(int id)
{
	const std::string path = "/accounts/" + std::to_string(id);
	QJsonObject j = requestJson(path);

	Account a;
	if(!a.read(j))
		throw WebServiceError("Cannot read server response", -1);

	return a;
}

Client WebService::getClient(const QString& cpf)
{
	const std::string path = "/clients/" + cpf.toStdString();
	QJsonObject j = requestJson(path);

	Client c;
	if(!c.read(j))
		throw WebServiceError("Cannot read server response", -1);

	return c;
}

QString WebService::withdraw(const Withdraw &w)
{
	QJsonObject withdraw_request;
	w.write(withdraw_request);

	qDebug().noquote() << QJsonDocument(withdraw_request).toJson();
	const std::string path = "/withdraw";
	std::string j = jsonToStr(withdraw_request);
	QJsonObject response = requestJson(path, "PUT", j);

	return response["status"].toString();
}

QString WebService::deposit(const Deposit& d)
{
	QJsonObject deposit_request;
	d.write(deposit_request);

	const std::string path = "/deposit";
	std::string j = jsonToStr(deposit_request);
	QJsonObject response = requestJson(path, "PUT", j);

	return response["status"].toString();
}

QString WebService::transaction(const Transaction &t){
	QJsonObject transaction_request;
	t.write(transaction_request);

	qDebug().noquote() << QJsonDocument(transaction_request).toJson();
	const std::string path = "/transaction";
	std::string j = jsonToStr(transaction_request);
	QJsonObject response = requestJson(path, "POST", j);

	return response["status"].toString();
}

void WebService::setPort(short value)
{
	port = value;
}

std::string WebService::request(const std::string &path,
	const std::string &method,
	const std::string &data)
{
	curlpp::Cleanup cleanup;

	curlpp::Easy request;
	std::stringstream s;

	std::string url = this->ip
			+ ":"
			+ std::to_string(this->port)
			+ path;


	request.setOpt(new curlpp::options::CustomRequest(method));
	request.setOpt(new curlpp::options::Url(url));
	request.setOpt(new curlpp::options::WriteStream(&s));

	std::istringstream sstream(data);

	if(data.size()){
		request.setOpt(new curlpp::options::ReadStream(&sstream));
		request.setOpt(new curlpp::options::InfileSize(data.size()));
		request.setOpt(new curlpp::options::Upload(true));
	}

	request.perform();

	int code = curlpp::infos::ResponseCode::get(request);
	if(code >= 300){
		WebServiceError error;
		error.code = code;

		error.read(strToJson(s.str()));
		throw error;
	}

	return s.str();
}

QJsonObject WebService::strToJson(const std::string& s)
{
	QByteArray array(s.c_str(), s.size());
	return QJsonDocument::fromJson(array).object();
}

std::string WebService::jsonToStr(const QJsonObject& j)
{
	QJsonDocument doc(j);
	return QString(doc.toJson(QJsonDocument::Compact)).toStdString();
}

QJsonObject WebService::requestJson(
	const std::string& path,
	const std::string& method,
	const std::string& data)
{
	return strToJson(request(path, method, data));
}
