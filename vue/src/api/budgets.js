import { postRequest, getRequest } from './utils';

async function getBudgets() {
    return getRequest(
        '/budgets',
        {}
    )
}

async function getBudget(id) {
    return getRequest(
        '/budget',
        {
            id: id
        }
    )
}

async function createBudget(title, description) {
    return postRequest(
        '/create_budget',
        {
            title: title,
            description: description
        }
    )
}

export {getBudgets, createBudget, getBudget}