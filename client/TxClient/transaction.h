#ifndef TRANSACTION_H
#define TRANSACTION_H
#include <QString>
#include <QJsonObject>

/**
 * @brief Class to serialize the transaction web-service request
 */
class Transaction
{
public:
	Transaction();
	Transaction(const int& sender_id,
		    const int& receiver_id,
		    const QString& sender_method,
		    const QString& receiver_method,
		    const double& value,
		    const int &receiver_branch);

	/**
	 * @brief Function to atualize Transaction class based on a Json
	 * @param json Json object
	 * @return success or fail
	 */
	bool read(const QJsonObject& json);

	/**
	 * @brief Function to write into a Json the transaction class
	 * @param json Json object
	 * @return success or fail
	 */
	bool write(QJsonObject& json) const;

private:
	static const QString JSON_TYPE;
	int sender_id;
	int receiver_id;
	int receiver_branch;
	QString sender_method;
	QString receiver_method;
	double value;
};

#endif // TRANSACTION_H
