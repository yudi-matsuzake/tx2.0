#ifndef WITHDRAW_H
#define WITHDRAW_H
#include <QString>
#include <QJsonObject>

/**
 * @brief Class to serialize the withdraw web-service request
 */
class Withdraw
{
public:
	Withdraw();
	Withdraw(const int& account_id, const double& value, const QString& withdraw_method);

	/**
	 * @brief Function to atualize Withdraw class based on a Json
	 * @param json Json object
	 * @return success or fail
	 */
	bool write(QJsonObject& json) const;

	/**
	 * @brief Function to write into a Json the withdraw class
	 * @param json Json object
	 * @return success or fail
	 */
	bool read(QJsonObject& json);
private:
	static const QString JSON_TYPE;
	int account_id;
	double value;
	QString withdraw_method;
};

#endif // WITHDRAW_H
