describe('Home Page Tests', () => {
  it('Visits the Home Page and verifies its content', () => {
    cy.visit('http://localhost:3000/')

    cy.get('h1').contains('Bem-vindo à Loja de Card Games')
    cy.get('.me-3').contains('Adicionar Cartas').should('be.visible')
    cy.get('.container > [href="/list-cards"]').contains('Visualizar Estoque').should('be.visible')

    cy.get('.sidebar').within(() => {
      cy.contains('Home').should('be.visible')
      cy.contains('Cadastro de Cartas').should('be.visible')
      cy.contains('Estoque de Cartas').should('be.visible')
      cy.contains('Histórico de Vendas').should('be.visible')
      cy.contains('Resetar o Banco de Dados').should('be.visible')
    })

    cy.get('footer').contains('© 2024 Loja de Card Games. Desenvolvido com criatividade e paixão.')
  })
})

describe('Add Card Tests', () => {
  it('Visits the Add Card page and adds a new card', () => {

    cy.visit('http://localhost:3000/add-card-form')

    cy.get('form').should('be.visible')

    cy.get('#name').type('Counterspell')
    cy.get('#cost').type('UU', { parseSpecialCharSequences: false })
    cy.get('#rarity').type('Incomum')
    cy.get('#type').type('Instant')
    cy.get('#description').type('Counter target spell.')
    cy.get('#quantity').type('10')
    cy.get('#price').type('15.50')

    cy.get('.btn').click()

    cy.url().should('include', '/list-cards')

    cy.get('table').contains('td', 'Counterspell').should('be.visible')
    cy.get('table').contains('td', 'UU').should('be.visible')
    cy.get('table').contains('td', 'Incomum').should('be.visible')
    cy.get('table').contains('td', '10').should('be.visible')
    cy.get('table').contains('td', '15.5').should('be.visible')
  })
})

describe('Reset Database Tests', () => {
  it('Visits the Reset Database page and performs the reset', () => {
    cy.visit('http://localhost:3000/reset-database')

    cy.get('.success-message').contains('O Banco de Dados foi resetado com sucesso!').should('be.visible')

    cy.get('.btn').contains('Voltar ao Estoque de Cartas').should('be.visible').click()

    cy.url().should('include', '/list-cards')
  })
})

describe('Sell Card Tests', () => {
  it('Visits the Sell Card page and sells a card', () => {
    cy.visit('http://localhost:3000/list-cards')

    cy.get('table').should('be.visible')

    cy.get('table')
      .contains('td', 'Lightning Bolt') 
      .parents('tr') 
      .find('[action="/sell-card/1"] > .btn')
      .click()

    cy.get('#quantity').type('2')
    cy.get('.btn').contains('Vender').click()

    cy.visit('http://localhost:3000/list-cards')
    cy.get('table')
      .contains('td', 'Lightning Bolt')
      .parents('tr')
      .find('td')
      .contains('43')
      .should('be.visible')
  })
})

describe('Sales History Page Tests', () => {
  it('Visits the Sales History page and verifies its content', () => {
    cy.visit('http://localhost:3000/list-sales')

    cy.get('h1').contains('Histórico de Vendas').should('be.visible')

    cy.get('table').should('be.visible')

    cy.get('table thead').within(() => {
      cy.contains('ID da Carta Vendida').should('be.visible')
      cy.contains('Valor de Venda').should('be.visible')
      cy.contains('Data e Horário de Venda').should('be.visible')
    });

    cy.get('table tbody tr').should('have.length.at.least', 1)

    cy.get('table').contains('Total:').should('be.visible')
    cy.get('table').contains('26.1').should('be.visible')

    cy.get('footer').contains('© 2024 Loja de Card Games. Desenvolvido com criatividade e paixão.').should('be.visible')
  })
})

describe('Cards Inventory Page Tests', () => {
  it('Visits the Cards Inventory page and verifies its content', () => {
    cy.visit('http://localhost:3000/list-cards');

    cy.get('h1').contains('Estoque de Cartas').should('be.visible');

    cy.get('table').should('be.visible');

    cy.get('table thead').within(() => {
      cy.contains('Nome').should('be.visible');
      cy.contains('Custo Convertido').should('be.visible');
      cy.contains('Raridade').should('be.visible');
      cy.contains('Tipo').should('be.visible');
      cy.contains('Descrição').should('be.visible');
      cy.contains('Quantidade').should('be.visible');
      cy.contains('Preço').should('be.visible');
    });

    cy.get('table tbody tr').should('have.length.at.least', 1);

    cy.get('table tbody tr').each(($row) => {
      cy.wrap($row).within(() => {
        cy.contains('Excluir').should('be.visible');
        cy.contains('Atualizar').should('be.visible');
        cy.contains('Vender').should('be.visible');
      });
    });

    cy.get('footer').contains('© 2024 Loja de Card Games. Desenvolvido com criatividade e paixão.').should('be.visible');
  });
});



