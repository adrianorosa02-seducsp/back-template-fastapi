import os
from http import HTTPStatus
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import create_db, get_session
from fast_zero.models import Aluno, User
from fast_zero.schemas import AlunoPublic, AlunoSchema, UserPublic, UserSchema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Comando para criar as tabelas ao subir a aplicação
@app.on_event('startup')
def on_startup():
    create_db()


@app.get('/')
def read_root():
    return {
        'Disciplina': 'Backend para Desenvolvimento Ágil',
        'aluno_id': os.getenv('ALUNO_NUM', 'Não definido'),
        'repositorio': os.getenv('GITHUB_REPO', 'Não definido'),
        'ambiente': 'Docker Swarm',
        'status': 'Online e Integrado',
    }


# Endpoints de Usuários
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        raise HTTPException(status_code=400, detail='Email já cadastrado')

    new_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@app.get('/users/', response_model=List[UserPublic])
def list_users(session: Session = Depends(get_session)):
    users = session.scalars(select(User)).all()
    return users


# Novos Endpoints de Alunos
@app.post('/alunos/', status_code=HTTPStatus.CREATED, response_model=AlunoPublic)
def cadastra_aluno(aluno: AlunoSchema, session: Session = Depends(get_session)):
    # Opcional: Verificar se RA já existe
    db_aluno = session.scalar(select(Aluno).where(Aluno.ra == aluno.ra))
    if db_aluno:
        raise HTTPException(status_code=400, detail='Aluno com este RA já cadastrado')

    new_aluno = Aluno(
        escola=aluno.escola,
        serie=aluno.serie,
        n_aluno=aluno.n_aluno,
        nome_aluno=aluno.nome_aluno,
        ra=aluno.ra,
        digito=aluno.digito,
        dt_nascimento=aluno.dt_nascimento,
        email_microsoft=aluno.email_microsoft,
        email_google=aluno.email_google,
        situacao_aluno=aluno.situacao_aluno
    )

    session.add(new_aluno)
    session.commit()
    session.refresh(new_aluno)

    return new_aluno


@app.get('/alunos/', response_model=List[AlunoPublic])
def lista_alunos(session: Session = Depends(get_session)):
    alunos = session.scalars(select(Aluno)).all()
    return alunos
