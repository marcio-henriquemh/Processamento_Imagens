from PyQt5.QtGui import *
import sys
from PIL import Image
from PyQt5.QtCore import Qt, QCoreApplication
import numpy as np
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QGridLayout, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QGridLayout, QWidget


class janela_filtro(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicializar a câmera
        self.cap = cv2.VideoCapture(0)
        self.timer = self.startTimer(1000//30)

        #

        # Criar um widget para exibir a imagem
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        # Criar um combobox para selecionar o filtro
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Sem filtro", "Filtro 1D", "Filtro 2D"])
         # Criar um combobox para selecionar o tamanho da matriz do filtro
        self.sizeComboBox = QComboBox()
        self.sizeComboBox.addItems(["3x3", "5x5", "7x7"])

        # Conectar o sinal de alteração de índice do combobox ao método de atualização da imagem
        self.sizeComboBox.currentIndexChanged.connect(self.atualizar_imagem)

        # Conectar o sinal de alteração de índice do combobox ao método de atualização da imagem
        self.comboBox.currentIndexChanged.connect(self.atualizar_imagem)

        # Adicionar o widget e o combobox ao layout da janela principal
        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.comboBox, 1, 0)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # Iniciar o loop de atualização de imagem
        self.atualizar_imagem()

    def atualizar_imagem(self):
        # Lê o próximo quadro da câmera

     
         ret, imagem = self.cap.read()
        # Converte o quadro para um formato compatível com Qt
        
         if  ret :
        
          linha, coluna, canal = imagem.shape
          bytes_em_linha = canal * coluna

          image = QImage(imagem.data, coluna, linha,bytes_em_linha, QImage.Format_Grayscale8)
          pixmap = QPixmap.fromImage(image)
            # Exibe a imagem no widget
          self.label.setPixmap(QPixmap.fromImage(image))
            # self.image_label.setPixmap(pixmap)


        # Aplica o filtro selecionado
         index = self.comboBox.currentIndex()
         
         # Aplica o filtro selecionado com o tamanho selecionado
         indice_valor = self.sizeComboBox.currentIndex()
         if index == 1:
                imagem = self.filtro_gaussiano_quadrado(imagem,indice_valor)
                img_conver=Image.fromarray(np.uint8(imagem))
                img_caminho="C:\\Users\\isado\\OneDrive\\Documentos\\aplicacao_processamento_de_imagens\\imagem_gaussiana.png"
                img_conver.save(img_caminho)
    
         elif index == 2:
                imagem = self.filtro_convolucao_gaussiana(imagem,indice_valor)
                img_conver=Image.fromarray(np.uint8(imagem))
                img_caminho="C:\\Users\\isado\\OneDrive\\Documentos\\aplicacao_processamento_de_imagens\\imagem_gaussiana_convolucao.png"
                img_conver.save(img_caminho)
         else:
             
              img_conver=Image.fromarray(np.uint8(imagem))
              img_caminho="C:\\Users\\isado\\OneDrive\\Documentos\\aplicacao_processamento_de_imagens\\imagem_original.png"
              img_conver.save(img_caminho)
        
                       
    




    def filtro_gaussiano_quadrado(self, imagem, indice_valor):
        # Aqui você pode colocar seu código para aplicar o filtro 1D
        tamanho_mascara = 2*indice_valor + 3
        mascara_sigma = 1.5
        mascara = np.zeros((tamanho_mascara, tamanho_mascara))
        for i in range(tamanho_mascara):
            for j in range(tamanho_mascara):
                mascara[i, j] = np.exp(-((i - tamanho_mascara//2)**2 + (j - tamanho_mascara//2)**2)/(2*mascara_sigma**2))
        mascara /= mascara.sum()

        # Aplica a convolução do mascara com a imagem
        filtrar_imagem = np.zeros_like(imagem)
        imagem_padded = cv2.copyMakeBorder(imagem, tamanho_mascara//2, tamanho_mascara//2, tamanho_mascara//2, tamanho_mascara//2, cv2.BORDER_CONSTANT)
        for i in range(imagem.shape[0]):
            for j in range(imagem.shape[1]):
                filtrar_imagem[i, j] = (imagem_padded[i:i+tamanho_mascara, j:j+tamanho_mascara]*mascara).sum()

        # Retorna a imagem filtrada
        return filtrar_imagem

        

    def filtro_convolucao_gaussiana(self, imagem, indice_valor):
        # Aqui você pode colocar seu código para aplicar o filtro 2D
        tamanho_mascara = 2*indice_valor + 3
        mascara = np.zeros((tamanho_mascara, tamanho_mascara))
        sigma = 1.0
        for x in range(-tamanho_mascara//2, tamanho_mascara//2+1):
            for y in range(-tamanho_mascara//2, tamanho_mascara//2+1):
                r = np.sqrt(x**2 + y**2)
                mascara[x+tamanho_mascara//2, y+tamanho_mascara//2] = (1.0 / (2.0 * np.pi * sigma**2)) * np.exp(-r**2 / (2.0 * sigma**2))
        mascara = mascara / mascara.sum()

    # Aplica a convolução
        imagem_convoluida = np.zeros_like(imagem)
        imagem_padded = cv2.copyMakeBorder(imagem, tamanho_mascara//2, tamanho_mascara//2, tamanho_mascara//2, tamanho_mascara//2, cv2.BORDER_CONSTANT)
        for i in range(tamanho_mascara//2, imagem_padded.shape[0]-tamanho_mascara//2):
            for j in range(tamanho_mascara//2, imagem_padded.shape[1]-tamanho_mascara//2):
                imagem_convoluida[i-tamanho_mascara//2, j-tamanho_mascara//2] = np.sum(mascara*imagem_padded[i-tamanho_mascara//2:i+tamanho_mascara//2+1, j-tamanho_mascara//2:j+tamanho_mascara//2+1])

        # Retorna a imagem filtrada
        return imagem_convoluida


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = janela_filtro()
    window.show()
    sys.exit(app.exec_())