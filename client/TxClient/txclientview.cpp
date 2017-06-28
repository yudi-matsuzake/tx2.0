#include "txclientview.h"
#include "ui_txclientview.h"
#include <QInputDialog>
#include <QMessageBox>

TxClientView::TxClientView(QWidget *parent) :
	QMainWindow(parent),
	ui(new Ui::TxClientView)
{
	ui->setupUi(this);

	// Initialize web service
	this->web_service = new WebService("localhost", 5000);

	// Loop to verify user cpf input
	while(1){
		bool ok;

		this->user_cpf = QInputDialog::getText(
					this,
					"Welcome!",
					"Input your cpf:",
					QLineEdit::Normal,
					QString(),
					&ok);

		if(ok){
			if (this->user_cpf != ""){

				try {
					this->web_service->setPort(QInputDialog::getText(
								   this, "Welcome!",
								   "Input the branch id",
								   QLineEdit::Normal,
								   QString()).toInt()+8080);
					this->c = this	->web_service
							->getClient(this->user_cpf);

				}catch(WebServiceError& e){
					QMessageBox::critical(this, tr("Error"), e.msg);
					continue;
				}
				break;
			}else{
				QMessageBox::critical(
					this,
					tr("Error"),
					tr("Insert a valid username."));
			}
		}else{
			exit(EXIT_SUCCESS);
		}
	}

	this->initializeTable();
	this->initializeComboBoxes();
}

int append808(int x){
	return 8080 + x;
}

QTableWidgetItem* TxClientView::createTableItem(const QString &value)
{
	return new QTableWidgetItem(value);
}

QTableWidgetItem* TxClientView::createTableItem(int value)
{
	return createTableItem(QString::number(value));
}

QTableWidgetItem* TxClientView::createTableItem(double value)
{
	return createTableItem(QString::number(value));
}

void TxClientView::initializeTable(){

	ui->tableAccounts->setColumnCount(4);
	ui->tableAccounts->setRowCount(this->c.accounts.size());

	QStringList headers;

	ui->tableAccounts
		->horizontalHeader()
		->setSectionResizeMode(QHeaderView::Stretch);

	ui->tableAccounts
		->verticalHeader()
		->setVisible(false);

	ui->tableAccounts
		->setEditTriggers(QAbstractItemView::NoEditTriggers);

	headers <<	tr("Account")
		<<	tr("Branch ID")
		<<	tr("Bank")
		<<	tr("Balance")
		<<	tr("Saving");

	ui->tableAccounts
		->setHorizontalHeaderLabels(headers);

	int row = 0;
	for (Account& c : this->c.accounts){
		ui->tableAccounts->setItem(row, 0,
			createTableItem(c.getId()));

		ui->tableAccounts->setItem(row, 1,
			createTableItem(this->web_service->getPort()));

		ui->tableAccounts->setItem(row, 2,
			createTableItem(c.getBalance()));

		ui->tableAccounts->setItem(row, 3,
			createTableItem(c.getSaving()));

		row++;
	}
}

void TxClientView::initializeComboBoxes(){
	ui->comboDeposit->addItem("Saving");
	ui->comboDeposit->addItem("Current");
	ui->comboReceiver->addItem("Saving");
	ui->comboReceiver->addItem("Current");
	ui->comboWithdraw->addItem("Saving");
	ui->comboWithdraw->addItem("Current");
	ui->ComboSender->addItem("Saving");
	ui->ComboSender->addItem("Current");
}

void TxClientView::atualizeTable()
try{
	this->c = this->web_service->getClient(this->user_cpf);
	ui->tableAccounts->setRowCount(this->c.accounts.size());

	int row = 0;
	for (Account& c : this->c.accounts){
		ui->tableAccounts->setItem(row, 0,
			createTableItem(c.getId()));

		ui->tableAccounts->setItem(row, 1,
			createTableItem(this->web_service->getPort()));

		ui->tableAccounts->setItem(row, 2,
			createTableItem(c.getBalance()));

		ui->tableAccounts->setItem(row, 3,
			createTableItem(c.getSaving()));


		row++;
	}
}catch(WebServiceError& e){
	QMessageBox::critical(this, tr("Error"), e.msg);
}


TxClientView::~TxClientView()
{
	delete ui;
}


void TxClientView::on_btnDeposit_clicked()
try{
	int i = ui->tableAccounts
		->item(ui->tableAccounts->currentRow(), 0)
		->text().toInt();

	double d = ui->lineDeposit->text().toDouble();
	QString s = ui->comboDeposit->currentText().toLower();
	Deposit dep(i, d, s);

	QString r = this->web_service->deposit(dep);
	QMessageBox::information(this, "Result", r, QMessageBox::Ok);

	this->atualizeTable();

}catch(WebServiceError& e){
	QMessageBox::critical(this, tr("Error"), e.msg);
}

void TxClientView::on_btnWithdraw_clicked()
try{
	int i = ui->tableAccounts
		->item(ui->tableAccounts->currentRow(), 0)
		->text().toInt();

	double d = ui->lineWithdraw->text().toDouble();
	QString s = ui->comboWithdraw->currentText().toLower();
	Withdraw w(i, d, s);

	QString r = this->web_service->withdraw(w);
	QMessageBox::information(this, "Result", r, QMessageBox::Ok);
	this->atualizeTable();

}catch(WebServiceError& e){
	QMessageBox::critical(this, tr("Error"), e.msg);
}

void TxClientView::on_btnTransaction_clicked()
try{
	int s_id = ui
		->tableAccounts
		->item(ui->tableAccounts->currentRow(), 0)
		->text().toInt();

	int r_id = ui->lineReceiver->text().toInt();
	QString s_m = ui->ComboSender->currentText().toLower();
	QString r_m = ui->comboReceiver->currentText().toLower();
	double v = ui->lineTransaction->text().toDouble();
	int b_id = ui->lineBranch->text().toInt();
	Transaction t(s_id, r_id, s_m, r_m, v, b_id);

	QString r = this->web_service->transaction(t);
	QMessageBox::information(this, "Result", r, QMessageBox::Ok);
	this->atualizeTable();
}catch(WebServiceError& e){
	QMessageBox::critical(this, tr("Error"), e.msg);
}

void TxClientView::on_btnRefresh_clicked()
try{
	this->c = this->web_service->getClient(this->user_cpf);
	this->atualizeTable();
}catch(WebServiceError& e){
	QMessageBox::critical(this, tr("Error"), e.msg);
}
