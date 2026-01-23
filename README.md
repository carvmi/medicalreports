## Sistema de apoio ao diagnóstico do câncer de mama por análise de mamografias
### Objetivo
A solução permite que profissionais médicos tenham acesso aos protótipos de inteligência artificial para auxiliar no diagnóstico. Além disso, auxilia o Grupo de Pesquisas em Computação Biomédica, do Instituto do Complexo Econômico-Industrial da Saúde da UFPE, a validar as soluções atuais em desenvolvimento.
### Acesso
Para acesso ao sistema, o usuário precisa ser identificado via login. Conforme as exigências da Sociedade Brasileira de Informática em Saúde e da ANVISA para esse tipo de sistema, as ações desse usuário precisam também ser rastreadas e armazenas em arquivo de log.
### Inteligência Artificial
Após realizado o login, o usuário deve conseguir escolher uma imagem de mamografia previamente armazenada como arquivo. O sistema vai exibir uma visualização navegável da imagem em tela. Após seleção da região suspeita de lesão na mama, será habilitada a funcionalidade de análise automática, acionada por um botão. Ao acionar o botão, a imagem será enviada para uma API que a envia para máquina de aprendizado e retorna o resultado da classificação. A API retorna esse resultado para o front, que elabora uma prévia do laudo gerado pela IA para o usuário.
### Laudo
Caso o usuário concorde, o laudo poderá ser impresso em PDF ou impressora. O laudo apresenta o nome completo do usuário, intituição e registro profissional, além da afirmação que o usuário concorda com o resultado gerado pela máquina. A aparência do laudo pode ser configurada previamente, exibindo um cabeçalho com o nome, marca e o endereço físico e eletrônico da instituição. Essa configuração é carregada do banco de dados logo após o usuário se logar. 

## Padrão do Django
- O Django segue o padrão MVT, o que significa que tem três arquivos principais: Models, Views e Templates. 
- Models: Onde gerencia o banco de dados
- Views: Todas as funções python responsáveis por gerenciar o processamento das URLs (é necessário importar as views no arquivos "urls.py")
- Templates: arquivos html
### Relacionamentos
- Medprofiles e Institution - Many to Many (Muitos para muitos)
- Patient e Mammogram - One to Many (Um para muitos)

## Templates
### Homepage
<img width="1915" height="946" alt="image" src="https://github.com/user-attachments/assets/aec7f1a5-a28b-4b31-ae13-0386f8ad25ca" />

### Login 
O requisito de "Acesso" foi aplicado nas views de exams, institution, medprofiles e patients para bloquear o acesso de usuários não autenticados. Foi utilizado "from django.contrib.auth.decorators import login_required" e "@login_required(login_url='/login/')" para retornar para a página de login.
<img width="1911" height="939" alt="image" src="https://github.com/user-attachments/assets/682972c3-ba85-472a-bc86-9cfc738fff0c" />

### Cadastro 
<img width="1902" height="933" alt="image" src="https://github.com/user-attachments/assets/11dcbaaa-5d45-4d51-9c6e-fe7ba32851d4" />




