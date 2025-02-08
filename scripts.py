scripts = {
    "atendimento": """
    Estrutura de Atendimento
    - Saudação Inicial: (Ex.: "Sette Fibra - Consultor - nome. Bom dia/boa tarde/boa noite. Como posso ajudar?")
    - Confirmação de Dados Cadastrais: CPF, sexo do titular, endereço, dois números de contato, WhatsApp, e-mail.
    - Protocolo de Atendimento: Informar o protocolo ao cliente no início do atendimento.
    - Tratativa da Solicitação:
    - Interação Durante o Atendimento: Manter o cliente informado.
    - Saudação Final: ("Posso ajudar em algo mais? A Sette Fibra agradece seu contato.")
    """,

    "principais": """
    Principais Assuntos de Atendimento
    - Sem Conexão: Identificar problemas no roteador, cabos, ou sinal.
    - Lentidão: Atualizar roteador, testar dispositivos, e realizar teste de velocidade.
    - Oscilações/Quedas: Gerar relatórios, verificar ONU, validar configurações.
    - Alteração de Senha: Acessar roteador pelo IP e realizar ajustes.
    - Sem Acesso a Aplicativos/Sites: Alterar DNS, testar em outra rede.
    - Sem Acesso a Câmeras: Redirecionar portas, verificar IP fixo.
    """,

    "servicos": """
    Serviços Disponíveis
    - Atualização de plano.
    - Upgrade ou downgrade de plano.
    - Renovação contratual.
    - Transferência de endereço.
    """,

    "planos_atualizados_se77e": """
    🔗 [Planos Atualizados SE77E](https://app.clickup.com/36969994/docs/1387ga-6643/1387ga-9013)
    Clique no link acima para acessar as informações atualizadas sobre os planos.
    """,

    "transferencia_endereco": """
    **Transferência de Endereço**
    - Endereço atual
    - Novo endereço: CEP, Ponto de referência
    - Valor da taxa
    - Contato
    - Protocolo
    - Data do agendamento

    Observação: Solicitar ao cliente que leve os equipamentos para o novo endereço.
    Taxa: R$ 100,00 à vista ou R$ 120,00 parcelado em até 4x.
    """,

    "juridico": """
    **Jurídico**
    Segue número do Jurídico da Sette para clientes com contas bloqueadas que desejam fazer acordo:
    - 📞 62 93300-2036
    """,

    "cancelamento": """
    **Cancelamento**
    Para realizar o cancelamento:
    - Via WhatsApp: Selecione "Outras Opções" no atendimento automático.
    - Via ligação: Ligue para 4051-9377 (departamento SAC).
    """,

    "app_sette": """
    **Aplicativo Sette Fibra**
    Você pode acessar todos os boletos na central do assinante pelo aplicativo Sette Fibra.
    - Login e senha: Apenas os números do CPF ou CNPJ.
    """,

    "renovacao_contratual": """
    **Renovação Contratual**
    - Tipo de assinatura de contrato: (Aceite de voz / 100% digital)
    - Quantos meses tem o contrato:
    - Data:
    - Hora:
    - Plano:
    - Valor:
    - Tipo de cobrança: (Carnê / digital)
    - Contato:
    - Protocolo:
    - Atendente responsável:
    """,

    "los": """
    LOS (Loss of Signal) - Aviso
    Essa luz vermelha se chama LOS. Quando ela acende em vermelho, significa um problema físico na fibra (tanto interna quanto externa). 
    As causas mais comuns incluem:
    - Fibra rompida na rua;
    - Conector danificado (pontinha verde conectada no equipamento);
    - Outras questões físicas.

    Procedimento:
    Poderia retirar o equipamento da tomada por 3 minutos, por gentileza?
    """,

    "velocidade": """
    Orientações para Teste de Velocidade
    1. Durante o teste, deve haver apenas um aparelho conectado à rede. Caso contrário, outros dispositivos podem consumir banda e afetar o resultado.
    2. Realizar o teste na rede 5G, próximo ao roteador. A rede 2.4G é limitada a 60 Mbps devido à sua tecnologia mais antiga.
    - Caso a rede 5G não apareça, o dispositivo pode não ser compatível.
    - Como alternativa, o teste pode ser feito com cabo de rede conectado ao PC ou notebook.
    3. Certificar-se de que o aparelho suporta a velocidade contratada.
    
    Links para Teste:
    - [Fast](https://fast.com/pt/)
    - [SpeedTest](https://www.speedtest.net/pt)
    """,

    "renovacao": """
    Script de Renovação
    Introdução: "Para atualizar seus dados, podemos confirmar algumas informações, por gentileza?"
    - CPF: _____
    - RG: ______
    - Endereço completo: ______
    - Telefone: ______
    - E-mail: ______

    Encerramento: "O(a) Senhor(a) concorda com a assinatura de contrato/renovação por 12 meses?" (SIM/NÃO)
    """,

    "observacoes": """
    Observações Gerais
    - Todo atendimento é de responsabilidade do Contact Center.
    - Transferências que exigem intervenção de outro setor são registradas no IXC.
    - Chats e ligações só podem ser transferidos para cobrança em caso de renegociação ou para o SAC após tentativa de reversão.
    """,

    "configuracao_max": """
    **Configuração MAX**
    1. Clique em "Conectar Provedor".
    2. Selecione o provedor PLAYHUB.
    3. Preencha:
       - Provedor: SE77E
       - Código: 
       - Senha:
    """,

    "valores_procedimentos": """
    **Procedimentos**
    - Atualização de Plano: R$ 5,00
    - Renovação Contratual: R$ 5,00
    - Troca de Titularidade: R$ 5,00
    - Reversão de Cancelamento: R$ 5,00
    - Venda À la Carte: R$ 3,50

    **Upgrade e Migração**
    - 1 GB: R$ 9,00
    - 750 MB: R$ 6,00
    - 550 MB ou 600 MB: R$ 4,00
    - 200 MB: R$ 1,50

    **Wireless Condomínio**
    - 15 MB: R$ 1,50
    - 25 MB: R$ 2,00
    - 35 MB: R$ 3,00
    - 50 MB: R$ 4,00
    - 100 MB: R$ 8,00

    **Plano Wireless**
    - 7 MB: R$ 0,50
    - 10 MB: R$ 2,00
    - 15 MB: R$ 3,00

    **Obs:** Caso a meta não seja atingida, será pago 50% do valor de cada plano e serviço.
    """,

    "formulario_contact_center": """
    **Formulário Contact Center**
    Acesse o formulário no link abaixo:
    - [Formulário Contact Center](https://docs.google.com/forms/d/e/1FAIpQLSfdwHV1XU4t7Lxyzmuro3-4yMdZE8VgY-IVf8U6xG_PaeHzHQ/viewform)
    """,

    "downdetector": """
    **Downdetector**
    Consulte o status de serviços no Downdetector:
    - [Downdetector](https://downdetector.com.br/)
    """
}
