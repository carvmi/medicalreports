# Medical Reports

Aplicacao Django para cadastro e gerenciamento de dados clinicos de mamografia, com interface web e API JSON.

## Funcionalidades implementadas

- Autenticacao de usuario na interface web:
- cadastro (`/cadastro/`)
- login (`/login/`)
- CRUD web para:
- exames (`/exams/`)
- pacientes (`/patients/`)
- instituicoes e enderecos (`/institution/`)
- perfis profissionais (`/medprofiles/`)
- Soft delete nas entidades principais com `is_active` e `deleted_at`.
- Upload de imagem do exame e logo da instituicao.
- Exportacao de laudo em PDF para exames (`/exams/report/<id>`), contendo dados do paciente, instituicao, exame, aceite e IP registrado.
- API JSON com autenticacao de sessao para:
- auth (`/api/auth/register`, `/api/auth/login`, `/api/auth/me`)
- patients (`/api/patients/`, `/api/patients/<id>/`)
- institutions (`/api/institutions/`, `/api/institutions/<id>/`)
- addresses (`/api/addresses/`, `/api/addresses/<id>/`)
- medprofiles (`/api/medprofiles/`, `/api/medprofiles/<id>/`)
- exams (`/api/exams/`, `/api/exams/<id>/`)
- Endpoint de documentacao da API em HTML (`/api/docs`), carregado de `MRAPI-documentation.html`.

## Regras implementadas para IP

- O IP do exame e preenchido automaticamente no backend no momento de criacao.
- O campo `user_ip` nao aparece nos formularios de criacao/edicao.
- O IP e mostrado no PDF do laudo.
- `X-Forwarded-For` so e aceito quando a requisicao vem de proxy confiavel (`DJANGO_TRUSTED_PROXY_IPS`).

## Filtros de registros ativos

- Listagens web usam apenas registros ativos.
- No formulario de exame, os selects de `patient` e `local` exibem apenas opcoes ativas (`is_active=True`).

## Estrutura do projeto

- Apps Django em `apps/`:
- `apps.login`
- `apps.patients`
- `apps.institution`
- `apps.medprofiles`
- `apps.exams`
- `apps.api`
- Configuracoes em `config/settings/`:
- `base.py`
- `dev.py`
- `prod.py`

## Relacionamentos implementados

- `HealthProfessional` e `Institution`: many-to-many.
- `Patient` e `MammogramExam`: one-to-many.
- `Institution` e `Address`: one-to-one.

<img width="1800" height="855" alt="Projeto_Integrador" src="https://github.com/user-attachments/assets/40b66011-6926-4fa6-8a5e-304930c1e974" />

## Exportacao PDF

A geracao de PDF e feita com ReportLab na app de exames.

<img width="1610" height="867" alt="image" src="https://github.com/user-attachments/assets/afe66293-dfc2-4282-bece-93c67c4e98b6" />

## Telas

### Homepage

<img width="1915" height="946" alt="image" src="https://github.com/user-attachments/assets/aec7f1a5-a28b-4b31-ae13-0386f8ad25ca" />

### Login

O acesso a exames, instituicoes, medprofiles e patients e protegido com autenticacao via `login_required`.

<img width="1911" height="939" alt="image" src="https://github.com/user-attachments/assets/682972c3-ba85-472a-bc86-9cfc738fff0c" />

### Cadastro

<img width="1902" height="933" alt="image" src="https://github.com/user-attachments/assets/11dcbaaa-5d45-4d51-9c6e-fe7ba32851d4" />

## Execucao local

```bash
py -3 manage.py migrate
py -3 manage.py runserver 0.0.0.0:8000
```

## Testes

```bash
py -3 manage.py test apps.exams -v 1
```
