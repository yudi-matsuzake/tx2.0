#include "txclientview.h"
#include <QApplication>
#include <QDebug>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	TxClientView w;
	w.show();

	return a.exec();
}
