# Calculadora de Cashback

Este repositório contém a solução Full-Stack para uma calculadora de cashback.

## 🚀 Links da Aplicação
- **Frontend (App Hospedado):** https://calculadora-cashback.vercel.app/
- **Backend (API URL):** https://calculadora-cashback-lpng.onrender.com/docs

## 🛠️ Arquitetura e Tecnologias Utilizadas
- **Frontend:** Desenvolvido em React (Vite) e CSS puro. Hospedado na **Vercel**.
- **Backend:** Desenvolvido em Python com FastAPI, responsável por processar as regras de negócio de bônus e dobro de cashback. Hospedado no **Render**.
- **Banco de Dados:** PostgreSQL hospedado na **Neon.tech**. Utilizado para registrar o histórico de consultas, vinculando cada transação ao IP do usuário.

## 📋 Regras de Negócio Implementadas
A API processa os cálculos em cascata conforme a documentação:
1. Aplica o desconto do cupom sobre o valor total.
2. Calcula o cashback base (5% do valor final).
3. Verifica a promoção comercial (dobra o cashback se o valor final > R$ 500).
4. Aplica o bônus VIP (10% de acréscimo sobre o valor do cashback processado).
5. Armazena cada consulta feita pelo ip do usuário