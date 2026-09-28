import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os

class RasterbatorEpsonL3250:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Póster Mosaico - Especial Epson L3250")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # Definições A4 a 300 DPI (Resolução de impressão ideal)
        self.A4_LARGURA = 2480
        self.A4_ALTURA = 3508
        
        # Margens físicas da Epson L3250 em pixels (300 DPI)
        self.M_ESQ = 35
        self.M_DIR = 35
        self.M_TOPO = 35
        self.M_BASE = 106
        
        # Área útil real onde a tinta realmente sai
        self.AREA_UTIL_LARGURA = self.A4_LARGURA - (self.M_ESQ + self.M_DIR)
        self.AREA_UTIL_ALTURA = self.A4_ALTURA - (self.M_TOPO + self.M_BASE)
        
        # Inicialização das variáveis de controle
        self.caminho_imagem = None
        self.linhas_finais = 1
        
        self.criar_interface()

    def criar_interface(self):
        lbl_titulo = tk.Label(self.root, text="Rasterbator com Margem de Segurança", font=("Arial", 14, "bold"), fg="#1a73e8", pady=10)
        lbl_titulo.pack()
        
        lbl_sub = tk.Label(self.root, text="Divide imagens em várias folhas A4 sem deformar ou cortar nas emendas.", font=("Arial", 9, "italic"), fg="gray")
        lbl_sub.pack(pady=(0, 15))

        # 1. Seleção de Ficheiro
        frame_arquivo = tk.LabelFrame(self.root, text=" 1. Selecione a Imagem do Póster ", padx=10, pady=10)
        frame_arquivo.pack(fill="x", padx=20, pady=5)
        
        self.btn_carregar = tk.Button(frame_arquivo, text="Procurar Imagem...", command=self.carregar_imagem, bg="#4285F4", fg="white", font=("Arial", 9, "bold"))
        self.btn_carregar.pack(side="left", padx=5)
        
        self.lbl_status = tk.Label(frame_arquivo, text="Nenhum ficheiro carregado", fg="red", wraplength=250, justify="left")
        self.lbl_status.pack(side="left", padx=10)

        # 2. Configuração do Mosaico (Tiling)
        frame_config = tk.LabelFrame(self.root, text=" 2. Configuração do Tamanho (Mosaico) ", padx=10, pady=10)
        frame_config.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame_config, text="Orientação do A4:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_orientacao = ttk.Combobox(frame_config, values=["Vertical (Portrait)", "Horizontal (Landscape)"], state="readonly", width=22)
        self.combo_orientacao.current(0)
        self.combo_orientacao.grid(row=0, column=1, pady=5)
        self.combo_orientacao.bind("<<ComboboxSelected>>", self.atualizar_proporcoes)
        
        tk.Label(frame_config, text="Número de Colunas (Largura):").grid(row=1, column=0, sticky="w", pady=5)
        self.spin_colunas = tk.Spinbox(frame_config, from_=1, to=20, width=5, command=self.atualizar_proporcoes)
        self.spin_colunas.bind("<KeyRelease>", self.atualizar_proporcoes)
        self.spin_colunas.grid(row=1, column=1, sticky="w", pady=5)
        
        self.lbl_dimensoes_finais = tk.Label(frame_config, text="Tamanho estimado: Selecione uma imagem", fg="purple", font=("Arial", 9, "bold"))
        self.lbl_dimensoes_finais.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")

        # 3. Ação Final
        self.btn_gerar = tk.Button(self.root, text="3. Gerar PDF Único para Impressão", command=self.gerar_mosaico, state=tk.DISABLED, bg="#0F9D58", fg="white", font=("Arial", 11, "bold"), pady=8)
        self.btn_gerar.pack(fill="x", padx=20, pady=20)

    def carregar_imagem(self):
        self.caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png *.tiff *.bmp")])
        if self.caminho_imagem:
            nome = os.path.basename(self.caminho_imagem)
            self.lbl_status.config(text=f"Pronto: {nome}", fg="green")
            self.btn_gerar.config(state=tk.NORMAL)
            self.atualizar_proporcoes()

    def obter_dados_painel(self):
        if self.combo_orientacao.current() == 0:  # Vertical
            largura_pagina, altura_pagina = self.A4_LARGURA, self.A4_ALTURA
            util_largura, util_altura = self.AREA_UTIL_LARGURA, self.AREA_UTIL_ALTURA
        else:  # Horizontal
            largura_pagina, altura_pagina = self.A4_ALTURA, self.A4_LARGURA
            util_largura = self.A4_ALTURA - (self.M_TOPO + self.M_BASE)
            util_altura = self.A4_LARGURA - (self.M_ESQ + self.M_DIR)
            
        return largura_pagina, altura_pagina, util_largura, util_altura

    def atualizar_proporcoes(self, event=None):
        if not self.caminho_imagem:
            return
            
        try:
            img = Image.open(self.caminho_imagem)
            largura_p, altura_p, util_l, util_a = self.obter_dados_painel()
            
            valor_spin = self.spin_colunas.get()
            cols = int(valor_spin) if valor_spin.isdigit() else 1
            if cols < 1: cols = 1
            
            proporcao_orig = img.width / img.height
            largura_util_total = cols * util_l
            altura_util_total = largura_util_total / proporcao_orig
            
            linhas = round(altura_util_total / util_a)
            if linhas < 1: 
                linhas = 1
                
            self.linhas_finais = linhas
            
            cm_l = (cols * 21.0) if self.combo_orientacao.current() == 0 else (cols * 29.7)
            cm_a = (linhas * 29.7) if self.combo_orientacao.current() == 0 else (linhas * 21.0)
            
            self.lbl_dimensoes_finais.config(
                text=f"Divisão: {cols} Colunas x {linhas} Linhas\nTotal de folhas A4: {cols * linhas} | Painel aprox: {cm_l:.1f} x {cm_a:.1f} cm"
            )
        except Exception:
            pass

    def gerar_mosaico(self):
        if not self.caminho_imagem:
            return
            
        caminho_pdf = filedialog.asksaveasfilename(
            initialfile="meu_poster_mosaico.pdf",
            defaultextension=".pdf", 
            filetypes=[("Documento PDF", "*.pdf")], 
            title="Salvar PDF do Póster"
        )
        if not caminho_pdf:
            return
            
        try:
            img_original = Image.open(self.caminho_imagem)
            largura_p, altura_p, util_l, util_a = self.obter_dados_painel()
            
            valor_spin = self.spin_colunas.get()
            cols = int(valor_spin) if valor_spin.isdigit() else 1
            rows = self.linhas_finais
            
            tamanho_total_util = (cols * util_l, rows * util_a)
            img_mosaico_total = img_original.resize(tamanho_total_util, Image.Resampling.LANCZOS)
            
            lista_paginas = []
            
            for r in range(rows):
                for c in range(cols):
                    box_esquerda = c * util_l
                    box_topo = r * util_a
                    box_direita = box_esquerda + util_l
                    box_base = box_topo + util_a
                    
                    pedaco_crop = img_mosaico_total.crop((box_esquerda, box_topo, box_direita, box_base))
                    folha_branca = Image.new("RGB", (largura_p, altura_p), "white")
                    
                    if self.combo_orientacao.current() == 0:
                        folha_branca.paste(pedaco_crop, (self.M_ESQ, self.M_TOPO))
                    else:
                        folha_branca.paste(pedaco_crop, (self.M_TOPO, self.M_ESQ))
                    
                    lista_paginas.append(folha_branca)
            
            if lista_paginas:
                lista_paginas[0].save(
                    caminho_pdf,
                    save_all=True,
                    append_images=lista_paginas[1:],
                    dpi=(300, 300),
                    quality=95
                )
                messagebox.showinfo("Sucesso!", f"PDF gerado com {len(lista_paginas)} páginas!\nSalvo em: {caminho_pdf}")
            
        except Exception as e:
            messagebox.showerror("Erro no Processamento", f"Ocorreu um problema ao gerar o PDF:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RasterbatorEpsonL3250(root)
    root.mainloop()
