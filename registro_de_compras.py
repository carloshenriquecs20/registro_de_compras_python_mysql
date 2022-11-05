from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="registro_de_compras"
)


def adicionar():
    linha1 = adiciona.cliente.text()
    linha2 = adiciona.produto.text()
    linha3 = adiciona.quantidade.text()
    linha4 = adiciona.preco.text()
    pagamento = ''
        
    if adiciona.aprazo.isChecked():
        pagamento = 'À prazo'
    else:
        pagamento = 'À vista'

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO historico (cliente,produto,quantidade,preço,pagamento) VALUES (%s, %s, %s, %s, %s)"
    dados = (str(linha1), str(linha2), str(linha3).replace(',', '.'), str(linha4).replace(',', '.'), pagamento)
    cursor.execute(comando_SQL, dados)
    banco.commit()
    linha1 = adiciona.cliente.text()
    linha2 = adiciona.produto.text()
    linha3 = adiciona.quantidade.text()
    linha4 = adiciona.preco.text()
    adiciona.close()


def modificar():
    linha = design.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute('SELECT id FROM historico')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]


    if modifica.cCliente.isChecked():
        cliente = modifica.lcliente.text()
        print(cliente)
        cursor.execute(f'UPDATE historico set cliente="{cliente}" where id={str(valor_id)}')
    
    if modifica.cProduto.isChecked():
        produto = modifica.lproduto.text()
        print(produto)
        cursor.execute(f'UPDATE historico set produto="{produto}" where id={str(valor_id)}')
   
    if modifica.cQuantidade.isChecked():
        quantidade = modifica.lquantidade.text()
        print(quantidade)
        cursor.execute(f'UPDATE historico set quantidade="{quantidade}" where id={str(valor_id)}')
    
    if modifica.cPreco.isChecked():
        preco = modifica.lpreco.text()
        print(preco)
        cursor.execute(f'UPDATE historico set preço="{preco}" where id={str(valor_id)}')

    banco.commit()
    modifica.close()

def baixar():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM historico"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("registro_de_compras.pdf")
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(200,800, "Histórico de Compras")
    pdf.setFont("Times-Bold", 14)

    pdf.drawString(50,750, "CLIENTE")
    pdf.drawString(140,750, "PRODUTO")
    pdf.drawString(235,750, "QUANTIDADE")
    pdf.drawString(355,750, "PREÇO")
    pdf.drawString(425,750, "PAGAMENTO")


    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(50,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(140,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(270,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(365,750 - y, str(dados_lidos[i][4]))
        pdf.drawString(450,750 - y, str(dados_lidos[i][4]))

    pdf.save()

def deletar():
    linha = design.tableWidget.currentRow()
    design.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute('SELECT id FROM historico')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute('DELETE FROM historico WHERE id='+ str(valor_id))



app = QtWidgets.QApplication([])
design = uic.loadUi('design.ui')
adiciona = uic.loadUi('adiciona.ui')
modifica = uic.loadUi('modifica.ui')

design.btn_adicionar.clicked.connect(adiciona.show)
design.btn_modificar.clicked.connect(modifica.show)
design.btn_deletar.clicked.connect(deletar)
design.btn_baixar.clicked.connect(baixar)
adiciona.enviar.clicked.connect(adicionar)
modifica.enviar2.clicked.connect(modificar)




cursor = banco.cursor()
comando_SQL = "SELECT * FROM historico"
cursor.execute(comando_SQL)
dados_lidos = cursor.fetchall()

design.tableWidget.setRowCount(len(dados_lidos))
design.tableWidget.setColumnCount(6)
for i in range(0, len(dados_lidos)):
    for j in range(0,6):
        design.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

design.show()
app.exec()