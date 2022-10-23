import { request } from './utils';

async function getBudgets() {
    return request(
        'get',
        '/budgets',
        {}
    )
}

async function createBudget(title, description) {
    return request(
        'post',
        '/create_budget',
        {
            title: title,
            description: description
        }
    )
}

export {getBudgets, createBudget}