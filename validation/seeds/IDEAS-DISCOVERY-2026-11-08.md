<!-- Cited research seed. Not an instruction, not a rubric, and not evidence of demand or prize odds.
Source file supplied 2026-11-08. Attribution stays with the research note. The adjudication loop does not execute this prose.
-->

# Ideas & Validation — camada de descoberta

Pesquisa pública realizada em 08/11/2026, America/Chicago (CST). Escopo: pesquisa e propostas, não implementação. Nenhum repo clonado, código de terceiros executado, inscrição alterada, contato enviado ou serviço contratado. Contexto: ROADMAP-MONITOR-2026-11-05.md e pesquisa VALIDATION-STACK-GITHUB-2026-11-08.md. Roadmap é snapshot anterior: não serve para atualizar resultados/submissões nesta rodada.

## Recomendação

**Primeiro: Import Flight Recorder.** Dor documentada por fabricante e usuários; demo verificável; núcleo determinístico local sem LLM pago. A área de importação é concorrida: diferencial precisa ser recibo reversível e prova de preservação, não “AI limpa CSV”.

**Segundo: Decision Afterlife.** Relato direto de equipes descreve exatamente a lacuna Jira–Confluence e workarounds; caminho real para Codegeist via Forge. Não basta resumir decisões: detectar que premissa mudou, apontar evidência e mostrar os itens afetados. Risco: ferramentas nativas podem já ser suficientes e extração pode produzir ruído.

Tab Escape é terceira opção e bom recurso interno da stack: encantamento visual forte, mas menor originalidade. Blackout Rehearsal tem diferenciação de demonstração e encaixe temático híbrido ainda condicional. Part Twin é útil, mas cobertura de modelos pode inviabilizar escala.

SOTA é uma ambição de qualidade, não uma classificação comprovada. Não há benchmark comparativo nem validação humana nesta rodada. Nenhuma ideia tem novidade global provada, demanda validada, receita, odds de prêmio ou garantia de capital.

## Gates de eventos — fontes oficiais abertas hoje

### Kiroween
https://kiroween.devpost.com/rules
Aberto para desenvolvimento de novos projetos desde 30/10/2026 11:00 CDT, America/Chicago; prazo 04/12/2026 16:00 CST. Só trabalho novo após início; frameworks/templates padrão permitidos com divulgação de trabalho prévio. App funcional feito com Kiro, GitHub público OSS com LICENSE detectável e /.kiro na raiz, URL funcional e vídeo público YouTube menor que três minutos. Não basta código gerado por outra ferramenta com pasta .kiro cosmética. Categorias Resurrection, Frankenstein, Skeleton Crew (duas aplicações distintas) e Costume Contest. Cinco critérios com pesos iguais: impacto, tecnologia/Kiro, design, inovação, apresentação. Não forçar tema se o produto não pertence a uma categoria.

Regra exclui residentes do Brasil, entre outras jurisdições; não presumir elegibilidade pela nacionalidade ou por estar fisicamente nos EUA: residência e demais requisitos devem ser verdadeiros e conferidos pelo responsável antes da entrada. Prêmio não exige viagem; não publicar dados privados de identidade no repo. Se usar igoreduardoai publicamente, manter materiais internos/identidade privada separados. Nenhum submit nesta rodada.

Grave Truth já está na fila deste evento: não recomendar abandonar trabalho em andamento ou reapresentar outro projeto congelado como “novo”. Registro de início e preexistência precisa ser conferido; esta pesquisa não auditou histórico do projeto.

### Firebase #BuildHybridAI
https://firebasehybridaihackathon.devpost.com/rules
https://firebasehybridaihackathon.devpost.com/
Regras oficiais ainda NÃO disponíveis em 08/11; página promete publicação em 09/11. Janela anunciada 09–30/11, encerramento anunciado 30/11 16:00 CST. Tema anunciado: Firebase AI Logic com inferência híbrida on-device/cloud. **Pesquisa/preparo apenas; nenhum build como entrada Firebase iniciado aqui.** Reavaliar elegibilidade, início permitido, tecnologias, free tier/hardware e billing quando regras saírem. Não usar “Firebase hosting” como substituto do requisito de inferência híbrida. Não garantir inferência cloud grátis ou disponibilidade de modelo local.

### Codegeist
https://codegeist2026.devpost.com/rules
Aberto desde 27/10/2026 11:00 CDT; prazo 22/12/2026 14:00 CST, America/Chicago. Exige app Forge integrado a ao menos um entre Jira, Confluence, JSM, Bitbucket, Teamwork Graph ou Rovo. Developer site gratuito previsto. Novos e existentes: existentes precisam atualização/rebuild em Forge após início, manifest e módulo Forge. Link instalável no ambiente dos jurados e instruções completas. Vídeo menor que cinco minutos, com aviso de que jurados não precisam ver além de três. Rovo NÃO obrigatório para prêmio principal. Há módulos específicos para bônus agentes/MCP/graph, não promessa de acesso grátis a tudo. Residência brasileira também aparece nas exclusões. Uso de Forge tem limites de recursos/cotas: medir sem contratar plano.

Nenhuma das ideias usa governo, PHI ou exige serviço pago no núcleo. Entradas gratuitas não significam custo operacional zero. Checar ferramentas de desenvolvimento e cotas separadamente. Revalidar regras antes de qualquer build elegível/submit.

## 1. Import Flight Recorder — caixa-preta de dados que impede uma migração “bonita” de estragar valores

**Público/tarefa:** pequena equipe importando catálogo ou estoque CSV entre ferramentas.
**Dor observada:** Microsoft documenta remoção automática de zeros, truncamento após 15 dígitos e conversões para data; explica que formatar depois não recupera valores perdidos. Issue ImportExcel #33 traz relatos e workarounds com apóstrofo/fórmula; é HISTÓRICO e fechado, não bug atual alegado. Dor estrutural continua documentada pelo suporte atual.
- https://support.microsoft.com/en-us/excel/keeping-leading-zeros-and-large-numbers
- https://github.com/dfinke/ImportExcel/issues/33

**Mecanismo:** simular importação em schema explícito, produzir diff célula a célula, separar ambiguidade de erro, registrar transformações aprovadas e exportar dados + recibo de proveniência. Preservar original imutável. Sem tentar adivinhar dígitos já destruídos.
**Próximos existentes:** Excel Power Query e conversões configuráveis; Dromo já oferece mapeamento AI, validação, modo privado, metadados e export anotado. PapaParse (MIT) já resolve parsing no browser. Portanto, parser/limpador/privacidade não são novidade.
- https://dromo.io/ (produto comercial, não apresentado como OSS)
- https://github.com/mholt/PapaParse ; README master/README.md lido via GitHub
**Diferencial hipótese:** recibo reversível e contraexemplo visível de onde a informação desapareceria, com recusa de reparo irrecuperável. Ainda precisa comparação funcional para ver o que Dromo/Power Query já cobrem.
**Demo surpreendente:** arrastar catálogo sintético aparentemente normal → mapa mostra SKU com zero, ID grande e data ambígua → clique abre origem versus conversão → usuário escolhe política → export e reimport preservam valores → arquivo já truncado recebe “não recuperável sem original”, não invenção.
**Experimento mais barato:** walkthrough/planilha manual com catálogo não sensível e pessoa que faça importações; comparar com fluxo atual e Power Query. Observar se detecta e corrige perdas, se entende recibo e se o guarda. Matar/reduzir se configuração nativa resolver sem esforço ou recibo não mudar decisão.
**Viabilidade:** um formato CSV, um schema alvo, parser local e ledger; sem LLM necessário. Limites de tamanho/memória, encoding, locale, fórmula injetada em CSV e export seguro são essenciais. Não “sanitizar” apagando silenciosamente dados. Sem PII/PHI.
**Evento:** Kiroween apenas se categoria justificada e uso real de Kiro; Frankenstein não decorativo. Firebase só após regras e se inferência híbrida resolver algo indispensável, não forçar AI num núcleo determinístico. Sem encaixe Forge automático.
**Pode falhar:** mercado cheio, usuário prefere corrigir no Excel, suporte a mil schemas explode escopo, confiança em export depende de prova real.

## 2. Decision Afterlife — uma decisão volta a aparecer quando a premissa que a sustentava morre

**Público/tarefa:** equipe pequena mantém Jira + Confluence e precisa rever decisão sem caçar comentários.
**Dor direta:** discussão Atlassian “Best practice for tracking key decisions…” relata perda de motivo/aprovador/alternativas após meses; respostas usam projetos separados, macros, ADRs e disciplina manual. Relato prova ocorrência, não tamanho do mercado.
- https://community.atlassian.com/forums/discussion/3195026/best-practice-for-tracking-key-decisions-and-major-changes-in-jira-cloud
**Mecanismo:** cartão de decisão versionado com afirmação, premissas, fonte, itens impactados e condição de revisão. Um fato explícito muda → cartão identifica quais decisões precisam revisão, sem afirmar causalidade inventada ou decidir sozinho.
**Existentes:** macros e DACI Confluence; Rovo search/agents; Log4brains (Apache-2.0), ADR docs-as-code, timeline e busca. “Memória de equipe” não é inovação por si.
- https://www.atlassian.com/software/confluence/templates/decision
- https://github.com/thomvaill/log4brains ; develop/README.md lido
**Diferencial hipótese:** validade temporal das premissas e replay da decisão com contexto da época, ligado ao impacto operacional, não resumo de reunião. Só triggers explícitos no MVP.
**Demo:** ticket diz “usar fornecedor A porque suporta export X” → cartão abre fonte e alternativa rejeitada → mudar fixture de capacidade para “X removido” → reaparece decisão + issues afetadas + evidência anterior e nova → pessoa confirma revisar; nada é reescrito automaticamente.
**Experimento barato:** board sintético e cartões manuais com líder/engenheiro; pedir reconstrução de uma decisão com e sem cartões e reconhecer mudança relevante. Verificar se custo de manter premissas supera tempo poupado. Invalida se simples macro/ADR atende igual ou alertas são ignorados.
**Viabilidade:** Forge issue panel + uma fonte Confluence autorizada; links explícitos e regras determinísticas primeiro. LLM opcional apenas para sugerir candidatos, nunca aprovar. Permissões por usuário, propagação de exclusões, versões/fontes e revisão humana. Sem Slack/email/contas reais no MVP.
**Evento:** encaixe direto Codegeist Software Teams: Forge + Jira/Confluence são caminho crítico do produto. App instalável e quotas testadas antes de aspirar bônus Rovo. Não declarar credenciais/eligibilidade sem verificação.
**Pode falhar:** manter premissas dá trabalho; relações falsas geram ruído; recursos nativos satisfazem cliente; permissionamento pode ser mais difícil que demo.

## 3. Tab Escape — mostrar o exato lugar onde uma jornada sem mouse fica impossível

**Público/tarefa:** designer/dev precisa entender e corrigir bloqueio de teclado numa jornada.
**Dor:** axe-core já admite cobertura parcial e incomplete; issue Playwright #14422 documenta elemento focável antes de listener estar pronto, com workaround de wait, considerado bug que afeta humano. Histórico fechado, não bug atual de Playwright.
- https://github.com/microsoft/playwright/issues/14422
- https://github.com/dequelabs/axe-core (README lido na pesquisa anterior)
**Mecanismo:** executar teclas reais num app de teste autorizado, registrar transições de foco e estado, detectar loop/bloqueio e exportar caso mínimo + teste de regressão. Não simular pessoa com deficiência nem certificar WCAG.
**Existentes:** taba11y já desenha ordem de tabulação e destaca elementos; Playwright e axe já fazem automação/auditoria. Caminho colorido não é novidade.
- https://chromewebstore.google.com/detail/taba11y-tab-order-accessi/aocppmckdocdjkphmofnklcjhdidgmga (atualizado 11/03/2026)
- https://github.com/microsoft/playwright
**Diferencial hipótese:** percurso dinâmico condicionado à tarefa → “esta compra/edição não termina” + reprodução mínima/teste, em vez de só mostrar tab order estático.
**Demo:** scanner não aponta violação nos estados simples → pessoa tenta fluxo com teclado → replay mostra modal cujo foco nunca chega ao botão esperado → aplicar correção manual na fixture → replay completa a tarefa. Uma armadilha dentro de modal é legítima se Escape/saída acessível funcionam; não marcar qualquer loop como bug.
**Experimento barato:** comparar fluxo e relatório com taba11y + trace nativo; pedir dev reproduzir e explicar causa. Descartar se apenas duplica report existente ou detecta trap intencional como erro.
**Viabilidade:** um app local com modal e formulário, Chromium primeiro, ações e assertivos definidos. Shadow DOM/iframes, variações do browser, foco intencional e usuário real são limites. Nenhum patch automático em site de terceiros.
**Evento:** Kiroween Frankenstein só com combinação funcional de grafo de navegação + regressão, feito com Kiro; não inferir elegibilidade só pelo nome “Escape”. Pode ficar melhor como ferramenta interna do que novo projeto competitivo.
**Pode falhar:** diferença é incremental; falsos positivos e teste automatizado de acessibilidade não substituem tecnologias assistivas/humanos.

## 4. Blackout Rehearsal — ensaio que prova o que sobrevive quando a internet desaparece

**Público/tarefa:** pequena empresa com formulário offline de inventário/inspeção não clínica quer saber se “salvo” é realmente recuperável.
**Dor:** relato Kobo de drafts sumidos após update, com respostas adicionais em 2024/2025; issue Enketo #1043 sobre imagens offline perdidas é histórico fechado. Não alegar bug atual no produto.
- https://community.kobotoolbox.org/t/recovering-lost-drafts-after-an-update-offline-submissions-stored-before-submitting-to-server/42948
- https://github.com/enketo/enketo/issues/1043
**Mecanismo:** harness para app instrumentado simula cenários de desconexão/reabertura/retry; mostra “local”, “pendente”, “confirmado” com recibos e hashes. Não precisa construir plataforma de formulários nova nem prometer recuperar cache apagado.
**Existentes:** Workbox já enfileira/reenvia requests; Automerge (MIT) resolve sincronização CRDT, com valores concorrentes recuperáveis por getConflicts. Não é nova invenção de offline sync.
- https://developer.chrome.com/docs/workbox/modules/workbox-background-sync
- https://github.com/automerge/automerge
- https://automerge.org/docs/reference/documents/conflicts/
**Diferencial hipótese:** uma demonstração adversarial compreensível do contrato de durabilidade, com evidência do que foi perdido/duplicado e distinção entre merge convergente e decisão semântica correta.
**Demo:** inventário fictício com nota e foto → desligar endpoint de teste → fechar/reabrir app → alterar mesmo campo em duas cópias → reconectar → dados preservados, conflito fica visível, nenhuma duplicata, estado final confirmado somente após ACK real.
**Experimento barato:** desenhar linha de estados sobre logs sintéticos e pedir dev prever onde dado pode sumir; só avançar se descobre defeito não detectado pelos testes atuais. MVP técnico futuro usa fixture deliberadamente frágil versus corrigida. Não testar destrutivamente app de cliente.
**Viabilidade:** app controlado e endpoint local, IndexedDB, operation IDs, fault injection reproduzível. Workbox avisa que checkbox offline DevTools não bloqueia requests do service worker: testar rede/servidor de verdade em ambiente isolado. Quota/eviction iOS e multi-device real são limites; não alegar garantia “zero perda”.
**Evento:** tema Firebase é promissor apenas em tese: AI local poderia estruturar nota offline, cloud enriquecer ao reconectar, mas isso NÃO é necessário ao harness e pode ser cosmético. Esperar regras 09/11 e validar modelo/hardware/custo antes de build de entrada. Se híbrido não for caminho crítico, não escolher esse evento.
**Pode falhar:** demanda é de infraestrutura, difícil explicar; instrumentação específica por app; uma demo de dois browsers não prova offline móvel em campo.

## 5. Part Twin — gêmeos visuais, compatibilidade diferente

**Público/tarefa:** pessoa organiza peças/acessórios de um equipamento e precisa saber se a variante correta está documentada, antes de usar ou buscar reposição.
**Dor:** iFixit explica que versões visualmente próximas exigem modelo exato, ano/código/GHz; às vezes não há mapeamento confiável por serial. Isso evidencia problema, não vontade comprovada de pagar por novo app.
- https://www.ifixit.com/Info/Part_Verification
**Mecanismo:** passaporte de objeto local com modelo exato + trechos de manual autorizado; comparar peça candidata com requisitos declarados. Classificar compatível/incompatível/não comprovado com fonte. Não inferir compatibilidade só por foto e não orientar reparos perigosos.
**Existentes:** checker e dispositivos salvos do próprio iFixit; Homebox (AGPL-3.0) inventário, fotos, documentos, garantias e manutenção. Inventário com QR não é novo.
- https://github.com/sysadminsmedia/homebox (URL canônica confirmada; README main lido)
**Diferencial hipótese:** comparação de contraexemplo quase idêntico e “qual evidência falta?” em vez de catálogo + chatbot. Sem promessa de cobertura universal.
**Demo:** dois acessórios fictícios de equipamento não crítico parecem iguais → passaporte revela código de variante diferente → fonte descarta um e confirma outro → remover evidência de um requisito → resultado vira “não comprovado”, não palpite.
**Experimento barato:** cartões físicos/fotos sintéticas e manuais próprios, pedir pessoa selecionar candidato e explicar por quê. Parar se modelo/manual já dá resposta imediatamente ou cadastrar dados custa mais que resolver problema.
**Viabilidade:** uma família de equipamentos inofensivos, tabelas criadas por nós, busca local; OCR opcional somente com revisão. Evitar baterias, tensão de rede, equipamentos médicos, gás e segurança. Não copiar fotos/manuais sem permissão, não montar banco de serial real nem comprar nada.
**Evento:** nenhuma exigência oficial dá encaixe especial; Kiroween só se conceito e categoria honestos; Firebase pendente e não forçar modelo. Maior risco de virar app genérico de inventário; baixa prioridade.
**Pode falhar:** dados de compatibilidade caros/incompletos, responsabilidade física, usuário consulta fabricante de graça; novidade mais fraca que aparência da demo.

## Lições de vencedores — evidência pública, não auditoria nem vídeo assistido

1. **InteractionKit**, marcado Winner na galeria oficial Kiroween 2025; página descreve dois apps distintos (Math-O-Lantern, Holo-Board) sobre tracking de gestos e template. Lição: input visível → resultado imediato e mecanismo reutilizável demonstrado em tarefas distintas. Não precisamos copiar webcam/17 gestos ou aceitar “sem alucinações” como prova.
- https://kiroween-2025.devpost.com/project-gallery
- https://devpost.com/software/kiro-interactionkit
2. **Faxi**, página Devpost mostra Winner Best Resurrection e Influencer Judges’ Choice; fax manuscrito vira tarefa digital e resposta por fax. Lição: respeitar hábito real e remover fricção, não colocar chat por cima. Também mostra por que escopo importa: telecom, pagamentos e várias integrações não são nossa escolha sem custo. Claims de segurança/usuários do autor não foram validados por nós.
- https://devpost.com/software/faxi-16iecy

Nesta pesquisa foram lidas páginas e descrições de demos, não executados builds nem assistidos integralmente vídeos. Vencer não prova demanda, lucro, generalização ou que determinada feature causou vitória. Não copiar projetos anteriores como entradas novas.

## Workflow leve para incorporar à stack (proposta, sem rotina criada)

Observar dor → mapear alternativas → mecanismos candidatos → reality check → demo/protótipo → validação humana → rubrica oficial + harness técnico → submit/evidências.

Para cada candidato registrar:
- dor/tarefa e público específico; URL/data de observação; citação curta e workaround; distinguir relato histórico, docs atuais e hipótese;
- concorrente mais próximo e tarefa que já resolve; não tratar “open source” como originalidade;
- mecanismo e resultado observável; demo sem chat quando não necessário; o que invalida ideia;
- custos, dados/permissões, licenças, limites e regra de início/reuso;
- menor experimento capaz de derrubar hipótese; observação humana com consentimento, sem enviar convites nesta tarefa;
- resultado real por tentativa: conclusão, erro, tempo/custo observados, review e evidência; nenhum score inventado;
- decisão: investigar/prototipar/pausar/descartar e motivo; registro de versão e hipótese alterada.

Três rotas possíveis: (A) microferramenta determinística — Import, mais confiável e menos “AI”; (B) integração contextual — Decision, sponsor e dor mais claros, maior custo de permissão/adoção; (C) simulação/híbrido — Blackout, efeito visual forte, maior risco técnico e regras pendentes. Recomendo A e B para experimentar, não desenvolver cinco produtos.

Harness: pytest/gold/holdout + E2E Playwright + axe/teclado + performance + ataques pertinentes + piloto sintético apenas para descobrir falhas + revisão humana. Métrica técnica não substitui interesse de usuários. Cada achado reproduzível vira regressão, não feedback inventado de “cliente”.

Antes de publicar: revisão de licença e identidade; entrada/edição permitida e freeze; repo/demo verificáveis; claims com fontes; vídeo mostra funcionalidade real e uma recusa; confirmação + URL + snapshot e commit na hora. Nenhuma ação externa aprovada ou realizada nesta pesquisa.

## Próximo gate

Escolher um experimento para Import e um para Decision; não criar novo repo ou codar antes de aprovar escopo e evento. Firebase permanece pesquisa até 09/11 e regras oficiais. Não chamar catálogo de ideias de “SOTA comprovado”.
