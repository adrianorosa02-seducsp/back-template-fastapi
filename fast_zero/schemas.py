from pydantic import BaseModel, EmailStr

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# O que a API responde publicamente (Mostrando a senha para fins didáticos!)
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    #password: str

# Como o dado fica no Banco de Dados
class UserDB(UserSchema):
    id: int

# Novos Schemas para Alunos
class AlunoSchema(BaseModel):
    escola: str
    serie: str
    n_aluno: int
    nome_aluno: str
    ra: str
    digito: str
    dt_nascimento: str
    email_microsoft: EmailStr
    email_google: EmailStr
    situacao_aluno: str

class AlunoPublic(AlunoSchema):
    id: int
