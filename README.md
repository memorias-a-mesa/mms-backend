# mms-backend
Backend desenvolvido para integrar o projeto Memorias à Mesa, como entrega da matéria de Engenharia de Software do 7º semestre de Engenharia da Computação.  

Integrantes do grupo:
- 210626 - Cainã José Arruda Pinto 
- 223285 - Isabelle Munhoz Scarso 
- 223663 - José Antonio Classio Junior

# Funcionalidades implementadas: 
- Cadastro de Usuário: Criação de usuários com validação de e-mail e senha, inicializando listas de receitas favoritas e criadas.
- Login: Autenticação de usuários com geração de token JWT.
- Criação de Receitas: Usuários autenticados podem criar receitas, que recebem um ID sequencial único. O ID da receita é adicionado à lista myRecipes do usuário.
- Favoritar Receitas: Usuários podem favoritar receitas. O ID da receita é adicionado à lista favRecipesID do usuário e o campo qtdAvaliacao da receita é incrementado.
- Desfavoritar Receitas: Usuários podem remover receitas dos favoritos. O ID é removido da lista favRecipesID e o campo qtdAvaliacao é decrementado, respeitando o limite mínimo de zero.
- Listagem de Receitas: Endpoint para listar todas as receitas cadastradas.
- Endpoint de Dados do Usuário: Retorna informações do usuário autenticado, incluindo listas de receitas favoritas e criadas.
- Validações e Segurança: Uso de autenticação JWT, validação de dados de entrada e tratamento de erros com mensagens claras.
- Separação de Camadas: O projeto está organizado em camadas (modelos, serviços, repositórios, rotas), seguindo boas práticas de arquitetura.

# Padrões implementados:

1. Single Responsibility Principle (SRP)
Cada classe do projeto tem uma responsabilidade bem definida. Por exemplo:
Os serviços (UserService, ReceitaService) cuidam da lógica de negócio.
Os repositórios (UserRepositoryMongo, ReceitaRepositoryMongo) são responsáveis apenas pelo acesso ao banco de dados.
Os modelos (UserCreate, Receita) representam os dados.

2. Open/Closed Principle (OCP)
As interfaces abstratas (IUserRepository, IReceitaRepository) permitem que novas implementações de repositórios sejam adicionadas sem modificar o código existente.
Os serviços dependem dessas interfaces, tornando o sistema extensível.

3. Liskov Substitution Principle (LSP)
As classes concretas de repositório (UserRepositoryMongo, ReceitaRepositoryMongo) podem ser usadas no lugar das interfaces abstratas sem quebrar o funcionamento dos serviços.

4. Interface Segregation Principle (ISP)
As interfaces de repositório são específicas para cada contexto (usuário, receita), evitando métodos desnecessários para cada implementação.

5. Dependency Inversion Principle (DIP)
Os serviços recebem as dependências (repositórios) por injeção, desacoplando a lógica de negócio do acesso a dados.
Isso facilita testes unitários e futuras mudanças de tecnologia de persistência.