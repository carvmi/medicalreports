## Documentação da API (JSON)

### Base URL
- `http://localhost:8000/api/`

### Autenticação (sessão)
A API usa sessão do Django. Faça login e reutilize os cookies nas chamadas seguintes.

#### `POST /api/auth/register`
Cria um novo usuário.

Request (JSON):
```json
{
  "username": "doctor1",
  "email": "doctor1@example.com",
  "password": "12345678"
}
```

Response 201:
```json
{
  "data": {
    "id": 1,
    "username": "doctor1",
    "email": "doctor1@example.com"
  }
}
```

Response 400:
```json
{
  "error": "Usuario ja existe."
}
```

#### `POST /api/auth/login`
Autentica e cria sessão.

Request (JSON):
```json
{
  "username": "doctor1",
  "password": "12345678"
}
```

Response 200:
```json
{
  "data": {
    "id": 1,
    "username": "doctor1",
    "email": "doctor1@example.com"
  }
}
```

Response 401:
```json
{
  "error": "Usuario ou senha invalidos."
}
```

#### `GET /api/auth/me`
Retorna o usuário autenticado.

Response 200:
```json
{
  "data": {
    "id": 1,
    "username": "doctor1",
    "email": "doctor1@example.com"
  }
}
```

Response 401:
```json
{
  "error": "Autenticacao necessaria."
}
```

### Pacientes

#### `GET /api/patients/`
Lista todos os pacientes.

Response 200:
```json
{
  "data": [
    {
      "id": 1,
      "full_name": "Maria Silva",
      "birth_date": "1985-10-12",
      "gender": "F",
      "cpf": "12345678901",
      "phone": "81999999999",
      "email": "maria@example.com",
      "allergies": "Penicilina",
      "pre_existing_conditions": "Hipertensão",
      "notes": "Paciente em acompanhamento.",
      "created_at": "2026-02-10T10:30:45.123456-03:00",
      "updated_at": "2026-02-10T10:30:45.123456-03:00"
    }
  ]
}
```

#### `GET /api/patients/<id>/`
Retorna um paciente.

Response 200:
```json
{
  "data": {
    "id": 1,
    "full_name": "Maria Silva",
    "birth_date": "1985-10-12",
    "gender": "F",
    "cpf": "12345678901",
    "phone": "81999999999",
    "email": "maria@example.com",
    "allergies": "Penicilina",
    "pre_existing_conditions": "Hipertensão",
    "notes": "Paciente em acompanhamento.",
    "created_at": "2026-02-10T10:30:45.123456-03:00",
    "updated_at": "2026-02-10T10:30:45.123456-03:00"
  }
}
```

#### `POST /api/patients/`
Cria um paciente.

Request (JSON):
```json
{
  "full_name": "Maria Silva",
  "birth_date": "1985-10-12",
  "gender": "F",
  "cpf": "12345678901",
  "phone": "81999999999",
  "email": "maria@example.com",
  "allergies": "Penicilina",
  "pre_existing_conditions": "Hipertensão",
  "notes": "Paciente em acompanhamento."
}
```

Response 201:
```json
{
  "data": {
    "id": 1,
    "full_name": "Maria Silva",
    "birth_date": "1985-10-12",
    "gender": "F",
    "cpf": "12345678901",
    "phone": "81999999999",
    "email": "maria@example.com",
    "allergies": "Penicilina",
    "pre_existing_conditions": "Hipertensão",
    "notes": "Paciente em acompanhamento.",
    "created_at": "2026-02-10T10:30:45.123456-03:00",
    "updated_at": "2026-02-10T10:30:45.123456-03:00"
  }
}
```

#### `PUT/PATCH /api/patients/<id>/`
Atualiza um paciente.

Request (JSON):
```json
{
  "phone": "81988888888",
  "notes": "Atualizado."
}
```

Response 200:
```json
{
  "data": {
    "id": 1,
    "full_name": "Maria Silva",
    "birth_date": "1985-10-12",
    "gender": "F",
    "cpf": "12345678901",
    "phone": "81988888888",
    "email": "maria@example.com",
    "allergies": "Penicilina",
    "pre_existing_conditions": "Hipertensão",
    "notes": "Atualizado.",
    "created_at": "2026-02-10T10:30:45.123456-03:00",
    "updated_at": "2026-02-10T10:30:45.123456-03:00"
  }
}
```

#### `DELETE /api/patients/<id>/`
Remove um paciente.

Response 200:
```json
{
  "data": {
    "deleted": true
  }
}
```

### Instituições

#### `GET /api/institutions/`
Lista instituições.

Response 200:
```json
{
  "data": [
    {
      "id": 1,
      "name": "Hospital Central",
      "endereco_fisico_id": 1,
      "endereco_fisico": {
        "id": 1,
        "rua": "Rua A",
        "cep": "50000000",
        "bairro": "Centro",
        "cidade": "Recife",
        "uf": "PE",
        "number": "100"
      },
      "site": "https://hospital.example.com",
      "phone": "8133334444",
      "email": "contato@hospital.example.com",
      "itype": "H",
      "logo_url": "http://localhost:8000/media/institution/static/logo.png"
    }
  ]
}
```

#### `GET /api/institutions/<id>/`
Retorna uma instituição.

Response 200:
```json
{
  "data": {
    "id": 1,
    "name": "Hospital Central",
    "endereco_fisico_id": 1,
    "endereco_fisico": {
      "id": 1,
      "rua": "Rua A",
      "cep": "50000000",
      "bairro": "Centro",
      "cidade": "Recife",
      "uf": "PE",
      "number": "100"
    },
    "site": "https://hospital.example.com",
    "phone": "8133334444",
    "email": "contato@hospital.example.com",
    "itype": "H",
    "logo_url": "http://localhost:8000/media/institution/static/logo.png"
  }
}
```

#### `POST /api/institutions/`
Cria instituição.

Request (JSON):
```json
{
  "name": "Hospital Central",
  "endereco_fisico": 1,
  "site": "https://hospital.example.com",
  "phone": "8133334444",
  "email": "contato@hospital.example.com",
  "itype": "H"
}
```

Response 201:
```json
{
  "data": {
    "id": 1,
    "name": "Hospital Central",
    "endereco_fisico_id": 1,
    "endereco_fisico": {
      "id": 1,
      "rua": "Rua A",
      "cep": "50000000",
      "bairro": "Centro",
      "cidade": "Recife",
      "uf": "PE",
      "number": "100"
    },
    "site": "https://hospital.example.com",
    "phone": "8133334444",
    "email": "contato@hospital.example.com",
    "itype": "H",
    "logo_url": null
  }
}
```

#### `PUT/PATCH /api/institutions/<id>/`
Atualiza instituição.

Request (JSON):
```json
{
  "phone": "8133335555"
}
```

Response 200:
```json
{
  "data": {
    "id": 1,
    "name": "Hospital Central",
    "endereco_fisico_id": 1,
    "endereco_fisico": {
      "id": 1,
      "rua": "Rua A",
      "cep": "50000000",
      "bairro": "Centro",
      "cidade": "Recife",
      "uf": "PE",
      "number": "100"
    },
    "site": "https://hospital.example.com",
    "phone": "8133335555",
    "email": "contato@hospital.example.com",
    "itype": "H",
    "logo_url": null
  }
}
```

#### `DELETE /api/institutions/<id>/`
Remove instituição.

Response 200:
```json
{
  "data": {
    "deleted": true
  }
}
```

### Endereços

#### `GET /api/addresses/`
Lista endereços.

Response 200:
```json
{
  "data": [
    {
      "id": 1,
      "rua": "Rua A",
      "cep": "50000000",
      "bairro": "Centro",
      "cidade": "Recife",
      "uf": "PE",
      "number": "100"
    }
  ]
}
```

#### `GET /api/addresses/<id>/`
Retorna um endereço.

Response 200:
```json
{
  "data": {
    "id": 1,
    "rua": "Rua A",
    "cep": "50000000",
    "bairro": "Centro",
    "cidade": "Recife",
    "uf": "PE",
    "number": "100"
  }
}
```

#### `POST /api/addresses/`
Cria endereço.

Request (JSON):
```json
{
  "rua": "Rua A",
  "cep": "50000000",
  "bairro": "Centro",
  "cidade": "Recife",
  "uf": "PE",
  "number": "100"
}
```

Response 201:
```json
{
  "data": {
    "id": 1,
    "rua": "Rua A",
    "cep": "50000000",
    "bairro": "Centro",
    "cidade": "Recife",
    "uf": "PE",
    "number": "100"
  }
}
```

#### `PUT/PATCH /api/addresses/<id>/`
Atualiza endereço.

Request (JSON):
```json
{
  "number": "120"
}
```

Response 200:
```json
{
  "data": {
    "id": 1,
    "rua": "Rua A",
    "cep": "50000000",
    "bairro": "Centro",
    "cidade": "Recife",
    "uf": "PE",
    "number": "120"
  }
}
```

#### `DELETE /api/addresses/<id>/`
Remove endereço.

Response 200:
```json
{
  "data": {
    "deleted": true
  }
}
```

### Perfis Médicos

#### `GET /api/medprofiles/`
Lista profissionais.

Response 200:
```json
{
  "data": [
    {
      "id": 1,
      "full_name": "Dr. João Souza",
      "position": "Radiologista",
      "specialization": "Mamografia",
      "professional_registration": "CRM-PE 12345",
      "institutions": [
        {
          "id": 1,
          "name": "Hospital Central"
        }
      ]
    }
  ]
}
```

#### `GET /api/medprofiles/<id>/`
Retorna um profissional.

Response 200:
```json
{
  "data": {
    "id": 1,
    "full_name": "Dr. João Souza",
    "position": "Radiologista",
    "specialization": "Mamografia",
    "professional_registration": "CRM-PE 12345",
    "institutions": [
      {
        "id": 1,
        "name": "Hospital Central"
      }
    ]
  }
}
```

#### `POST /api/medprofiles/`
Cria profissional.

Request (JSON):
```json
{
  "full_name": "Dr. João Souza",
  "position": "Radiologista",
  "specialization": "Mamografia",
  "professional_registration": "CRM-PE 12345",
  "institution": [1]
}
```

Response 201:
```json
{
  "data": {
    "id": 1,
    "full_name": "Dr. João Souza",
    "position": "Radiologista",
    "specialization": "Mamografia",
    "professional_registration": "CRM-PE 12345",
    "institutions": [
      {
        "id": 1,
        "name": "Hospital Central"
      }
    ]
  }
}
```

#### `PUT/PATCH /api/medprofiles/<id>/`
Atualiza profissional.

Request (JSON):
```json
{
  "position": "Radiologista Senior"
}
```

Response 200:
```json
{
  "data": {
    "id": 1,
    "full_name": "Dr. João Souza",
    "position": "Radiologista Senior",
    "specialization": "Mamografia",
    "professional_registration": "CRM-PE 12345",
    "institutions": [
      {
        "id": 1,
        "name": "Hospital Central"
      }
    ]
  }
}
```

#### `DELETE /api/medprofiles/<id>/`
Remove profissional.

Response 200:
```json
{
  "data": {
    "deleted": true
  }
}
```

### Exames

#### `GET /api/exams/`
Lista exames.

Response 200:
```json
{
  "data": [
    {
      "id": 1,
      "patient_id": 1,
      "patient_name": "Maria Silva",
      "local_id": 1,
      "local_name": "Hospital Central",
      "exam_date": "2026-02-10",
      "description": "Achado suspeito em quadrante superior.",
      "result": "INDETERMINADO",
      "itype": "PENDENTE",
      "acceptance_term": false,
      "user_ip": "127.0.0.1",
      "created_at": "2026-02-10T11:10:45.123456-03:00",
      "image_url": "http://localhost:8000/media/mammograms/exam1.png"
    }
  ]
}
```

#### `GET /api/exams/<id>/`
Retorna um exame.

Response 200:
```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "patient_name": "Maria Silva",
    "local_id": 1,
    "local_name": "Hospital Central",
    "exam_date": "2026-02-10",
    "description": "Achado suspeito em quadrante superior.",
    "result": "INDETERMINADO",
    "itype": "PENDENTE",
    "acceptance_term": false,
    "user_ip": "127.0.0.1",
    "created_at": "2026-02-10T11:10:45.123456-03:00",
    "image_url": "http://localhost:8000/media/mammograms/exam1.png"
  }
}
```

#### `POST /api/exams/`
Cria exame.

Request (JSON):
```json
{
  "patient": 1,
  "local": 1,
  "exam_date": "2026-02-10",
  "description": "Achado suspeito em quadrante superior.",
  "result": "INDETERMINADO",
  "itype": "PENDENTE",
  "acceptance_term": false
}
```

Response 201:
```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "patient_name": "Maria Silva",
    "local_id": 1,
    "local_name": "Hospital Central",
    "exam_date": "2026-02-10",
    "description": "Achado suspeito em quadrante superior.",
    "result": "INDETERMINADO",
    "itype": "PENDENTE",
    "acceptance_term": false,
    "user_ip": "127.0.0.1",
    "created_at": "2026-02-10T11:10:45.123456-03:00",
    "image_url": null
  }
}
```

#### `PUT/PATCH /api/exams/<id>/`
Atualiza exame.

Request (JSON):
```json
{
  "result": "BENIGNO",
  "itype": "PRONTO"
}
```

Response 200:
```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "patient_name": "Maria Silva",
    "local_id": 1,
    "local_name": "Hospital Central",
    "exam_date": "2026-02-10",
    "description": "Achado suspeito em quadrante superior.",
    "result": "BENIGNO",
    "itype": "PRONTO",
    "acceptance_term": false,
    "user_ip": "127.0.0.1",
    "created_at": "2026-02-10T11:10:45.123456-03:00",
    "image_url": null
  }
}
```

#### `DELETE /api/exams/<id>/`
Remove exame.

Response 200:
```json
{
  "data": {
    "deleted": true
  }
}
```

### Observações importantes
- Todas as rotas (exceto `register` e `login`) exigem autenticação.
- `PUT/PATCH` aceitam payload JSON parcial (apenas os campos a atualizar).
- Upload de imagem em `exams` e `logo` em `institutions` deve ser feito via `multipart/form-data`.
- `DELETE` faz soft delete (marca `is_active=false` e `deleted_at`).
