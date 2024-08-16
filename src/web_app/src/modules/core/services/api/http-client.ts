import ky, { type KyInstance} from 'ky';

export const httpClient: KyInstance = ky.create({
    prefixUrl: import.meta.env.VITE_APP_API_URL,
});
