# Scientific Video · PT / EN

Agente de comunicação científica baseado no kit bilíngue “Do artigo ao vídeo científico”. Versão 0.1.0, piloto local.

## Começar

Depois de instalar o plugin, abra uma nova conversa no Codex. Selecione **Scientific Video · PT / EN**, anexe o artigo e envie:

> Use $scientific-video para transformar este artigo em um vídeo de comunicação científica em português. Conduza as nove etapas com minhas validações e mantenha um registro do projeto. Comece pela interpretação científica do artigo.

Informe a pasta onde deseja salvar o novo projeto. O agente deve aproveitar as informações que você já forneceu, sem repetir perguntas. Para continuar depois, informe a pasta do projeto e peça que leia `project_state.json` e `CONTINUITY.md`.

O nome técnico da skill é `scientific-video`; o plugin é `scientific-video-agent`. Algumas interfaces mostram a skill com o nome do plugin como prefixo. Se a menção não resolver, selecione a skill no menu da interface.

## As nove etapas

1. Entendimento científico do artigo.
2. Protagonista, público e narrativa.
3. Quantidade de tapes, roteiro e duração.
4. Linguagem visual e identidade.
5. Duas imagens e validação de cada tape.
6. Animatic e teste da história.
7. Produção e aprovação de cada tape.
8. Montagem final e revisão.
9. Pacote de divulgação e autorização de publicação.

Responda **Aprovado**, **Ajustar: ...** ou **Voltar à etapa: ...**, indicando o tape e a versão quando houver mais de um item em revisão. O agente apresenta o resultado antes de pedir aprovação. As etapas 05 e 07 se repetem por tape. A aprovação do último par ou clipe pode fechar a etapa correspondente, sem pedir a mesma aprovação novamente.

## Continuidade e fidelidade

Adote como sugestão principal e formato padrão 1080 × 1920 pixels (largura × altura), vertical 9:16, desde o início. Apresente esse padrão na revisão; mude somente mediante pedido explícito do usuário. Não escolha outro formato automaticamente por causa do canal, das referências ou das limitações da ferramenta.

Cada tape possui IN e OUT. O OUT aprovado é o mesmo arquivo usado como IN do seguinte. Para N tapes consecutivos, o planejamento prevê N+1 imagens únicas antes de revisões e exceções aprovadas. O número de tapes depende do artigo; 19 não é um padrão obrigatório.

O primeiro tape tem uma chamada visual ligada ao protagonista. O último escurece parcialmente a cena e faz os créditos subirem, mantendo o protagonista visível. Os créditos são extraídos de informações verificadas.

O agente deve diferenciar dados reais e metáforas visuais. Números, curvas, instituições e conclusões não podem ser inventados. Alterações em materiais aprovados geram uma revisão identificada.

## O que está incluído

Uma skill com o fluxo de trabalho, os nove prompts em cada idioma, regras comuns, modelos de registro e um auxiliar para criar pastas e verificar a consistência dos registros. O auxiliar usa Python 3 e a biblioteca padrão; se Python não estiver disponível, o agente pode manter os mesmos registros com as ferramentas de arquivos disponíveis.

As ferramentas de imagem, vídeo, áudio e edição dependem do ambiente de cada pesquisador. Este pacote não inclui assinatura, créditos ou um gerador de vídeo. Quando uma ferramenta não estiver disponível, o agente prepara os materiais de produção e informa o que continua pendente.

Os controles de aprovação são instruções e registros do fluxo. A verificação automática detecta inconsistências de versões, arquivos e sequência; ela não comprova por si só a autenticidade de uma aprovação ou a correção científica. Essas verificações continuam a exigir revisão do pesquisador e inspeção dos resultados.

## Compartilhar sem GitHub

Envie o ZIP do agente aos colegas. Ele contém apenas o agente e sua documentação, sem o artigo ou os vídeos do projeto original. O destinatário deve extrair o pacote em uma pasta própria e instalar o plugin local no ambiente compatível.

No Codex, o colega pode usar a skill de criação de plugins com esta instrução, anexando ou indicando a pasta extraída:

> Use $plugin-creator para registrar e instalar o plugin local scientific-video-agent desta pasta. Preserve as instruções e os arquivos existentes; não recrie o agente. Depois, confira a instalação e explique como iniciá-lo em uma nova conversa.

Como alternativa sem instalação, em um ambiente que consiga ler os arquivos locais, indique `skills/scientific-video/SKILL.md` e peça ao assistente para seguir esse fluxo e ler as referências do idioma escolhido. Essa alternativa carrega as instruções na conversa; não instala um plugin.

## Estado desta versão

O pacote passa pelos validadores de skill e plugin. O auxiliar foi verificado com 14 testes de registros e arquivos sintéticos. Isso não equivale a um teste completo de um novo artigo até um vídeo final. O primeiro uso com outro artigo é o piloto recomendado para avaliar narrativa, produção visual e experiência do pesquisador.

Os registros de cada novo artigo devem ficar fora da pasta do plugin. Compartilhe apenas os materiais que pretende divulgar; a instalação do agente não publica o projeto.
