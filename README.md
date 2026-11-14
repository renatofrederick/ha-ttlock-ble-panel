# TTLock BLE Panel Bridge

Integração HACS privada que adiciona `ttlock_ble_panel.get_passcodes` ao Access
Panel sem substituir, copiar ou modificar a integração oficial `ttlock_ble`.

## O que ela faz

- Restaura somente a leitura e sincronização de PINs pelo Access Panel.
- Não habilita criar, alterar ou excluir PINs.
- Não altera a integração oficial `ttlock_ble`; ela continua atualizável pelo
  HACS como antes.

## Instalação pelo HACS

1. Confirme que a integração oficial **TTLock BLE** está instalada, carregada e
   possui a entidade `lock.*` da fechadura.
2. No HACS, abra o menu de três pontos → **Repositórios personalizados**.
3. Adicione a URL deste repositório privado e escolha a categoria
   **Integration**. A conta do GitHub conectada ao HACS precisa ter acesso a
   este repositório.
4. Procure por **TTLock BLE Panel Bridge** no HACS e instale-o.
5. Reinicie o Home Assistant uma única vez para carregar o componente.
6. Em **Configurações → Dispositivos e serviços → Adicionar integração**,
   adicione **TTLock BLE Panel Bridge**. Não há token, senha ou configuração
   extra para preencher.
7. Atualize o Access Panel com a branch
   `ttlock-panel-read-adapter`; ela passa a usar
   `ttlock_ble_panel.get_passcodes`.

Depois disso, o painel volta a listar e sincronizar os PINs lidos por BLE.
Antes de promover a atualização do painel, faça uma leitura manual em uma
fechadura administrada por você.

## Segurança

O serviço retorna PINs reais somente na resposta de uma chamada autenticada ao
Home Assistant. Ele não cria entidades, não grava estados, histórico,
diagnósticos ou logs. Quem tiver permissão para chamar esse serviço poderá ler
os PINs; use no Access Panel uma credencial própria do Home Assistant, com o
menor privilégio compatível, e não torne este repositório público.

## Atualização e rollback

- Atualize normalmente pelo HACS; a integração oficial `ttlock_ble` é
  independente desta ponte.
- Se uma atualização da ponte falhar, use **Redownload** no HACS para voltar à
  versão anterior disponível e reinicie o Home Assistant.
- Para remover a ponte, remova primeiro a configuração dela em
  **Dispositivos e serviços**, depois desinstale-a pelo HACS. Isso não remove
  fechaduras, entidades ou o histórico de `ttlock_ble`.

## Compatibility

Testada contra `ha-ttlock-ble` `v3.12.2`. A ponte lê a conexão ativa dessa
integração, que não é uma API pública do upstream. Se uma atualização futura
do TTLock BLE mudar essa interface, a leitura falhará com um erro claro no Home
Assistant; a fechadura e a integração oficial permanecem sem alteração.
