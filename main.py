import customtkinter as ctk
from tkinter import filedialog

from banco import criar_tabela, salvar_produto, listar_produtos
from calculos import calcular_preco
from estilo import *
from importar_excel import importar_produtos_excel


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Precificação de Doces")
        self.geometry("1000x600")
        self.configure(fg_color=COR_FUNDO)

        criar_tabela()

        self.menu_lateral()
        self.tela_cadastro()

    def menu_lateral(self):
        self.frame_menu = ctk.CTkFrame(
            self,
            width=220,
            fg_color=COR_CARD
        )
        self.frame_menu.pack(side="left", fill="y")

        titulo = ctk.CTkLabel(
            self.frame_menu,
            text="Doces App",
            font=FONTE_TITULO,
            text_color=COR_TEXTO
        )
        titulo.pack(pady=30)

        ctk.CTkButton(
            self.frame_menu,
            text="Cadastrar Produto",
            fg_color=COR_BOTAO,
            hover_color=COR_BOTAO_HOVER,
            font=FONTE_BOTAO,
            command=self.tela_cadastro
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self.frame_menu,
            text="Visualizar Produtos",
            fg_color=COR_BOTAO,
            hover_color=COR_BOTAO_HOVER,
            font=FONTE_BOTAO,
            command=self.tela_visualizacao
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(
            self.frame_menu,
            text="Importar Planilha",
            fg_color=COR_BOTAO,
            hover_color=COR_BOTAO_HOVER,
            font=FONTE_BOTAO,
            command=self.importar_planilha
        ).pack(pady=10, padx=20, fill="x")

    def limpar_tela(self):
        if hasattr(self, "frame_conteudo"):
            self.frame_conteudo.destroy()

        self.frame_conteudo = ctk.CTkFrame(
            self,
            fg_color=COR_FUNDO
        )

        self.frame_conteudo.pack(
            side="right",
            fill="both",
            expand=True
        )

    def criar_campo(self, frame, texto):
        label = ctk.CTkLabel(
            frame,
            text=texto,
            font=FONTE_NORMAL,
            text_color=COR_TEXTO
        )

        label.pack(
            pady=(10, 2),
            padx=20,
            anchor="w"
        )

        entrada = ctk.CTkEntry(
            frame,
            height=35,
            font=FONTE_NORMAL
        )

        entrada.pack(
            pady=5,
            padx=20,
            fill="x"
        )

        return entrada

    def tela_cadastro(self):
        self.limpar_tela()

        titulo = ctk.CTkLabel(
            self.frame_conteudo,
            text="Cadastro de Produto",
            font=FONTE_TITULO,
            text_color=COR_TEXTO
        )
        titulo.pack(pady=20)

        form = ctk.CTkFrame(
            self.frame_conteudo,
            fg_color=COR_CARD
        )
        form.pack(
            pady=10,
            padx=30,
            fill="x"
        )

        self.entrada_nome = self.criar_campo(form, "Nome do produto:")
        self.entrada_ingredientes = self.criar_campo(form, "Custo ingredientes R$:")
        self.entrada_embalagem = self.criar_campo(form, "Custo embalagem R$:")
        self.entrada_mao_obra = self.criar_campo(form, "Mão de obra R$:")
        self.entrada_margem = self.criar_campo(form, "Margem de lucro %:")
        self.entrada_estoque = self.criar_campo(form, "Quantidade estoque:")

        self.resultado = ctk.CTkLabel(
            self.frame_conteudo,
            text="",
            font=FONTE_SUBTITULO,
            text_color=COR_TEXTO
        )
        self.resultado.pack(pady=10)

        ctk.CTkButton(
            self.frame_conteudo,
            text="Confirmar e Visualizar",
            fg_color=COR_BOTAO,
            hover_color=COR_BOTAO_HOVER,
            font=FONTE_BOTAO,
            height=40,
            command=self.salvar
        ).pack(pady=15)

    def salvar(self):
        try:
            nome = self.entrada_nome.get().strip()

            if nome == "":
                self.resultado.configure(
                    text="Digite o nome do produto."
                )
                return

            custo_ingredientes = float(
                self.entrada_ingredientes.get().replace(",", ".")
            )

            embalagem = float(
                self.entrada_embalagem.get().replace(",", ".")
            )

            mao_obra = float(
                self.entrada_mao_obra.get().replace(",", ".")
            )

            margem_lucro = float(
                self.entrada_margem.get().replace(",", ".")
            )

            estoque = int(
                self.entrada_estoque.get()
            )

            custo_total, lucro, preco_venda = calcular_preco(
                custo_ingredientes,
                embalagem,
                mao_obra,
                margem_lucro
            )

            salvar_produto(
                nome,
                custo_ingredientes,
                embalagem,
                mao_obra,
                margem_lucro,
                custo_total,
                lucro,
                preco_venda,
                estoque
            )

            self.limpar_campos()

            self.tela_visualizacao()

        except ValueError:
            self.resultado.configure(
                text="Preencha os campos corretamente."
            )

    def limpar_campos(self):
        self.entrada_nome.delete(0, "end")
        self.entrada_ingredientes.delete(0, "end")
        self.entrada_embalagem.delete(0, "end")
        self.entrada_mao_obra.delete(0, "end")
        self.entrada_margem.delete(0, "end")
        self.entrada_estoque.delete(0, "end")

    def importar_planilha(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a planilha",
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )

        if caminho:
            importar_produtos_excel(caminho)
            self.tela_visualizacao()

    def tela_visualizacao(self):
        self.limpar_tela()

        titulo = ctk.CTkLabel(
            self.frame_conteudo,
            text="Produtos Cadastrados",
            font=FONTE_TITULO,
            text_color=COR_TEXTO
        )
        titulo.pack(pady=20)

        produtos = listar_produtos()

        if not produtos:
            vazio = ctk.CTkLabel(
                self.frame_conteudo,
                text="Nenhum produto cadastrado.",
                font=FONTE_SUBTITULO,
                text_color=COR_TEXTO_SECUNDARIO
            )
            vazio.pack(pady=30)
            return

        for produto in produtos:
            nome, preco_venda, custo_total, lucro, estoque = produto

            card = ctk.CTkFrame(
                self.frame_conteudo,
                fg_color=COR_CARD,
                corner_radius=12
            )

            card.pack(
                pady=8,
                padx=30,
                fill="x"
            )

            texto = f"""
Produto: {nome}

Preço de venda: R$ {preco_venda:.2f}

Custo total: R$ {custo_total:.2f}

Lucro estimado: R$ {lucro:.2f}

Estoque: {estoque} unidades
"""

            label = ctk.CTkLabel(
                card,
                text=texto,
                font=FONTE_NORMAL,
                text_color=COR_TEXTO,
                justify="left"
            )

            label.pack(
                pady=10,
                padx=20,
                anchor="w"
            )


if __name__ == "__main__":
    app = App()
    app.mainloop()