#ifndef TXCLIENTVIEW_H
#define TXCLIENTVIEW_H

#include <QMainWindow>
#include <QList>
#include <QTableWidgetItem>
#include "webservice.hpp"

namespace Ui {
class TxClientView;
}

class TxClientView : public QMainWindow
{
	Q_OBJECT

public:
	explicit TxClientView(QWidget *parent = 0);
	~TxClientView();

private slots:
	void on_btnDeposit_clicked();

	void on_btnWithdraw_clicked();

	void on_btnTransaction_clicked();

	void on_btnRefresh_clicked();

private:
	/**
	 * @brief Function to initialize table
	 */
	void initializeTable();

	/**
	 * @brief Function to initialize combo boxes
	 */

	void initializeComboBoxes();

	/**
	 * @brief Function to atualize table
	 */

	void atualizeTable();
	Ui::TxClientView *ui;
	QString user_cpf;
	WebService* web_service;
	Client c;

	static QTableWidgetItem* createTableItem(const QString& value);
	static QTableWidgetItem* createTableItem(int value);
	static QTableWidgetItem* createTableItem(double value);

};

#endif // TXCLIENTVIEW_H
