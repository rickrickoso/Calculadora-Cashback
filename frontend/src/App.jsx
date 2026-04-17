import React, { useState } from 'react'
import { History } from 'lucide-react'
import './App.css'

export default function CalculadoraCashback(){
  
  // controla a visualizacao da aba lateral a=t f=f
  const [abaAberta, setAbaAberta] = useState(false)
  // armazena o historico
  const [historicoIP, setHistoricoIP] = useState ([])

  // guarda os valores do formulário
  const [tipoPlano, setTipoPlano] = useState('Normal')
  const [valorCompra, setValorCompra] = useState('')
  const [cupom, setCupom] = useState('')
  // calcula valor total e cashback
  const [resultado, setResultado] = useState(null)

  const carregarHistorico = async () => {
    try {
      // faz um GET pro historico
      const response = await fetch('https://calculadora-cashback-lpng.onrender.com/consulta/historico')
      const data = await response.json() // converte pra json
      setHistoricoIP(data.dados) // salva os dados
    } catch(error) {
      console.error("Erro ao buscar histórico:", error)
    }
  }
// funcao que abre/fecha a aba lateral e atualiza o histórico
  const alternarAba = () => {
    const novaAbaAberta = !abaAberta
    setAbaAberta(novaAbaAberta)
    if (novaAbaAberta) {
      carregarHistorico();
    }
  }
  // funcao que calcula o cashback
  const calcularCashback = async (e) => {
    e.preventDefault() // evita recarregar pag
    // cria o JSON que o python recebe
    const payload = {
      valor_subtotal: parseFloat(valorCompra) || 0, // texto -> decimal
      percentual_cupom: parseFloat(cupom) || 0,
      is_vip: tipoPlano === 'VIP' // transforma a string em bool
    }

    try {
      const response = await fetch('https://calculadora-cashback-lpng.onrender.com/consulta/cashback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json' // comunica envio json
        },
        body: JSON.stringify(payload)
      })
      
      if (!response.ok){
        alert("Por favor, insira apenas valores válidos e maiores que zero.")
        return
      }

      // pega a data da consulta
      const data = await response.json()
      setResultado(data)

      if (abaAberta){
        carregarHistorico()
      }

    } catch (error) {
      console.error("Erro na requisicao:", error)
      alert("Ocorreu um erro ao conectar com o servidor.")
    }
  }
    // Interface

  return (
    <div className="container-principal">
      {/*Cabecalho*/}
      <header className="barra-superior">
        <div className="logo-container">
          <img src="/nology_br_logo.jpg" alt="Logo Nology" className='logo-img'/>
          <h2>Nology</h2>
        </div>
        <button onClick={alternarAba} className="botao-historico" title="Histórico">
          <History size={24} />
        </button>
      </header>

      <main className="conteudo-calculadora">
        <h1 className="titulo">Calculadora de Cashback</h1>

        {/*Formulario*/}
        <form className="formulario-cashback" onSubmit={calcularCashback}>
          <div className='campo-form'>
            <label>Tipo de Plano:</label>
            <select value={tipoPlano} onChange={(e) => setTipoPlano(e.target.value)}>
            <option value="Normal">Normal</option>
            <option value="VIP">VIP</option>
            </select>
          </div>
        
        <div className="campo-form">
          <label>Valor da compra: R$</label>
          <input
            type="number"
            step="0.01" // numeros decimais
            value={valorCompra}
            onChange={(e) => setValorCompra(e.target.value)}
            required
          /> 
        </div>

        <div className="campo-form">
          <label>Possui cupom? (%)</label>
          <input
          type="number"
          placeholder="0"
          value={cupom}
          onChange={(e) => setCupom(e.target.value)}
        />
        </div>

        <button type="submit" className="botao-calcular">Calcular</button>

        </form>

        {/*Resultado*/}
        {resultado && (
          <div className="resultado-box">
            <h3>Resultado:</h3>
            <p>Valor Final: R$ {resultado.Valor_Total.toFixed(2)}</p>
            <p>Seu Cashback: R$ {resultado.Cashback.toFixed(2)}</p>
          </div>
        )}
      </main>

      {abaAberta && (
        <aside className='aba-lateral'>
          <div className='cabecalho-aba'>
            <h3>Histórico de Consultas</h3>
            <button className='fecha-aba' onClick={alternarAba}>Fechar</button>
          </div>

          <ul className="lista-historico">
            {historicoIP.length > 0 ? (
              historicoIP.map((item) => (
                <li key={item.id}>
                  <strong>[{item.data_formatada}]</strong> <br/>
                  R$ {item.valor_total} {'->'} Cashback: R$ {item.cashback}
                  { item.vip ? ' (VIP)' : ' (Normal)'}
                </li>
              ))
            ) : (
              <p>Nenhuma consulta encontrada.</p>  
            )}
          </ul>
        </aside>
      )}
    </div>
  )
}


