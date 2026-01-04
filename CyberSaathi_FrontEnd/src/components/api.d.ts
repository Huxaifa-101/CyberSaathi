/**
 * Type definitions for CyberSaathi API Client
 */

export interface ApiConfig {
    baseUrl: string;
    headers: {
        'Content-Type': string;
    };
}

export interface ChatResponse {
    answer: string;
    sources?: Array<{
        document: string;
        page?: number;
        relevance?: number;
    }>;
    query?: string;
}

export interface HealthResponse {
    status: string;
    message?: string;
}

export interface InfoResponse {
    version?: string;
    models?: string[];
    [key: string]: any;
}

export interface CyberSaathiAPI {
    chat(query: string): Promise<ChatResponse>;
    healthCheck(): Promise<HealthResponse>;
    getInfo(): Promise<InfoResponse>;
    testConnection(): Promise<boolean>;
}

export const apiConfig: ApiConfig;
export const cyberSaathiAPI: CyberSaathiAPI;

declare const _default: CyberSaathiAPI;
export default _default;
