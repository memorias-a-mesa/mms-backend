# mms-backend
Backend desenvolvido para integrar o projeto Memorias à Mesa, como entrega da matéria de Engenharia de Software do 7º semestre de Engenharia da Computação.  

Integrantes do grupo:
- 210626 - Cainã José Arruda Pinto 
- 223285 - Isabelle Munhoz Scarso 
- 223663 - José Antonio Classio Junior

# Funcionalidades implementadas: 
- Cadastro de Usuário: Criação de usuários com validação de e-mail e senha.
- Login: Autenticação de usuários com geração de token JWT.
- Criação de Receitas: Usuários autenticados podem criar receitas, que recebem um ID sequencial único. O autorId da receita é definido como o username do criador.
- Favoritar Receitas: Usuários podem favoritar receitas. O username do usuário é adicionado à lista favorited_by da receita e o campo qtdAvaliacao é incrementado.
- Desfavoritar Receitas: Usuários podem remover receitas dos favoritos. O username é removido da lista favorited_by e o campo qtdAvaliacao é decrementado, respeitando o limite mínimo de zero.
- Listagem de Receitas: Endpoint para listar todas as receitas cadastradas.
- Endpoint de Dados do Usuário: Retorna informações do usuário autenticado.
- Endpoint de Resumo de Receitas: Retorna um resumo das receitas criadas e favoritadas por um usuário.
- Validações e Segurança: Uso de autenticação JWT, validação de dados de entrada e tratamento de erros com mensagens claras.

# Arquitetura e Padrões:

## Organização do Código
- **Routers**: Gerenciam endpoints e status codes HTTP
- **Services**: Contêm a lógica de negócio
- **Repositories**: Abstraem o acesso ao banco de dados
- **Models**: Definem as estruturas de dados
- **Config**: Configurações do sistema (banco de dados, autenticação)

## Princípios SOLID Implementados:

1. **Single Responsibility Principle (SRP)**
   - Separação clara em camadas (routers, services, repositories)
   - Serviços específicos para cada domínio (ReceitaService, UserService)
   - Validações separadas em classes próprias (ReceitaValidationService)

2. **Open/Closed Principle (OCP)**
   - Interfaces abstratas para repositórios
   - Sistema preparado para extensões sem modificar código existente

3. **Liskov Substitution Principle (LSP)**
   - Implementações de repositórios podem ser substituídas sem afetar o sistema
   - Contratos de interface bem definidos

4. **Interface Segregation Principle (ISP)**
   - Interfaces específicas para cada contexto
   - Separação clara de responsabilidades

5. **Dependency Inversion Principle (DIP)**
   - Injeção de dependências nos serviços
   - Dependência de abstrações, não implementações

## Endpoints Disponíveis:

### Autenticação
```
POST /login
- Login do usuário (retorna token JWT)
```

### Usuários
```
POST /users
- Criação de novo usuário
GET /users/data
- Dados do usuário autenticado
```

### Receitas
```
GET /receitas
- Lista todas as receitas
POST /receitas
- Cria nova receita
POST /receitas/{recipe_id}/favorite
- Favorita uma receita
DELETE /receitas/{recipe_id}/favorite
- Remove receita dos favoritos
GET /receitas/autor/{username}
- Lista receitas de um autor
GET /receitas/user/{username}/data
- Resumo das receitas do usuário
```
# Tecnologias Utilizadas
- FastAPI
- MongoDB
- PyJWT
- Motor (MongoDB Async Driver)
- Pydantic
- Bcrypt