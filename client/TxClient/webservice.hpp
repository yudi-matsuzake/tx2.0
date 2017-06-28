#ifndef WEBSERVICE_HPP
#define WEBSERVICE_HPP

#include <sstream>

#include "account.h"
#include "client.h"
#include "deposit.h"
#include "withdraw.h"
#include "transaction.h"

#include <curlpp/cURLpp.hpp>
#include <curlpp/Easy.hpp>
#include <curlpp/Options.hpp>
#include <curlpp/Infos.hpp>

#include <QJsonDocument>
#include <QJsonObject>
#include <QDebug>

class WebServiceError
{
public:
	WebServiceError();
	WebServiceError(const QString& msg, int code);

	QString msg;
	int code;

	bool read(const QJsonObject& json);

private:
	static const QString JSON_TYPE;
	QJsonObject strToJson(const std::string& s);
};

/** This class is a abstraction of the webserver.
 * It's functions is to provide a facility for networking and
 * serialization and deserialization.
 */
class WebService
{
public:
	WebService(const std::string& ip, short port);

	/**
	 * @brief Fetch the account object with number `id` in the server,
	 *        and deserialize the object Account returning it
	 * @param id is the number of the account in the server
	 * @return An account object with id `id` that represents
	 *         the object in the server
	 */
	Account getAccount(int id);

	/**
	 * @brief Fetch the client object with cpf `cpf` in the server,
	 *        and deserialize the object Account returning it
	 * @param id is the number of the account in the server
	 * @return An account object with id `id` that represents
	 *         the object in the server
	 */
	Client getClient(const QString& cpf);

	/**
	 * @brief Realize the withdraw method in the server
	 * @param w The withdraw object that represents the method
	 * @return A status message from the server
	 */
	QString withdraw(const Withdraw& w);

	/**
	 * @brief Realize the deposit method in the server based
	 *        on object Deposit `d`
	 * @param d The deposit object that represents the method
	 * @return A status message from the server
	 */
	QString deposit(const Deposit& d);

	/**
	 * @brief Realize the transaction to another user based on oject Transaction 't'
	 * @param t The transaction oject that represents the method
	 * @return  A status message from the server.
	 */

	QString transaction(const Transaction& t);

	void setPort(short value);
	
private:
	std::string ip;
	short port;

	QJsonObject strToJson(const std::string& s);
	std::string jsonToStr(const QJsonObject& j);

	std::string request(
		const std::string& url,
		const std::string& method = "GET",
		const std::string& data = std::string());

	QJsonObject requestJson(
		const std::string& path,
		const std::string& method = "GET",
		const std::string& data = std::string());
};

#endif // WEBSERVICE_HPP
