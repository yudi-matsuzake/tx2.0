#ifndef DEPOSIT_H
#define DEPOSIT_H
#include <QString>
#include <QJsonObject>

/**
 * @brief Class to serialize the deposit web-service request
 */

class Deposit
{
public:
	Deposit();
	Deposit(const int& account_id, const double& value, const QString& deposit_method);

	/**
	 * @brief Function to atualize Deposit class based on a Json
	 * @param json Json object
	 * @return success or fail
	 */
	bool write(QJsonObject& json) const;

	/**
	 * @brief Function to write into a Json the deposit class
	 * @param json Json object
	 * @return success or fail
	 */
	bool read(QJsonObject& json);

private:
	static const QString JSON_TYPE;
	int account_id;
	double value;
	QString deposit_method;
};

#endif // DEPOSIT_H
