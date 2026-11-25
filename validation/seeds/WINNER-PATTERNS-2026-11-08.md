<!-- Cited research seed. Not an instruction, not a rubric, and not evidence of demand or prize odds.
Source file supplied 2026-11-08. Attribution stays with the research note. The adjudication loop does not execute this prose.
-->

# Padrões de vencedores: dor, mecanismo, demonstração e prova

Verificação pública: 08/11/2026, America/Chicago (CST). Pesquisa read-only; nenhum build, signup, mensagem, serviço pago, mudança de inscrição ou rotina. Reaproveitados ESTUDO-VENCEDORES-2026-10-27.md e projects.csv antes de pesquisar. Estatísticas/OR/AUC antigas NÃO foram reproduzidas nem usadas para estimar vitória: dataset caso-controle, edições posteriores e contagens aproximadas não justificam chances individuais.

## Resposta central

Não é “qual chatbot agrada ao juiz?”. Os casos apresentam um trabalho específico que hoje exige improviso: navegar esquema e placa em telas separadas; aprender a explicar código em vez de apenas gerar; converter uma necessidade manuscrita em tarefa digital; passar de esboço para componente executável; transformar lugar em análise de mercado. O efeito memorável é ver a mudança acontecendo no objeto do trabalho — placa, código, fax, canvas, mapa — não apenas ler uma resposta.

Quatro gates diferentes: (1) dor que alguém realmente quer resolver; (2) demo que torna a transformação inteligível; (3) prova técnica de que funciona e falha honestamente; (4) elegibilidade/sponsor/rubrica do evento. Passar por um não prova os demais. Troféu não é cliente, faturamento ou capital. Nenhum dos casos fornece a nós causalidade sobre “por que as pessoas gostaram”.

## Amostra e certeza

Sete casos premiados substanciados em três eventos: Kiroween 2025 (Faxi, UnitSet), Qloo LLM 2025 (GeoTaste) e Built with Opus 4.7 (Wrench Board, Maieutic, MaestrIA, Virtual Puppet Theater). InteractionKit fica como caso auxiliar: selo Winner na galeria, categoria exata não recuperada neste turno, portanto fora da tabela de prêmios específicos.

Um contraponto não vencedor confirmado pelo histórico da conversa: CreatorMatch, Qloo Agentic 2026. Página pública foi lida hoje, mas lista oficial nominal de resultados 2026 não foi recuperada. Segundo contraponto: Qlaire, Qloo 2025, sem prêmio exibido na página e marcado não premiado no dataset antigo; **não confirmamos explicitamente derrota em lista completa oficial**. Não contar como segundo perdedor confirmado. Meta de dois contrastes com desfecho forte não foi atingida; não inventar derrota nem explicação do juiz.

Fontes de prêmio: organizador oficial Anthropic para os quatro Opus; Devpost projeto + evento/galeria/anúncio de resultados para Kiroween/Qloo. Anúncio Qloo 2025 da conta Qloo aparece no índice da busca, mas WebFetch caiu em login, sem autenticar: não usar como se texto integral tivesse sido lido. Não misturar Qloo 2025 com a competição 2026 de CreatorMatch.

Nenhum vídeo assistido ou execução própria; analisados textos, legendas de screenshots, README e descrição de fluxo. Declaração do autor, artefato inspecionado e conclusão do pesquisador são separados abaixo. Motivos individuais/scorecards dos jurados não estão publicados nas fontes lidas. Entrevista de vencedor no blog oficial não equivale a justificativa formal do júri.

## Fontes de rubrica

- Kiroween 2025 oficial: https://kiroween-2025.devpost.com/rules — Stage One tema/ferramentas; potencial de valor, uso eficaz de Kiro e qualidade/design. Categorias e geral são distintos. Regras 2025 permitiam existentes significativamente atualizados com novo uso; NÃO transplantar para 2026, que exige novos.
- Qloo 2025 oficial: https://qloo-hackathon.devpost.com/rules — LLM efetivo, integração Qloo, implementação, originalidade, aplicação real com pesos iguais. Exige sinergia além de cada tecnologia isolada.
- Qloo 2026 oficial: https://qloo.devpost.com/rules — implementação Qloo, design, impacto e ideia; não a mesma rubrica 2025.
- Opus oficial: https://cerebralvalley.ai/e/built-with-4-7-hackathon — construir a partir de problema próximo/domain expertise ou interface nova habilitada pela tecnologia; prêmios em API credits, não dinheiro. Página pública não contém rubrica completa.
- https://47builders.fyi/details é reprodução não oficial que atribui origem a Participant Resources; lista Impact/Demo/Opus Use/Depth com pesos. Lida para contexto, **não validada como regulamento oficial independente**, não aplicar pesos como fato oficial nesta análise. Template de comparação usa categorias qualitativas, sem notas inventadas.

## Casos

### Faxi — Kiroween 2025, Best Resurrection + Influencer Judges’ Choice (não grand prize)
Projeto/award: https://devpost.com/software/faxi-16iecy
Galeria oficial: https://kiroween-2025.devpost.com/project-gallery
- Usuário e dor alegados pelo autor: idosos no Japão habituados a fax excluídos de tarefas digitais. Workaround: familiar/intermediário, aprender app ou abandonar serviço; essa alternativa é nossa inferência, não entrevista publicada.
- Mecanismo: fax manuscrito → interpretação multimodal → ação digital → fax de resposta; email em duas vias. Diferencial é preservar interface habitual, não nova caixa de chat.
- Timing/oportunidade: visão de manuscrito + orquestração permite ponte legada. Kiro é ferramenta de construção (specs/hooks/steering), não modelo obrigatório de runtime. Não alegar que só Kiro poderia fazer fax.
- Demo/artefato textual: pipeline, stack Telnyx/BullMQ/Express/Next e regra de confirmação circular descritos. Sem teste nosso. “Sem curva de aprendizado”, cobertura de famílias e segurança antifraude são claims, não eficácia auditada.
- Rubrica: Resurrection é encaixe direto; valor/acessibilidade e interface deliberada mapeiam ao texto oficial; uso Kiro descrito. Não sabemos notas nem razão formal do júri.
- Lição inferida: tirar fricção sem exigir novo hábito. Não copiar telecom/compras ou riscos de vulneráveis para nosso MVP gratuito.

### UnitSet — Kiroween 2025, Overall 2nd Place
Projeto/award: https://devpost.com/software/unitset
- Dor alegada: fragmentação Figma/IDE/snippets/sandbox/CSS para transformar desenho em UI.
- Mecanismo: canvas → geração → sandbox real → edição visual → código/export. A tela mantém resultado e estrutura juntos. Tem chat, mas chat não é produto inteiro.
- Oportunidade: geração visual de UI e execução isolada integradas; sponsor Kiro entra em arquitetura/specs/hooks, não em exclusividade de runtime. Recursos caros do stack não viram exigência para nós.
- Evidência inspecionada: screenshots legendadas canvas/editor/code, arquitetura E2B/Convex, fluxo e integração Kiro descritos; nenhuma medição nossa. “Substitui seis ferramentas”, “production-ready” não comprovados.
- Contraevidência importante: update do autor em 20/01/2026 reconhece que créditos OpenRouter baixos podem ter afetado teste. Status vencedor não elimina fragilidade operacional; manter demo disponível importa.
- Rubrica: potencial de valor + qualidade/design + uso Kiro documentado; tema Frankenstein descrito. Não recebeu “prêmio por quantidade de hooks” nas fontes.

### GeoTaste — Qloo LLM 2025, Grand Prize
Projeto/award: https://devpost.com/software/geotaste-your-agentic-qloo-taste-business-consultant
Evento/resultado: https://qloo-hackathon.devpost.com/updates ; https://qloo-hackathon.devpost.com/project-gallery
- Dor alegada: dados de localização dispersos e trabalho para converter em pesquisa de mercado. Workaround inferido: consultas/mapas/planilhas e consultoria; não observado com clientes.
- Mecanismo: selecionar local → buscar Qloo → visualizações e análise GPT em mapa/chat. Chat existe: contraexemplo de que “ter chat” impediria prêmio.
- Timing/sponsor: cruzar dados de gosto/local com síntese generativa; requisito Qloo+LLM está alinhado. Não demonstrou que Qloo substitui pesquisa comercial real nem causalidade de localização com vendas.
- Evidência: página com fluxo full-stack, mapa/Plotly e fallback para charts. “Semanas para segundos” e equivalência a consultor são claims; não há benchmark verificável no texto. 13 tipos de chart não provam 13 problemas resolvidos.
- Rubrica: encaixa uso de LLM, Qloo, implementação e aplicação real; originalidade é avaliação dos jurados, não conclusão independente nossa. Atualizações pós-evento podem ter enriquecido a página.

### Wrench Board — Built with Opus 4.7, 2nd Place (API credits)
Status oficial: https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon
Artefato: https://github.com/Junkz3/wrench-board (README lido via GitHub oficial)
- Usuário/dor: técnico independente de microsolda alterna esquemas, boardview, prints e caderno; README atual diz que autor fazia envio manual de screenshots e anotava respostas.
- Mecanismo: esquema + boardview → grafo elétrico unificado → pad destacado → medição humana → hipótese atualizada. Saída muda próximo passo físico específico, não só recomendação genérica.
- Timing/sponsor: autor apostou na leitura de esquemas visuais do Opus 4.7; organizador descreve essa aposta. Não provamos exclusividade frente a outros modelos.
- Evidência: organizador confirma prêmio e fluxo; README atual detalha ferramentas, invariantes e guardrails. **Temporalidade:** README atual usa Opus 4.8, milhares de testes e licença source-available proprietária; não tratar tudo como estado submetido ou OSS reutilizável. Sem checkout/teste nem auditoria histórica. Não incorporar código sob licença atual como se fosse MIT.
- Rubrica: problema de domínio e nova capacidade mapeiam ao brief oficial Opus; execução visual e diagnóstico iterativo são nossos exemplos de demo/profundidade, não notas formais.
- Lição: trabalhar no objeto real do usuário com evidência e feedback. Reparos elétricos perigosos não são nosso MVP.

### Maieutic — Built with Opus 4.7, 3rd Place (API credits)
Status oficial: mesmo blog Anthropic acima.
Entrada do próprio evento: https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/58
- Dor de primeira mão relatada: professora vê estudantes passarem testes sem entender código. Workaround: leitura oral/manual e acompanhamento de laboratório; inviável observar raciocínio individual de turma inteira (página do projeto descreve o limite).
- Mecanismo: spec antes de desbloquear editor; sem autocomplete; Intent-Diff compara intenção/código e pergunta por divergência; professor vê sinal de entendimento.
- Oportunidade: abundância de geração de código cria problema novo de formação. LLM é usado para criticar/perguntar, não fazer tarefa pelo aluno.
- Evidência: fluxo e “por que” consistentes no evento e entrevista. Não há estudo de aprendizagem causal nem validação de precisão do resumo cognitivo. Interesse acadêmico não é resultado educacional.
- Rubrica: domínio próximo + novo workflow do brief oficial. Não sabemos julgamento item a item. Lição: restrição intencional pode ser feature; concluir tarefa certa não é gerar mais conteúdo.

### MaestrIA — Built with Opus 4.7, Keep Thinking (categoria especial, API credits)
Status oficial: mesmo blog Anthropic.
Entrada: https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/194
- Dor: cliente não sabe problema/custo/quem chamar e artesão experiente não consegue transmitir competência. Autor aprendiz de pai carpinteiro: proximidade relatada, não prova de todo mercado.
- Mecanismo: foto/relato → diagnóstico estruturado e regiões da imagem → brief para profissional; conhecimento local em arquivo de regras/preços/termos, não apenas prompt genérico.
- Sponsor/timing: percepção multimodal + orquestração transformam conhecimento tácito em artefato acionável. Não exclusivo de um modelo.
- Evidência alegada: eval de 12 fotos com mestre e nove dimensões, 74→81 após KB; autor e organizador reportam, **não reproduzimos**, não generalizar e não chamar validação de demanda. Conjunto pequeno com mesmo avaliador/domínio não estima segurança fora dele.
- Rubrica: brief “problema do seu domínio” e prêmio especial de evolução da ideia; não confundir com 1º/2º/3º.
- Lição: ground truth específico e baseline ajudam saber se mecanismo acrescenta valor. Não adotar diagnóstico físico arriscado nem preços inventados.

### Virtual Puppet Theater — Built with Opus 4.7, Most Creative Use (categoria especial, API credits)
Status oficial: mesmo blog Anthropic.
Artefato: https://github.com/rhmoller/virtual-puppet-theater (README inspecionado)
- Job: brincar/criar espetáculo com movimento e voz. Não há dor empresarial forte nem plano comercial; autor explicitamente diz que não pretende produto. Contraexemplo útil: prêmio criativo pode reconhecer encantamento sem mercado.
- Mecanismo: gesto controla fantoche, personagem AI reage e cenários/props surgem pela fala. Resultado é performance interativa, não feed de texto.
- Oportunidade/sponsor: tracking local + palco 3D + diálogo/geração espacial. README lista MediaPipe, Three, Opus, TTS com fallback; browser/hardware têm limites.
- Evidência: README aponta branch hackathon-release, distinguindo main pós-prazo. Não executamos/assistimos. Filho ter se divertido é relato do autor sobre uma pessoa, não validação universal.
- Rubrica: brief oficial admite construir nova forma de fazer/usar; categoria criativa específica confirmada pelo organizador. Não usar esse troféu para inferir receita/capital.

## Contrastes e limites dos não premiados

### CreatorMatch — não vencedor conhecido no acompanhamento, Qloo Agentic 2026
https://devpost.com/software/creatormatch-36ti82
Página relata dor de shortlist de creators, baseline popularidade vs afinidade, chamadas Qloo rastreadas, recusa de entidade errada e demo de dois brands. Declara zero clientes. Esses são sinais concretos de execução/adequação, ainda assim não houve prêmio no acompanhamento. Contraprova de que citar fontes + eval + sponsor seja receita suficiente. Afinidade diferente de popularidade NÃO prova lift de campanha; cobertura por podcast restringe universo e não há dados de resultado comercial. Melhor hipótese de investigação futura: acompanhar decisão real de um marketer com métricas de campanha; não afirmar que essa lacuna causou derrota. Sem scores ou comentários do júri. Não editar entrada congelada.

### Qlaire — contraste próximo, desfecho NÃO confirmado nesta rodada
https://devpost.com/software/qlaire
Mesmo Qloo LLM 2025 de GeoTaste; transforma produto/plataforma/tema em JSON de campanha, com enriquecimento Qloo, job queue e retries. Screenshot captions e fluxo existem; claims de horas poupadas sem benchmark. Dataset antigo marcava não premiado e página atual não exibe prêmio, mas ausência de badge/galeria parcial não é prova suficiente de derrota. Não chamar de perdedor confirmado. Comparação legítima de mecanismo: tanto GeoTaste quanto Qlaire têm LLM + Qloo + front/back, então tags/arquitetura genérica não distinguem valor nem explicam resultado.

Tentativa de verificar lista completa: https://www.linkedin.com/posts/qloo_hackathon-culturalintelligence-aiinnovation-activity-7370873373666549760-4W2g — índice atribui post ao Qloo e menciona GeoTaste/Zesty, mas fetch público exigiu login. Não autenticar nem presumir lista completa. Resultados nominais Qloo 2026 tampouco apareceram nas páginas oficiais acessíveis; não promover Undertow/Backline/Roomful de cards de galeria a vencedores sem prova.

## Padrões repetidos com contraprova

1. **Transformação no objeto da tarefa**: Wrench destaca placa; UnitSet transforma esboço em UI; Maieutic revela drift na própria spec/código; Faxi devolve fax. Inferência: jurado entende causa→efeito sem conhecer arquitetura. Contraexemplo: GeoTaste também tem chat e dashboard; regra não é “banir chat”.
2. **Domínio específico define o que não automatizar**: Maieutic não entrega solução; Wrench pede medida; Faxi preserva confirmação/hábito. Inferência: autoridade do usuário e restrição podem valer mais que autonomia total. Não temos teste de preferência por isso.
3. **Capacidade nova encontra workaround antigo**: esquemas visuais/Wrench; manuscrito/Faxi; geração excessiva/Maieutic; contexto multi-ferramenta/UnitSet. Sponsor não precisa ser tecnicamente insubstituível em toda competição: Kiro é ferramenta de desenvolvimento, Qloo é dados runtime. Provar uso requerido e benefício concreto, não alegar exclusividade falsa.
4. **Encantamento produtivo e encantamento lúdico são caminhos diferentes**: Wrench/UnitSet deixam próxima ação evidente; Puppet ganha criatividade sem objetivo comercial. Não vender entretenimento como business validation.
5. **Prova técnica e operação são gates próprios**: MaestrIA descreve eval contra mestre; Puppet separa branch submetida; UnitSet reconhece indisponibilidade por créditos. Não contar testes no main atual como resultados da submissão; nem assumir que vencedor funciona sempre.
6. **Há bons sinais em não vencedores**: CreatorMatch já tem fonte, baseline, recusa e sponsor no núcleo. Falta de troféu não prova que ideia é ruim; presença desses sinais não prova vitória. Próximo passo precisa testar adoção/resultado, não só adicionar mais frameworks.

## Mudanças nas nossas cinco ideias

- **Decision Afterlife — manter e priorizar para Codegeist, reduzir**: uma premissa explícita, uma decisão e issues afetados; alteração relevante reaparece com evidência. Não construir “memória de tudo”/chat da empresa. Comparar com macro/ADR nativo e medir se usuário toma decisão melhor/mais rápida, sem falsa causalidade. Prioridade de evento, não demanda comprovada.
- **Import Flight Recorder — manter como experimento de produto, mudar demo**: antes/depois e round-trip no dado real do catálogo, reversibilidade e recusa de recuperar dígito sem original. Não fazer limpador CSV genérico, competir primeiro com Power Query/Dromo. Sem sponsor técnico não forçar Firebase. Continua mais simples sem API paga; não chamá-lo automaticamente melhor entrada de hackathon.
- **Tab Escape — reter interno; não priorizar nova entrada**: replay de uma tarefa + regressão e confronto com taba11y/trace. Falta diferencial suficientemente demonstrado; desenho de setas sozinho não é produto novo.
- **Blackout Rehearsal — mudar para job específico e condicionar**: provar nota/foto e estado de confirmação em inspeção não clínica, não “chaos tool universal”. Só evento Firebase se regras e teste mostrarem híbrido realmente necessário; aguardar início/regras. Nenhum build de entrada antecipado.
- **Part Twin — rejeitar para próxima rodada**: fonte/dado compatível escasso, custo de cadastro, risco físico e alternativas nativas; efeito visual não resolve isso. Reabrir apenas com uma família de itens inofensivos, corpus autorizado e pessoa real com problema observado.

## Winner evidence card reutilizável

Evento/edição e regulamento URL | prêmio exato e tipo (geral/categoria/júri/popular/participação) | fonte oficial de status | data de leitura | usuário e tarefa | dor e workaround (fonte direta ou inferência) | capacidade nova | sponsor no build/runtime | mecanismo | transformação de demo | artefato e commit/release | resultado alegado vs verificado | baseline/limites | motivo textual do juiz (se existir) | nossa inferência | contraprova e ideia que mudaria.

“Não encontrado” é valor válido para motivo do júri, cliente, benchmark e vídeo analisado. Nunca preencher com história plausível. Votos/likes não são seleção do júri; bônus de blog/survey não é grand prize.

## Pre-build antes de escrever código

1. Elegibilidade, janela de início, reuso e categoria com fonte oficial atual; separar público igoreduardoai de identidade privada.
2. Uma pessoa/tarefa com dor e workaround, alternativa mais próxima incluindo recurso do sponsor. Identificar benefício que falta medir.
3. Cena de demo: entrada → transformação → resultado verificável → exceção/recusa. Verificar se melhora o trabalho, não apenas aparência.
4. Capability spike futuro só após início permitido: chamada/modelo/ferramenta requerido funciona no caminho crítico com custo/latência observados e fallback honesto.
5. Gabarito/holdout, baseline comparável, revisão humana e teste de adoção separados. Não converter persona sintética em cliente.
6. Evidência para cada critério da rubrica, sem nota prevista. Build/test/deploy e acesso ao jurado sustentáveis até fim do julgamento.
7. Freeze/submit só na janela permitida e com autorização, guardar versão submetida, screenshot e URL. Sem rebatizar projeto enviado como novo.

## Limitações finais

Amostra intencional de sete cases, concentrada em três eventos, não estudo representativo; viés de sobrevivência e disponibilidade. Páginas podem mudar após prêmio, marketing do organizador seleciona histórias, perdedores recebem menos documentação e não temos notas/ordem dos jurados nem testes comparativos de gosto humano. Só um não vencedor confirmado no contexto; segundo candidato tem desfecho incerto. Não calcular percentuais de sucesso, odds individuais, causalidade de tamanho do texto ou ranking “SOTA”. Prêmios Opus são créditos de API: particularmente inadequados como evidência de capital em dinheiro.
