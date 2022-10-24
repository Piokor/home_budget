import { getRequest } from './utils';

async function getUsers(username) {
    return getRequest(
        '/users',
        {
            query_str: username
        }
    )
}

export {getUsers}