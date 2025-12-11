import os

def clean():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def se_nao_esta_vazia(value, field_name) -> None:
    if value is None or value == "":
        raise ValueError(f"{field_name} não pode ser vazio ou None.")

class Material:
    def __init__(self, nome, preco, unidade) -> None:
        self._nome = nome
        self._preco = preco
        self._unidade = unidade

    def imprimir_info(self) -> None:
        print(f"Material = {self._nome}, Preço = {self._preco}, Unidade = {self._unidade}")

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        self._nome = nome

    def get_preco(self):
        return self._preco

    def set_preco(self, preco):
        self._preco = preco

    def get_unidade(self):
        return self._unidade

    def set_unidade(self, unidade):
        self._unidade = unidade


class ListaDeComponentes:
    def __init__(self) -> None:
        self._materiais = []

    def adicionar_material(self, mat, quantidade) -> None:
        if mat is None:
            raise ValueError("Não é possível adicionar material nulo.")
        if quantidade <= 0.0:
            raise ValueError("A quantidade deve ser maior que zero.")

        encontrado = False
        for i, (m, q) in enumerate(self._materiais):
            if m == mat:
                self._materiais[i] = (mat, q + quantidade)
                encontrado = True
                break

        if not encontrado:
            self._materiais.append((mat, quantidade))

    def obter_preco(self) -> float:
        total = sum(mat.get_preco() * qtd for mat, qtd in self._materiais)
        return total

    def imprimir_materiais(self) -> None:
        for mat, qtd in self._materiais:
            print(f" - {mat.get_nome()} x {qtd}")

    def get_materiais(self):
        return self._materiais

    def set_materiais(self, materiais):
        self._materiais = materiais


class Produto:
    def __init__(self, nome, preco, tax) -> None:
        self._nome = nome
        self._preco = preco
        self._tax = tax
        self._componentes = ListaDeComponentes()

    def adicionar_material(self, mat, quantidade):
        self._componentes.adicionar_material(mat, quantidade)

    def obter_preco(self) -> float:
        return self._componentes.obter_preco()

    def preco_total(self) -> float:
        return self.obter_preco() * (1.0 + self._tax/100)

    def imprimir_info(self) -> None:
        print(f"Produto = {self._nome}")
        print(f"Taxa = {self._tax}")
        print(f"Preço (sem taxa) = {self.obter_preco()}")
        print(f"Preço com taxa = {self.preco_total()}")
        self._componentes.imprimir_materiais()

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        self._nome = nome

    def get_preco(self):
        return self._preco

    def set_preco(self, preco):
        self._preco = preco

    def get_tax(self):
        return self._tax

    def set_tax(self, tax):
        self._tax = tax

    def get_componentes(self):
        return self._componentes

    def set_componentes(self, componentes):
        self._componentes = componentes


class MaterialRegistrado:
    def __init__(self) -> None:
        self._materiais = []

    def adicionar_material(self, nome, preco, unidade) -> None:
        if self.encontrar_material(nome) is not None:
            raise ValueError("Material com este nome já existe.")

        mat = Material(nome, preco, unidade)
        self._materiais.append(mat)

    def remover_material(self, nome) -> None:
        mat = self.encontrar_material(nome)
        if mat is None:
            raise ValueError("Material não encontrado.")
        self._materiais.remove(mat)

    def encontrar_material(self, nome) -> None:
        for m in self._materiais:
            if m.get_nome() == nome:
                return m
        return None

    def get_materiais(self):
        return self._materiais

    def set_materiais(self, materiais):
        self._materiais = materiais


class HistoricoDeProdutos:
    def __init__(self) -> None:
        self._produtos = []

    def adicionar_produto(self, produto) -> None:
        if self.encontrar_produto(produto.get_nome()) is not None:
            raise ValueError("Produto com este nome já existe.")
        self._produtos.append(produto)

    def remover_produto(self, nome) -> None:
        prod = self.encontrar_produto(nome)
        if prod is None:
            raise ValueError("Produto não encontrado.")
        self._produtos.remove(prod)

    def encontrar_produto(self, nome) -> None:
        for p in self._produtos:
            if p.get_nome() == nome:
                return p
        return None

    def duplicar_produto(self, nome) -> None:
        prod = self.encontrar_produto(nome)
        if prod is None:
            raise ValueError("Produto não encontrado.")
        
        copia = Produto(nome=prod.get_nome(), preco=prod.get_preco(), tax=prod.get_tax())
        for mat, qtd in prod.get_componentes().get_materiais():
            copia.adicionar_material(mat, qtd)
        self._produtos.append(copia)
        print(f"Produto duplicado: {copia.get_nome()}")

    def get_produtos(self):
        return self._produtos

    def set_produtos(self, produtos):
        self._produtos = produtos


class BancoDeDados:
    def __init__(self) -> None:
        self._materiais = MaterialRegistrado()
        self._produtos = HistoricoDeProdutos()

    def adicionar_material(self, nome, preco, unidade) -> None:
        self._materiais.adicionar_material(nome, preco, unidade)

    def remover_material(self, nome) -> None:
        self._materiais.remover_material(nome)

    def encontrar_material(self, nome) -> None:
        return self._materiais.encontrar_material(nome)

    def adicionar_produto(self, produto) -> None:
        self._produtos.adicionar_produto(produto)

    def remover_produto(self, nome) -> None:
        self._produtos.remover_produto(nome)

    def encontrar_produto(self, nome) -> None:
        return self._produtos.encontrar_produto(nome)

    def duplicar_produto(self, nome) -> None:
        self._produtos.duplicar_produto(nome)

    def get_materiais(self):
        return self._materiais

    def set_materiais(self, materiais):
        self._materiais = materiais

    def get_produtos(self):
        return self._produtos

    def set_produtos(self, produtos):
        self._produtos = produtos


class Interface:
    def __init__(self) -> None:
        self.db = BancoDeDados()

    def imprimir_produtos(self) -> None:
        if not self.db.get_produtos().get_produtos():
            print("Nenhum produto registrado.")
            return

        print("Produtos Registrados:")
        for p in self.db.get_produtos().get_produtos():
            p.imprimir_info()

    def imprimir_materiais(self) -> None:
        if not self.db.get_materiais().get_materiais():
            print("Nenhum material registrado.")
            return

        print("Materiais Registrados:")
        for m in self.db.get_materiais().get_materiais():
            m.imprimir_info()


def prepare(A):
    materiais = [
        {"nome": "Botão", "preco": 0.5, "unidade": "unidade"},
        {"nome": "Tecido", "preco": 20.0, "unidade": "metro"},
        {"nome": "Linha 1", "preco": 2.0, "unidade": "rolo"},
        {"nome": "Linha 2", "preco": 2.5, "unidade": "rolo"}
    ]
    
    for mat in materiais:
        A.db.adicionar_material(mat["nome"], mat["preco"], mat["unidade"])
        print(f"Material {mat['nome']} adicionado ao registro de materiais!")


def main(A):
    interface = A

    prepare(A)

    while True:
        clean()
        print("\nMenu:")
        print("1. Criar um produto")
        print("2. Adicionar materiais ao registro de materiais")
        print("3. Ver registro de materiais")
        print("4. Ver registro de produtos")
        print("5. Sair")
        
        opcao = input("Escolha uma opção (1-5): ")

        if opcao == "1":
            clean()
            while True:
                nome_produto = input("Digite o nome do produto: ")
        
                if interface.db.encontrar_produto(nome_produto):
                    print(f"Produto com o nome '{nome_produto}' já existe. Por favor, escolha um nome diferente.")
                    continue
                break
        
            taxa_produto = float(input("Digite a taxa do produto (em percentual, por exemplo, 0.1 para 10%): "))
            produto = Produto(nome_produto, preco=0.0, tax=taxa_produto)
        
            while True:
                nome_material = input("Digite o nome do material para adicionar ao produto (ou 'fim' para terminar): ")
                if nome_material.lower() == "fim":
                    break
        
                material = interface.db.encontrar_material(nome_material)
                if material is None:
                    print(f"Material '{nome_material}' não encontrado!")
                    continue
        
                quantidade = float(input(f"Digite a quantidade do material '{nome_material}' a ser adicionada: "))
                produto.adicionar_material(material, quantidade)
        
            preco_produto = produto.obter_preco()
            produto.set_preco(preco_produto)
            print(f"Produto {nome_produto} criado com sucesso!")
            print(f"Preço total do produto (sem taxa) = {preco_produto}")
        
            interface.db.adicionar_produto(produto)
        
            produto.imprimir_info()
            input("Pressione Enter para voltar ao menu...")


        elif opcao == "2":
            clean()
            nome_material = input("Digite o nome do material a ser registrado: ")
            preco_material = float(input(f"Digite o preço do material {nome_material}: "))
            unidade_material = input(f"Digite a unidade do material {nome_material} (ex: kg, unidade, litro): ")
            interface.db.adicionar_material(nome_material, preco_material, unidade_material)
            print(f"Material {nome_material} adicionado ao registro de materiais!")
            input("Pressione Enter para voltar ao menu...")

        elif opcao == "3":
            clean()
            interface.imprimir_materiais()
            input("Pressione Enter para voltar ao menu...")

        elif opcao == "4":
            clean()
            interface.imprimir_produtos()
            input("Pressione Enter para voltar ao menu...")

        elif opcao == "5":
            clean()
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente.")


A = Interface()
main(A)
