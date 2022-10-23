import { postRequest } from './utils';

async function createTransaction(transaction) {
    return postRequest(
        '/create_transaction',
        transaction
    )
}

export {createTransaction}