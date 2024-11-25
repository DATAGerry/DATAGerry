export interface Webhook {
    public_id: number;
    name: string;
    url: string;
    event_types: string[];
    active: boolean;
}

export interface WebhookCreate {
    name: string;
    url: string;
    event_types: string[];
    active: boolean;
}

export interface WebhookUpdate extends WebhookCreate {
    public_id: number;
}

export interface WebhookLog {
    date: string; // Date when the webhook was triggered
    status: 'successful' | 'failed'; // Status of the webhook trigger
    response_code: number; // HTTP response code
}
